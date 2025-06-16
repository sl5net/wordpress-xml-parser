# WordPress XML to Clean Text Converter

A Python script to parse a WordPress XML export file (`.xml`) and extract the clean, readable text content from all public pages.

The output is a single, structured text file (`.txt`) formatted with page titles and separators, making it ideal for use as a knowledge base for chatbots or other language models.

## Prerequisites

You need Python 3 and a few libraries. On a Manjaro/Arch-based system, you can install them with:

```bash
sudo pacman -S python-beautifulsoup4 python-lxml
```

## Usage

1.  Export your site content from the WordPress dashboard by going to `Werkzeuge` → `Daten exportieren` (Tools → Export) and selecting `Seiten` (Pages). This will give you a `.xml` file.
2.  Place the `parse_wp.py` script and your exported `.xml` file in the same directory.
3.  Run the script from your terminal, providing the input XML file and the desired output text file as arguments:

```bash
python parse_wp.py your_wordpress_export.xml cleaned_output.txt
```
The script will create `cleaned_output.txt` containing the cleaned text from all your pages.
```

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
```

