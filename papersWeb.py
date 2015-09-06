import os
import datetime
import time

papersDirectory = os.path.expandvars('$PAPERSDIR')+'/'

start = time.time()

authors=[]
years=[]
titles=[]
dates=[]
filenames=[]
sizes=[]

for filename in os.listdir(papersDirectory):
	if filename[0] != '.':
		#print(os.path.join(dirname, filename))
		data = filename.split('_')
		author = data[0]
		year = data[1]
		title = data[2]
		authors.append(author)
		years.append(year)
		titles.append(title.split('.')[0])   # removes the .pdf from the filename
		filenames.append(papersDirectory+filename)
		date = datetime.datetime.fromtimestamp(os.path.getmtime(papersDirectory+filename))
		dates.append(str(date))
		sizes.append(os.path.getsize(papersDirectory+filename))

print('''<HTML>
  <HEAD>
    <LINK href="papersWeb.css" rel="stylesheet" type="text/css">
<script src="sorttable.js"></script>
</head>
<body>''')

print('| <a href="http://adsabs.harvard.edu/abstract_service.html" target="_blank">ADS</a> ')
print('| <a href="file://'+papersDirectory+'.DS_Store">Finder</a> ')
print('|')	
		
print('<table style="width:100\%" class="sortable"')
print('<tr><th style="width:8em">Author</th><th style="width:4em">Year</th><th>Title</th><th>Date added</th></tr>')

for author,year,title,filename,date in zip(authors,years,titles,filenames,dates):
	print("<tr>")
	print("<td>"+author+"</td>")
	print("<td>"+year+"</td>")
	print('<td><a href="'+filename+'" target="_blank">'+title+'</a></td>')	
	print("<td>"+date+"</td>")
	print("</tr>")
	
print('</table>')

totalSize = sum(sizes)

stop = time.time()
#print('<br><hr>')
#print('<p><small>%d papers in %g seconds</small></p>' % (len(authors),stop-start))

print('<br><small>Stats: %d papers %.3g MB %.3g ms</small>' % (len(authors),totalSize/1e6,1000.0*(stop-start)))

print('''
</body>
</html>''')
