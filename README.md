# WordPress XML to Context-Aware Text Converter

A Python script to parse a WordPress XML export file (`.xml`) and extract clean, readable text content from all public pages.

What makes this script special is its ability to reconstruct the **hierarchical context** for each page. It intelligently determines a page's position within the site structure, creating a single, well-organized text file ideal for context-aware knowledge bases (e.g., for RAG pipelines with LLMs), site analysis, or content migration.

## Key Features

-   **Clean Text Extraction:** Strips all HTML tags, comments, and WordPress shortcodes to deliver pure text content.
-   **Hierarchical Context:** For each page, it provides a "breadcrumb" path (e.g., `Solutions > Project Experiences`).
-   **Intelligent 3-Tier Path-Finding:** It uses a robust, prioritized logic to find the most accurate path:
    1.  **Menu Path:** Reconstructs the path from the visible navigation menus (including custom links).
    2.  **Parent-Page Hierarchy:** Falls back to the parent-page relationships set in the WordPress backend.
    3.  **URL Structure:** As a final fallback, it infers the hierarchy directly from the page's URL structure.
-   **Multilingual Support:** Designed to correctly handle exports from multilingual sites (e.g., using Polylang) by focusing on a specific language.
-   **Structured Output:** Formats the output with clear headers for each page, including the page title and its discovered path, making it highly readable and easy to parse.

## Prerequisites

You need Python 3 and a few common libraries. You can install the dependencies using pip:

```bash
pip install beautifulsoup4 lxml
```
Or on an Arch/Manjaro-based system:
```bash
sudo pacman -S python-beautifulsoup4 python-lxml
```

## Usage

1.  **Export Your Content:** In your WordPress dashboard, go to `Tools` → `Export` (`Werkzeuge` → `Daten exportieren`). **Crucially, select `All content` (`Alle Inhalte`)**. A partial export (e.g., only "Pages") will not work, as the script needs menu and relationship data. This will give you a `.xml` file.

2.  **Run the Script:** Place the `parse_wp.py` script and your exported `.xml` file in the same directory. Run the script from your terminal, providing the input XML file and the desired output text file as arguments:
    ```bash
    python parse_wp.py your_wordpress_export.xml cleaned_output.txt
    ```
    The script will create `cleaned_output.txt` with the structured content.

### Pro-Tip

To run the script and immediately open the result in a text editor (like Kate, Gedit, VSCode, etc.), you can chain the commands. This is great for a fast feedback loop.

```bash
# On Linux (with Kate editor)
clear; python parse_wp.py your_wordpress_export.xml output.txt; kate output.txt

# On macOS (with TextEdit)
clear; python parse_wp.py your_wordpress_export.xml output.txt; open -a TextEdit output.txt

# On Windows (with Notepad)
cls && python parse_wp.py your_wordpress_export.xml output.txt && notepad output.txt
```

## Example Output

The script clearly indicates the source of the discovered path (`Menüpfad`, `Seiten-Hierarchie`, `URL-Pfad`, or `Status`):

```
# Seite: Gründer
# Seiten-Hierarchie: Über SL5 > Gründer

SL5 Sebastian: Manche Karrieren beginnen geradlinig im Büro...

---

# Seite: Kundenstimmen
# Menüpfad: Über SL5 > Kundenstimmen

Kurse für SQL, Java, PHP, JS, Python seit 2001...

---

# Seite: Projekt-TÜV
# Status: Nicht zugeordnet

Ist Ihr Software-Projekt in Gefahr?

---
```

MIT License

Copyright (c) 2024 Sebastian Lauffer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
