#!/usr/bin/env python3
#
# WordPress XML to Context-Aware Text Converter - Version 8 (Definitive)
#
# A script to parse a WordPress XML export file and extract clean, readable
# text content from all public pages, while reconstructing their hierarchical context.
#
# It uses a 3-tier priority system to find the most accurate page path:
# 1. Menu Path (via direct ID or custom URL match)
# 2. Page Parent Hierarchy (from wp:post_parent)
# 3. Inferred Path from URL structure (e.g., /parent/child/)
#
# This approach ensures the most reliable context for knowledge bases or site analysis.
# Developed in a collaborative, iterative process.
#
# Usage:
# clear; python parse_wp.py sl5de.WordPress.2025-06-16.xml cleaned_output.txt; kate cleaned_output.txt


import sys
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup, Comment
import re
from urllib.parse import urlparse, unquote

NAMESPACES = {
    'wp': 'http://wordpress.org/export/1.2/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
}

def clean_html_and_shortcodes(html_content):
    if not html_content: return ""
    soup = BeautifulSoup(html_content, 'lxml')
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        if 'wp:' in comment: comment.extract()
    text = soup.get_text(separator=' ', strip=True)
    text = re.sub(r'\[[^\]]+\]', '', text)
    return text.strip()

def get_path_from_url(url_string):
    """Extracts the cleaned path segments from a URL."""
    if not url_string: return []
    # unquote() handles URL-encoded characters like %f0%9f...
    path = unquote(urlparse(url_string).path)
    return [part for part in path.split('/') if part]

def parse_wordpress_xml(xml_file_path, output_file_path):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"XML-Fehler: Datei '{xml_file_path}' konnte nicht gelesen werden. Details: {e}")
        return

    # --- PASS 1: Sammle alle relevanten Daten und erstelle Mappings ---
    german_pages = {}
    all_menu_items = {}
    # NEUES MAPPING: Von URL-Slug zum Seiten-Titel
    slug_to_title = {}

    for item in root.findall('.//item'):
        post_type_elem = item.find('wp:post_type', NAMESPACES)
        if post_type_elem is None: continue
        post_type = post_type_elem.text

        if post_type == 'page':
            lang_category = item.find("category[@domain='language'][@nicename='de']")
            if lang_category is not None:
                post_id = item.find('wp:post_id', NAMESPACES).text
                title = (item.find('title').text or "Unbenannte Seite").strip()
                content = item.find('content:encoded', NAMESPACES).text or ""
                link = item.find('link').text or ""
                parent_id = (item.find('wp:post_parent', NAMESPACES) or ET.Element("")).text or '0'

                page_data = {'id': post_id, 'title': title, 'content': content, 'link': link, 'parent_id': parent_id}
                german_pages[post_id] = page_data

                # Fülle das Slug-Mapping
                path_parts = get_path_from_url(link)
                if path_parts:
                    slug_to_title[path_parts[-1]] = title

        elif post_type == 'nav_menu_item':
            menu_item_id = item.find('wp:post_id', NAMESPACES).text
            title = (item.find('title').text or "").strip()
            url, linked_page_id, parent_menu_id = '', '0', '0'
            for meta in item.findall('wp:postmeta', NAMESPACES):
                key, val = meta.find('wp:meta_key', NAMESPACES).text, meta.find('wp:meta_value', NAMESPACES).text
                if key == '_menu_item_object_id': linked_page_id = val
                elif key == '_menu_item_menu_item_parent': parent_menu_id = val
                elif key == '_menu_item_url': url = val
            all_menu_items[menu_item_id] = {'title': title, 'parent_id': parent_menu_id, 'page_id': linked_page_id, 'url': url}

    # --- PASS 2: Verbinde und schreibe ---
    with open(output_file_path, 'w', encoding='utf-8') as f_out:
        for page_id, page_data in sorted(german_pages.items(), key=lambda x: int(x[0])):
            clean_content = clean_html_and_shortcodes(page_data['content'])
            if not clean_content: continue

            breadcrumb = None
            source = "Status"

            # Priorität 1: Menü-Pfad (via ID oder URL)
            menu_item_id_for_page = None
            for m_id, m_data in all_menu_items.items():
                if m_data['page_id'] == page_id:
                    menu_item_id_for_page = m_id
                    break
            if not menu_item_id_for_page:
                page_link_norm = page_data['link'].strip().rstrip('/')
                for m_id, m_data in all_menu_items.items():
                    if m_data['url'].strip().rstrip('/') == page_link_norm:
                        menu_item_id_for_page = m_id
                        break
            if menu_item_id_for_page:
                path = []
                current_menu_id = menu_item_id_for_page
                for _ in range(10):
                    if current_menu_id not in all_menu_items: break
                    menu_item = all_menu_items[current_menu_id]
                    if menu_item['title']: path.insert(0, menu_item['title'])
                    parent_id = menu_item.get('parent_id', '0')
                    if parent_id == '0': break
                    current_menu_id = parent_id
                if path:
                    breadcrumb = " > ".join(path)
                    source = "Menüpfad"

            # Priorität 2: Expliziter Eltern-Pfad
            if not breadcrumb:
                path_list = []
                current_id = page_id
                for _ in range(10):
                    if current_id not in german_pages: break
                    path_list.insert(0, german_pages[current_id]['title'])
                    parent_id = german_pages[current_id].get('parent_id', '0')
                    if parent_id == '0' or parent_id not in german_pages: break
                    current_id = parent_id
                if len(path_list) > 1:
                    breadcrumb = " > ".join(path_list)
                    source = "Seiten-Hierarchie"

            # Priorität 3: Vollständiger URL-Pfad
            if not breadcrumb:
                path_slugs = get_path_from_url(page_data['link'])
                if len(path_slugs) > 1:
                    # Wandle alle Slugs im Pfad in Titel um
                    path_titles = [slug_to_title.get(slug, slug.replace('-', ' ').title()) for slug in path_slugs]
                    breadcrumb = " > ".join(path_titles)
                    source = "URL-Pfad"

            if not breadcrumb:
                breadcrumb = "Nicht zugeordnet"

            f_out.write(f"# Seite: {page_data['title']}\n")
            f_out.write(f"# {source}: {breadcrumb}\n\n")
            f_out.write(f"{clean_content}\n\n---\n\n")

    print(f"Erfolgreich! Die sauberen Seiteninhalte wurden in die Datei '{output_file_path}' geschrieben.")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Anwendung: python parse_wp_v8.py <input_datei.xml> <output_datei.txt>")
        sys.exit(1)
    parse_wordpress_xml(sys.argv[1], sys.argv[2])
