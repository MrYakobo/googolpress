#!/usr/bin/env python3
import argparse
from datetime import datetime
from glob import glob
import os
from pathlib import Path
import re
import subprocess
from jinja2 import Template
from bs4 import BeautifulSoup
from jinja2 import Template


def get_url(url):
    directory = "temp"
    subprocess.run(["rm", "-rf", directory], check=True)
    subprocess.run(["mkdir", directory], check=True)
    subprocess.run(["curl", "-LOJ", url], cwd=directory, check=True)

    return glob(f"{directory}/*.zip")[0]


def render_template(soup, url_or_local_file, zip_filename):
    if "https://" not in url_or_local_file:
        url_or_local_file = os.path.abspath(url_or_local_file)

    data = {
        "titles": soup.select(".title"),
        "old_head": soup.find("head").encode_contents().decode('utf8'),
        "old_body_classes": soup.body.get("class", ""),
        "old_body": str(soup.body.decode_contents()),
        "generated_date": datetime.now().isoformat(sep=" ", timespec="minutes"),
        "original_document": url_or_local_file,
        "document_title": Path(zip_filename).stem
    }

    with open("templates/main.j2.html") as f:
        template = Template(f.read())

    html = template.render(**data)

    return html


def fix_tables(soup):
    tables = soup.find_all("table")
    template = Template(open("templates/tables.j2.html").read())

    for table in tables:
        wrapper = template.render(table_html=table.encode_contents().decode('utf8'), table_classes=table.get("class", ""))
        table.replace_with(BeautifulSoup(wrapper, "html.parser"))

def make_tailwindcss():
    subprocess.run(["tailwindcss", "-i", "templates/input.css", "-o", "site/style.css"], check=True)

def massage_url(url):
    # https://docs.google.com/document/d/1GP3hX7KoZTutrrdv9h02oUTdJS-bPJwsG6Gl3_7M3lA/edit?usp=drive_link
    # =>
    # https://docs.google.com/document/u/0/export?format=html&id=$ID&includes_info_params=true&usp=sharing&cros_files=false

    pattern = r"(?<=/d/)([a-zA-Z0-9-_]+)"
    document_id = re.search(pattern, url).group(1)

    export_link = f"https://docs.google.com/document/u/0/export?format=zip&id={document_id}&includes_info_params=true&usp=sharing&cros_files=false"
    return export_link

def main(url_or_local_file):
    output_filename = "site/index.html"

    if os.path.exists(url_or_local_file):
        zip_filename = url_or_local_file
    else:
        # try to fetch the url
        if "export" not in url_or_local_file:
            url_or_local_file = massage_url(url_or_local_file)

        zip_filename = get_url(url_or_local_file)

    print(zip_filename)
    subprocess.run(["rm", "-rf", "site"], check=True)
    subprocess.run(["unzip", zip_filename, "-d", "site"], check=True)
    subprocess.run(["cp", *glob("assets/*"), "site"], check=True)

    html_filename = glob("site/*.html")[0]

    with open(html_filename, "r", encoding="utf-8") as f:
        input_html = f.read()

    make_tailwindcss()

    soup = BeautifulSoup(input_html, "html.parser")
    fix_tables(soup)
    html = render_template(soup, url_or_local_file, zip_filename)

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html)

    print("wrote to site!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url_or_zipfile")
    args = parser.parse_args()
    main(args.url_or_zipfile)
