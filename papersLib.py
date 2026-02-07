import os
import datetime
import re
import uuid
import subprocess

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
    try:
        subprocess.run(["pdftotext","-q","-enc", "UTF-8","-f","1","-l", "1",
            filename, tempFilename], check=True)
    except subprocess.CalledProcessError:
        return None, None
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
    fields = filename[:-4].split('_')
    if len(fields) == 4:
        author, author2, year, title = fields[:4]
    elif len(fields) == 2:
        author, title = fields[:2]
        author2, year = '',''
    elif len(fields) == 3:
        author, year, title = fields[:3]
        author2 = ''
    else:
        title = filename
        author, author2, year = '','',''
    fullFilename = papersDirectory+filename
    size = os.path.getsize(fullFilename)
    date = datetime.datetime.fromtimestamp(os.path.getmtime(fullFilename))
    date_str = date.strftime("%Y-%m-%d %H:%M:%S")
    doiString, doiLabel = getDOI(fullFilename)
    if includeTags: 
        tag = getTags(fullFilename)
    else:
        tag = ''
    return (author, author2, year, title, fullFilename,  
            date_str, size, tag,
            doiString, doiLabel)
            