import os
import datetime
import re
import uuid

papersDirectory = os.path.expandvars('$PAPERSDIR')+'/'
includeTags = False   # tags are still a work in progress

def getTags(filename):
	tagData = subprocess.Popen(["xattr -p com.apple.metadata:_kMDItemUserTags "+filename.replace(" ","\ ")+"|xxd -r -p |plutil -convert xml1 - -o -"],stdout=subprocess.PIPE,shell=True)
	(out, err) = tagData.communicate()
	if not "NULL" in out:
		return out
	else:
		return ''
			
def getDOI(filename):
	'''Scans the text of the given PDF file for a DOI number
	or arXiv number'''
	tempFilename = 'tmp'+str(uuid.uuid4())+'.txt'
	os.system('pdftotext -q -f 1 -l 1 '+filename.replace(" ","\ ")+' '+tempFilename)
	f = open(tempFilename, 'r')
	matches = re.findall(r'(doi|DOI|arXiv): ?([^\s]+)\s', f.read())
	f.close()
	doiString = ''
	doiLabel = ''
	for match in matches:
		if match[0] == 'arXiv':
			doiString = 'https://arxiv.org/abs/'+match[1]
			doiLabel = 'arXiv'
		else:
			doiString = 'https://doi.org/'+match[1]
			doiLabel = 'doi'
	return doiString,doiLabel

def getPaperInfo(filename):
	author, year, title = filename[:-4].split('_')[:3]
	fullFilename = papersDirectory+filename
	date = datetime.datetime.fromtimestamp(os.path.getmtime(fullFilename))
	doiString, doiLabel = getDOI(fullFilename)
	if includeTags: 
		tag = getTags(fullFilename)
	else:
		tag = ''
	return (author, year, title, fullFilename,  
			str(date), os.path.getsize(fullFilename), tag,
			doiString, doiLabel)
			