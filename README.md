
The script `papersWeb.py` looks in the directory `$PAPERSDIR` for PDF files.
Set this e.g. in your `.bashrc` using 
`export PAPERSDIR='/Users/cumming/Dropbox/Papers'`

The filenames should have the format 
`<first author>_<year>_<title>.pdf`

The following lines create an alias 'papers' that will open a Safari window with the list of papers:

`export PAPERSWEB='/Users/cumming/Dropbox/papersWeb'`

`alias papers='python $PAPERSWEB/papersWeb.py > $PAPERSWEB/papersWeb.html; open -a Safari $PAPERSWEB/papersWeb.html'`

Uses `list.js` from
`http://www.listjs.com`

Extracts DOI's from PDF files using `pdftotext` from
`http://www.foolabs.com/xpdf/home.html`
