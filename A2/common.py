import os, sys
import json
from subprocess import check_output

import justext

def getTextFromHTML(html):

	

	paragraphs = justext.justext(html, justext.get_stoplist("English"))
	text = ''

	for paragraph in paragraphs:
		if not paragraph.is_boilerplate:
			text += paragraph.text

	return text

def genericErrorInfo():
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	errorMessage = fname + ', ' + str(exc_tb.tb_lineno)  + ', ' + str(sys.exc_info())
	print('\tERROR:', errorMessage)

def readTextFromFile(infilename):

	text = ''
	
	try:
		infile = open(infilename, 'r')
		text = infile.read()
		infile.close()
	except:
		genericErrorInfo()

	return text

def derefURL(url):

	url = url.strip()
	if( len(url) == 0 ):
		return ''

	try:
		output = check_output(['curl', '--silent', '-m', '10', url])
		output = output.decode('utf-8')
	except:
		genericErrorInfo()

	return output

def dumpJsonToFile(outfilename, dictToWrite, indentFlag=True):

	try:
		outfile = open(outfilename, 'w')
		
		if( indentFlag ):
			json.dump(dictToWrite, outfile, ensure_ascii=False, indent=4)#by default, ensure_ascii=True, and this will cause  all non-ASCII characters in the output are escaped with \uXXXX sequences, and the result is a str instance consisting of ASCII characters only. Since in python 3 all strings are unicode by default, forcing ascii is unecessary
		else:
			json.dump(dictToWrite, outfile, ensure_ascii=False)

		outfile.close()

		print('\twriteTextToFile(), wrote:', outfilename)
	except:
		genericErrorInfo()

def getDictFromJson(jsonStr):

	try:
		return json.loads(jsonStr)
	except:
		genericErrorInfo

	return {}

def getDictFromFile(filename):

	try:
		return getDictFromJson( readTextFromFile(filename) )
	except:
		genericErrorInfo()

	return {}