#!/usr/bin/env python3
import argparse
import tempfile
from bs4 import BeautifulSoup, Tag
import os
import subprocess


def get_url(url, outfile):
    subprocess.run(["curl", "-L", url, "-o", outfile], check=True)


# Generate sidebar
def make_sidebar(soup):
    # Find all elements with class 'title'
    titles = soup.select(".title")

    # Create the sidebar HTML as a string
    sidebar = soup.new_tag(
        "nav",
        **{
            "id": "hamburgerMenu",
            "class": "fixed top-0 left-0 w-2/3 md:w-auto h-full bg-gray-800 text-white shadow-lg transform -translate-x-full transition-transform duration-300 md:static md:translate-x-0 font-inter overflow-y-scroll left-0 top-0 bg-white py-3 px-4 shadow-lg rounded-lg h-full z-20 flex-shrink-0",
        },
    )
    ul = soup.new_tag("ul")

    for title in titles:
        li = soup.new_tag("li")
        a = soup.new_tag(
            "a",
            href=f"#{title.get('id')}",
            **{"class": "md:text-lg hover:bg-blue-200 py-1 px-4 rounded w-full block"},
        )
        a.string = title.get_text(strip=True)
        li.append(a)
        ul.append(li)

    sidebar.append(ul)

    # Wrap tables in a scrollable div.
    tables = soup.find_all("table")
    for table in tables:
        wrapper = soup.new_tag(
            "div", **{"class": "border border-black/50 overflow-x-auto max-w-full"}
        )
        # make sure tables won't linebreak
        table["class"].append("whitespace-nowrap")
        table.replace_with(wrapper)
        wrapper.append(table)

    # Restructure body content
    old_body_classes = soup.body.get("class", "")
    old_body_content = str(soup.body.decode_contents())

    # Add sidebar and restructure body
    soup.body.clear()
    soup.body["class"] = "flex bg-black md:bg-gray-800"
    soup.body.append(sidebar)

    new_content_div = soup.new_tag(
        "div",
        **{
            "class": f"{' '.join(old_body_classes)} max-w-screen-lg overflow-x-hidden transition-opacity px-6 pt-16",
            "id": "mainContent",
        },
    )
    new_content_div.append(BeautifulSoup(old_body_content, "html.parser"))
    soup.body.append(new_content_div)


def embed_css(soup, css_filename):
    with open(css_filename) as f:
        css = f.read()

    style_tag = soup.new_tag("style", type="text/css")
    style_tag.string = css

    link_1 = soup.new_tag("link", rel="preconnect", href="https://fonts.googleapis.com")
    link_2 = soup.new_tag(
        "link", rel="preconnect", href="https://fonts.gstatic.com", crossorigin=True
    )
    link_3 = soup.new_tag(
        "link",
        href="https://fonts.googleapis.com/css2?family=Inter:wght@500&display=swap",
        rel="stylesheet",
    )

    soup.head.append(link_1)
    soup.head.append(link_2)
    soup.head.append(link_3)

    hamburger_script = open("hamburger.js").read()

    soup.head.append(
        BeautifulSoup(f"<script>{hamburger_script}</script>", "html.parser")
    )

    soup.body.append(
        BeautifulSoup(
            """
      <button
        id="hamburgerButton"
        class="fixed top-4 left-4 z-10 px-3 py-2 bg-gray-800 text-white rounded-md md:hidden text-2xl leading-8">
        ☰
        </button>
    """,
            "html.parser",
        )
    )

    meta_tag = soup.new_tag(
        "meta",
        attrs={"name": "viewport", "content": "width=device-width, initial-scale=1"},
    )
    soup.head.append(meta_tag)


def main(url, output_filename):
    with tempfile.TemporaryDirectory() as tmpdir:
        html_filename = tmpdir + "/original.html"
        get_url(url, html_filename)

        with open(html_filename, "r", encoding="utf-8") as f:
            input_html = f.read()

    # with open("a.html", "r", encoding="utf-8") as f:
    #     input_html = f.read()

    soup = BeautifulSoup(input_html, "html.parser")
    make_sidebar(soup)

    embed_css(soup, "style.css")

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(soup.prettify())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", default="out.html")
    parser.add_argument("url")
    args = parser.parse_args()
    main(
        args.url,
        args.output,
    )
