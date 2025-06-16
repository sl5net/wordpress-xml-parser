#!/usr/bin/env python3
#
# WordPress XML to Clean Text Converter
#
# A script to parse a WordPress XML export file and extract the clean,
# readable text content from all public pages, formatting it for use
# in a chatbot knowledge base.
#
# Usage:
# python parse_wp.py your_wordpress_export.xml cleaned_output.txt
#

# --- LIBRARIES ---

import sys
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup, Comment
import re


# MIT License: anyone can do almost anything with this code


# python parse_wp.py sl5de.WordPress.2025-06-16.xml sl5de.WordPress.2025-06-16.txt

# Define namespaces found in the WordPress XML file. This is crucial.
NAMESPACES = {
    'wp': 'http://wordpress.org/export/1.2/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
}

def clean_html_and_shortcodes(html_content):
    """Uses BeautifulSoup to strip all HTML tags and cleans shortcodes."""
    if not html_content:
        return ""

    soup = BeautifulSoup(html_content, 'lxml')

    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        if 'wp:' in comment:
            comment.extract()

    text = soup.get_text(separator=' ', strip=True)
    text = re.sub(r'\[[^\]]+\]', '', text)
    text = re.sub(r'([A-Z])\s+([a-z])', r'\1\2', text)

    return text.strip()

def parse_wordpress_xml(xml_file_path, output_file_path):
    """Parses a WordPress XML file and extracts clean text from pages."""
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"XML-Fehler: Die Datei '{xml_file_path}' konnte nicht gelesen werden. Ist sie gültig?")
        print(f"Fehlerdetails: {e}")
        return

    with open(output_file_path, 'w', encoding='utf-8') as f_out:
        for item in root.findall('.//item'):
            post_type_element = item.find('wp:post_type', NAMESPACES)
            if post_type_element is not None and post_type_element.text == 'page':
                title_element = item.find('title')
                title = title_element.text if title_element is not None else "Unbenannte Seite"

                # --- THIS IS THE LINE I HAVE FIXED ---
                # It now correctly uses NAMESPACES (all caps)
                encoded_content_element = item.find('content:encoded', NAMESPACES)
                # -------------------------------------

                encoded_content = encoded_content_element.text if encoded_content_element is not None else ""

                clean_content = clean_html_and_shortcodes(encoded_content)

                if clean_content:
                    f_out.write(f"# Seite: {title}\n\n")
                    f_out.write(f"{clean_content}\n")
                    f_out.write("\n---\n\n")

    print(f"Erfolgreich! Die sauberen Seiteninhalte wurden in die Datei '{output_file_path}' geschrieben.")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Anwendung: python parse_wp.py <input_datei.xml> <output_datei.txt>")
        sys.exit(1)

    input_xml = sys.argv[1]
    output_txt = sys.argv[2]

    try:
        parse_wordpress_xml(input_xml, output_txt)
    except FileNotFoundError:
        print(f"Fehler: Die Datei '{input_xml}' wurde nicht gefunden.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
