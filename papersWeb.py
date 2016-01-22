#!/anaconda/bin/python
import time
import subprocess
import re
from papersLib import *
from multiprocessing import Pool

start = time.time()

filenames = [name for name in os.listdir(papersDirectory) if '.pdf' in name]
pool = Pool(processes=8)
papers = pool.map(getPaperInfo,filenames)
os.system('rm tmp*.txt')
stop = time.time()
			
# page header
print('''<HTML>
  <HEAD>
  	<TITLE>Papers</TITLE>
    <LINK href="papersWeb.css" rel="stylesheet" type="text/css">
</head>
<body>''')

#<script src="sorttable.js"></script>



print('<div id="papers">')

# links at the top of the table
print('<div class="links">')
print('<a href="http://adsabs.harvard.edu/abstract_service.html" target="_blank">ADS</a> | ')
print('<a href="file://'+papersDirectory+'.DS_Store">Finder</a>')

print('</div>')
	
print('''<input class="search" placeholder="Search" />
  <button class="sort" data-sort="author">
  	Author
  	</button>
  <button class="sort" data-sort="year">
    Year
  </button>
    <button class="sort" data-sort="date">
  	Date added
  	</button>
  ''')
		
# table header row
print('<table>') # style="width:100\%" class="sortable">')

#print('<thead>')
#print('<tr><th style="width:8em">Author</th><th style="width:4em">Year</th><th>Title</th><th>Date added</th>')
#if includeTags:
#	print('<th>Tags</th>')
#print('</tr>')
#print('</thead>')


print('<tbody class="list">')



totalSize = 0.0
for author,author2,year,title,filename,date,size,tag,doiString,doiLabel in papers:
	print("<tr>")
	print('<td class="author">'+author)
	if author2 != '':
		print("& "+author2)
	print("</td>")
	
	print('<td class="year">'+year+'</td>')
	if len(title) > 50:
		title = title[:47]+'...'
	print('<td class="title"><a href="'+filename+'" target="_blank">'+title+'</a></td>')	
	print('<td class="date">'+date+"</td>")
	totalSize += size
	if includeTags:
		print('<td>')
		tagCount = 0
		for oneTag in tag.split('0'):
			if tagCount > 1:
				print(',')
			print(oneTag)
			tagCount+=1
		print('</td>')

	print('<td><a href="http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?author=^'+author+'&end_year='+year+'&start_year='+year+'&jou_pick=NO" target="_blank">ADS</a></td>')	

	if doiString != '':
		print('<td><a href="'+doiString+'" target="_blank">'+doiLabel+'</a></td>')	
	
	print('</tr>')	

print('''</tbody></table></div>
<script src="list.js"></script>
<script src="papersWeb.js"></script>''')

print('<br><small>Stats: %d papers %.3g MB %.3g s</small>' % (len(papers),totalSize/1e6,(stop-start)))


print('''
</body>
</html>''')



# Sample ADS search to show the fields:	#http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?db_key=AST&db_key=PHY&db_key=PRE&qform=AST&arxiv_sel=astro-ph&arxiv_sel=cond-mat&arxiv_sel=cs&arxiv_sel=gr-qc&arxiv_sel=hep-ex&arxiv_sel=hep-lat&arxiv_sel=hep-ph&arxiv_sel=hep-th&arxiv_sel=math&arxiv_sel=math-ph&arxiv_sel=nlin&arxiv_sel=nucl-ex&arxiv_sel=nucl-th&arxiv_sel=physics&arxiv_sel=quant-ph&arxiv_sel=q-bio&sim_query=YES&ned_query=YES&adsobj_query=YES&aut_logic=OR&obj_logic=OR&author=%5Eschatz&object=&start_mon=&start_year=&end_mon=&end_year=1999&ttl_logic=OR&title=&txt_logic=OR&text=&nr_to_return=200&start_nr=1&jou_pick=ALL&ref_stems=&data_and=ALL&group_and=ALL&start_entry_day=&start_entry_mon=&start_entry_year=&end_entry_day=&end_entry_mon=&end_entry_year=&min_score=&sort=SCORE&data_type=SHORT&aut_syn=YES&ttl_syn=YES&txt_syn=YES&aut_wt=1.0&obj_wt=1.0&ttl_wt=0.3&txt_wt=3.0&aut_wgt=YES&obj_wgt=YES&ttl_wgt=YES&txt_wgt=YES&ttl_sco=YES&txt_sco=YES&version=1
		#http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?db_key=AST&db_key=PRE&qform=AST&arxiv_sel=astro-ph&arxiv_sel=cond-mat&arxiv_sel=cs&arxiv_sel=gr-qc&arxiv_sel=hep-ex&arxiv_sel=hep-lat&arxiv_sel=hep-ph&arxiv_sel=hep-th&arxiv_sel=math&arxiv_sel=math-ph&arxiv_sel=nlin&arxiv_sel=nucl-ex&arxiv_sel=nucl-th&arxiv_sel=physics&arxiv_sel=quant-ph&arxiv_sel=q-bio&sim_query=YES&ned_query=YES&adsobj_query=YES&aut_logic=OR&obj_logic=OR&author=%5Eackerman&object=&start_mon=&start_year=2001&end_mon=&end_year=2001&ttl_logic=OR&title=&txt_logic=OR&text=&nr_to_return=200&start_nr=1&jou_pick=NO&ref_stems=&data_and=ALL&group_and=ALL&start_entry_day=&start_entry_mon=&start_entry_year=&end_entry_day=&end_entry_mon=&end_entry_year=&min_score=&sort=SCORE&data_type=SHORT&aut_syn=YES&ttl_syn=YES&txt_syn=YES&aut_wt=1.0&obj_wt=1.0&ttl_wt=0.3&txt_wt=3.0&aut_wgt=YES&obj_wgt=YES&ttl_wgt=YES&txt_wgt=YES&ttl_sco=YES&txt_sco=YES&version=1
	
#DOI weblink:
#https://doi.org/<DOI>
	
