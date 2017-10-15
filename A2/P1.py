#!/usr/bin/env python

import sys

def genInverted(fileDict):

	vocab = set()
	for filename, content in fileDict.items():
		
		f = content # 'Alexandre Desplat is a musical composer of the grand budapest hotel'
		f = f.lower() #'alexandre desplat is a musical composer of the grand budapest hotel'
		f = f.split() # ['alexandre, desplat ,is ,a ,musical ,composer ,of ,the ,grand ,budapest ,hotel]
		f = set(f)#{'alexandre, desplat ,is ,a ,musical ,composer ,of ,the ,grand ,budapest ,hotel}

		fileDict[filename] = f
		vocab = vocab.union(f)

	invertedFileDict = {}
	for word in vocab:

		invertedFileDict[word] = []
		for filename, content in fileDict.items():

			if( word in fileDict[filename] ):
				invertedFileDict[word].append(filename)

	return invertedFileDict

def main(filenames):

	fileDict = {}

	try:
		
		for f in filenames:
			f = f.strip()
			
			infile = open(f, 'r')
			fileDict[f] = infile.read()
			infile.close()

	except Exception as e:
		print('File error:', e)

	invertedFileDict = genInverted(fileDict)

	print('Inverted index of files:', filenames, '\n')
	for vocab, files in invertedFileDict.items():
		print(vocab, files)
	print()

if __name__ == "__main__":

	if( len(sys.argv) > 1 ):
		main( sys.argv[1:] )
	else:
		print('Invalid use: no parameters given')
