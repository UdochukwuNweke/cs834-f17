'''
4.8

'''

import glob

from common import genericErrorInfo
from common import derefURL
from common import readTextFromFile
from common import dumpJsonToFile
from common import getDictFromFile

from bs4 import BeautifulSoup
from urllib.parse import unquote

def getHTMLPaths():

	pathnames = []

	try:
		infile = open('wiki-small-html-files.txt', 'r')
		pathnames = infile.readlines()
		infile.close()
	except:
		genericErrorInfo()

	return pathnames

def getHTMLFilename(wiki):

	wiki = wiki.strip()
	wiki = wiki.split('.html')[0]
	wiki = wiki.split('/')[-1].strip().lower()

	return wiki

def getHTMLFilenames(pathnames):

	filenames = []
	for path in pathnames:
		path = getHTMLFilename(path)
		filenames.append(path)
	
	return filenames

def storeHTMLFiles_single_use():

	outfile = open('wiki-small-html-files.txt', 'w')

	counter = 0
	for filename in glob.iglob('en/**/*.html', recursive=True):
		outfile.write(filename + '\n')
		counter += 1

	outfile.close()


def getWikiOutlinks(sourcewiki, html, outlinksDict):

	if( len(html) == 0 ):
		return outlinksDict

	try:
		soup = BeautifulSoup(html, 'html.parser')
		anchorTags = soup.find_all('a')
		
		for tag in anchorTags:
			
			if( tag.has_attr('href') == False ):
				continue

			if( tag['href'].find('wikipedia') == -1 ):
				continue

			link = tag['href']
			link = unquote(link)
			
			outlinksDict.setdefault(link, 0)
			outlinksDict[link] += 1
					
	except:
		genericErrorInfo()

	return outlinksDict


def getTopKPages(pathnames, filenames):

	if( len(pathnames) == 0 ):
		return []

	outlinksDict = {}

	for i in range(len(pathnames)):
		wiki = pathnames[i]
		wiki = wiki.strip()
		html = readTextFromFile(wiki)

		if( i % 100 == 0 ):
			print(i, 'of', len(pathnames), 'wiki file:', wiki)
			print('\tlen:', len(outlinksDict))

		sourcewiki = getHTMLFilename(wiki)
		getWikiOutlinks(sourcewiki, html, outlinksDict)

		#if( i == 3 ):
		#	break

	dumpJsonToFile('./outlinksDict.json', outlinksDict)

def getTopKFromDict(k):

	print('\n'*2)
	print('top', k)
	if( k<1 ):
		return

	outlinksDict = getDictFromFile('./outlinksDict.json')
	result = sorted(outlinksDict.items(), key=lambda x: x[1], reverse=True)

	for i in range(len(result)):
		print(i+1, result[i])

		if( i == k-1 ):
			break


def main():
	#pathnames = getHTMLPaths()
	##filenames = getHTMLFilenames(pathnames)
	#getTopKPages(pathnames, filenames)

	getTopKFromDict(30)

if __name__ == '__main__':
    main()