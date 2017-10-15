from Porter import PorterStemmer
from krovetzstemmer import Stemmer

from common import readTextFromFile
from common import getTextFromHTML

krov = Stemmer()


f =	'en/articles/d/o/r/Dorothy_Block_a8f8.html'
text = getTextFromHTML( readTextFromFile(f) )

print 'ori:\n', text, '\n'
print 'porter:\n', PorterStemmer.useStemer(text), '\n'
print 'krov:\n', krov.stem(text), '\n'