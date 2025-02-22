"""
Chimecho entry point main.py to generate schedule html and png
"""

import logging

from chimecho.core.config import AppConfig
from chimecho.core.scheduler import load_templates, generate_week_html
from chimecho.core.render import render_html_page


def main():
    template_folder, _, _, output = AppConfig().get_cli_values()
    templates = load_templates(template_folder)
    html_week = generate_week_html(templates)

    with open(f"{output}.html", "w", encoding="utf-8") as f:
        f.write(html_week)

    logging.info("Weekly schedule generated as %s.html", output)

    render_html_page(f"{output}.html")


if __name__ == "__main__":
    main()
