from lxml import html
from bs4 import BeautifulSoup, Comment
import argparse
import csv

class Citation:
    def __init__(self):
        self.quote = ""
        self.location = ""
        self.note = ""
        self.work = ""

    def to_csv_list(self):
        # Why this order?
        # https://github.com/johnvining/commonplace/blob/af0e7ddccad5efba88c5bd2abcac4002644b06ca/server/src/cli/import.js#L97
        note_location = self.location[self.location.index("|") + 2:]
        note_location = note_location.replace(u'\xa0', u' ')
        return ["","",self.quote,self.work,"","","","","",note_location,self.note]


parser = argparse.ArgumentParser("kindle_scrape")
parser.add_argument("input_file", help="HTML file to parse")
parser.add_argument("work_name", help="Name of the book")
args = parser.parse_args()
input_file = args.input_file
output_file = input_file.replace('.html', '-extracted.csv')

with open(input_file, "r") as f:
    page = f.read()

soup = BeautifulSoup(page, "lxml")

# Start looking for notes after this comment
start = None
for comment in soup.findAll(string=lambda text: isinstance(text, Comment)):
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
    citation.work = args.work_name

    span = location.find_next(id="highlight")
    citation.quote=span.contents[0]

    note = span.find_next(id="note")
    if len(note) > 0:
        citation.note=note.contents[0]

    citation_list.append(citation)

    start = location

with open(output_file, "x") as f:
    csv_writer = csv.writer(f)
    for citation in citation_list:
        csv_writer.writerow(citation.to_csv_list())

print(str(len(citation_list)) + " lines printed")