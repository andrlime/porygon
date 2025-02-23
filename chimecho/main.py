"""
Chimecho entry point main.py to generate schedule html and png
"""

from chimecho.config import AppConfig
from chimecho.render import render_html_page
from chimecho.scheduler import generate_week_html, load_templates


if __name__ == "__main__":
    template_folder, _, _, output = AppConfig().get_cli_values()
    generate_week_html(load_templates(template_folder))
    render_html_page(f"{output}.html")
