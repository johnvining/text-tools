# text-tools
## Kindle Scrape

This takes an html file saved from the Kindle web interface and saves it as a CSV. The columns are order to be loaded in to [Commonplace](https://github.com/johnvining/commonplace/blob/af0e7ddccad5efba88c5bd2abcac4002644b06ca/server/src/cli/import.js#L97), but this can be modified easily! Let me know if this would be useful to you and I'm happy to help.

To run: 
- Start the virtual env: `source text-tools-venv/bin/activate`
- Run the script: `python3 kindlescrape.py '/path/to/savedFiled.html' 'Your Book Title'`

Reference:
- Writing requirements to text: `pip freeze > requirements.txt`
