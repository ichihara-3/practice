import argparse
import difflib
import sys

from bs4 import BeautifulSoup
from bs4.element import Tag
from colored import Back, Fore, Style


def remove_tags(soup: BeautifulSoup, tags: list[str]):
    for tag in tags:
        for e in soup.css.iselect(tag):
            e.decompose()


def replace_tags(soup: BeautifulSoup, replaces: dict[str, str]):
    for src, dst in replaces.items():
        for e in soup.css.iselect(src):
            e.wrap(soup.new_tag(dst))
            e.unwrap()


def remove_attrs(soup: BeautifulSoup, ignore: list[str]):
    for e in soup.find('html').descendants:
        if isinstance(e, Tag):
            attrs = list(e.attrs.keys())
            for key in attrs:
                if key in ignore:
                    continue
                del e[key]
        else:
            continue


def compare(html1: str, html2: str) -> list[str]:
    def _split(x: str) -> list[str]:
        return x.splitlines(keepends=True)

    diffs = difflib.unified_diff(_split(html1), _split(html2))
    return list(diffs)


def readfile(path: str):
    with open(path) as f:
        data = f.read()
    return data


def colorize(line: str) -> str:
    if sys.stdout.isatty():
        if line.startswith("+"):
            return f"{Fore.green}{Back.black}{line}{Style.reset}"
        if line.startswith("-"):
            return f"{Fore.red}{Back.black}{line}{Style.reset}"
        if line == "PASS":
            return f"{Fore.green}{Back.black}PASS{Style.reset}"
    return line


def printdiff(result: list[str]):
    if not result:
        print(colorize("PASS"))
    else:
        print("".join(map(colorize, result)))


def preprocess(soup: BeautifulSoup):
    remove_tags(soup, ["script"])
    replace_tags(soup, {"font": "span"})
    remove_attrs(soup, [])
    return soup


def main():
    parser = argparse.ArgumentParser(description="Compare two HTML files")
    parser.add_argument("file1", help="First file to compare", nargs="?", default="sample1.html")
    parser.add_argument("file2", help="Second file to compare", nargs="?", default="sample2.html")
    args = parser.parse_args()

    html1 = readfile(args.file1)
    html2 = readfile(args.file2)

    soup1 = preprocess(BeautifulSoup(html1, "lxml"))
    soup2 = preprocess(BeautifulSoup(html2, "lxml"))

    printdiff(compare(soup1.prettify(formatter="html"), soup2.prettify(formatter="html")))


if __name__ == "__main__":
    main()
