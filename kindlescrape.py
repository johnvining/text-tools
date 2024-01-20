from lxml import html
from bs4 import BeautifulSoup, Comment
from unidecode import unidecode
import argparse

class Citation:
    def __init__(self):
        self.quote = ""
        self.location = ""
        self.note = ""

    def print_it(self):
        print(unidecode(self.quote + "|" + self.location[self.location.index("|") + 2:] + "|" + self.note))


parser = argparse.ArgumentParser("kindle_scrape")
parser.add_argument("input_file", help="HTML file to parse")
args = parser.parse_args()
input_file = args.input_file

with open(input_file, "r") as f:
    page = f.read()

soup = BeautifulSoup(page, "lxml")

# Start looking for notes after this comment
start = None
for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
    if comment in [u' Star, if necessary ']:
        start = comment
        break

citation_list = []

cont = True
while cont:
    citation = Citation()

    location = start.find_next(id="annotationNoteHeader")
    if location is None:
        cont = False
        break

    citation.location = location.contents[0]

    span = location.find_next(id="highlight")
    citation.quote=span.contents[0]

    note = span.find_next(id="note")
    if len(note) > 0:
        citation.note=note.contents[0]

    citation_list.append(citation)

    start = location


for citation in citation_list:
    citation.print_it()



