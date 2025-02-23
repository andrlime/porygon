"""
Chimecho entry point main.py to generate schedule html and png
"""

from chimecho.config import AppConfig
from chimecho.scheduler import load_templates, generate_week_html
from chimecho.render import render_html_page


def main():
    template_folder, _, _, output = AppConfig().get_cli_values()
    generate_week_html(load_templates(template_folder))
    render_html_page(f"{output}.html")


if __name__ == "__main__":
    main()
