#!/anaconda/bin/python
import time
import subprocess
import re
import os
from multiprocessing import Pool

from papersLib import *

def main():
    start = time.time()

    filenames = [name for name in os.listdir(papersDirectory)
                 if name.lower().endswith('.pdf')]

    with Pool(processes=8) as pool:
        papers = pool.map(getPaperInfo, filenames)

    os.system('rm -f tmp*.txt')

    stop = time.time()

    # ---------------- HTML OUTPUT ---------------- #

    print('''<HTML>
  <HEAD>
    <TITLE>Papers</TITLE>
    <LINK href="papersWeb.css" rel="stylesheet" type="text/css">
  </HEAD>
  <BODY>''')

    print('<div id="papers">')

    print('<div class="links">')
    print('<a href="https://ui.adsabs.harvard.edu" target="_blank">ADS</a> | ')
    print('<a href="file://' + papersDirectory + '">Finder</a>')
    print('</div>')

    print('''<input class="search" placeholder="Search" />
  <button class="sort" data-sort="author">Author</button>
  <button class="sort" data-sort="year">Year</button>
  <button class="sort" data-sort="date">Date added</button>
''')

    print('<table>')
    print('<tbody class="list">')

    totalSize = 0.0

    for (author, author2, year, title, filename,
         date, size, tag, doiString, doiLabel) in papers:

        print("<tr>")
        print('<td class="author">' + author)
        if author2:
            print(" & " + author2)
        print("</td>")

        print('<td class="year">' + year + '</td>')

        if len(title) > 50:
            title = title[:47] + '...'

        print('<td class="title"><a href="' + filename +
              '" target="_blank">' + title + '</a></td>')
        print('<td class="date">' + date + "</td>")

        totalSize += size

        if includeTags:
            print('<td>')
            print(', '.join(tag.split('0')))
            print('</td>')

        print('<td><a href="http://adsabs.harvard.edu/cgi-bin/nph-abs_connect'
              '?author=^' + author +
              '&end_year=' + year +
              '&start_year=' + year +
              '&jou_pick=NO" target="_blank">ADS</a></td>')

        if doiString:
            print('<td><a href="' + doiString +
                  '" target="_blank">' + doiLabel + '</a></td>')

        print('</tr>')

    print('''</tbody></table></div>
<script src="list.js"></script>
<script src="papersWeb.js"></script>''')

    print('<br><small>Stats: %d papers; %.4g MB; %.3g s</small>' %
          (len(papers), totalSize / 1e6, (stop - start)))

    print('</body></html>')


if __name__ == "__main__":
    main()
