
__author__="Harshit.Kashiv"

'''
Provides various utility functions
Added cleanTokenWithoutComma

'''
from HTMLParser import HTMLParser
import string
import unicodedata, re
import collections

def handleNumericFieldsNULLs(s):
	if s is None:
		return -999999
	else:
		return s

def removeN(s):
	#pprint({'s': s})
	if s.strip().lower() == 'n':
		s = ' '
	
	return s

def getASCIIString(s):
	#Changed for null thingy on 11/11
	#Changed for | and \n and \r on 11/18
		
	if s is not None:
		s = s.replace('|', ' ').replace('\n', ' ').replace('\r',' ')
		return filter(lambda x: x in string.printable, s)
	else:
		return ' '

def getASCIIStringNoneHandled(s):
	#Changed for null thingy on 11/11
	#Changed for | and \n and \r on 11/18
		
	if s is not None:
		s = s.replace('|', ' ').replace('\n', ' ').replace('\r',' ')
		return filter(lambda x: x in string.printable, s)
	else:
		return ' '

def removeJunkChars(s):
	all_chars = (unichr(i) for i in xrange(0x110000))
	#control_chars = ''.join(c for c in all_chars if unicodedata.category(c) == 'Cc')
	# or equivalently and much more efficiently
	control_chars = ''.join(map(unichr, range(0,32) + range(127,160)))

	control_char_re = re.compile('[%s]' % re.escape(control_chars))

	return control_char_re.sub(' ', s)

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

def strip_tags(html):
	MLS = MLStripper()
	try:
		MLS.feed(html)
		return MLS.get_data()
	except:
		return html

def commaSplitter(s):
	#Split on comma and ignore NoneType Error
	if s is None:
		return []
	else:
		return s.split(',')


def myfloat(s):
	#If s is blank return -1 else return float(s)
	if s is '':
		return float(-1)
	else:
		return float(s)

def cleanToken(token):
    alphaPattern=re.compile('[^a-zA-Z0-9 \.\+#&]')
    toBeRemovedPattern=re.compile('([0-9]+[\.][0-9]+)|([ ][0-9]+[ ])|([ ][\+]+[ ])|([ ][\+]+)|([ ][#]+[ ])|([ ][#]+)|([\.][ ])|([ ][0-9]+\Z)|([0-9]+[\+])|(\A[0-9]+[.])')
    
    multSpacePattern=re.compile('[ ]+')

    token=re.sub(alphaPattern,' ',token)

    #deliberately done twice for thorough cleaning :-)
    token=re.sub(toBeRemovedPattern,' ',token)
    token=re.sub(toBeRemovedPattern,' ',token)
    token = multSpacePattern.sub(' ',token).strip().lower()

    return token

def cleanTokenWithoutComma(token):
    alphaPattern=re.compile('[^a-zA-Z0-9 \.\+#&,]')
    toBeRemovedPattern=re.compile('([0-9]+[\.][0-9]+)|([ ][0-9]+[ ])|([ ][\+]+[ ])|([ ][\+]+)|([ ][#]+[ ])|([ ][#]+)|([\.][ ])|([ ][0-9]+\Z)|([0-9]+[\+])|(\A[0-9]+[.])')
    
    multSpacePattern=re.compile('[ ]+')

    token=re.sub(alphaPattern,' ',token)

    #deliberately done twice for thorough cleaning :-)
    token=re.sub(toBeRemovedPattern,' ',token)
    token=re.sub(toBeRemovedPattern,' ',token)
    token = multSpacePattern.sub(' ',token).strip().lower()

    return token


def removeNonAscii(str): return "".join(i for i in str if ord(i)<128)

def removeNonAscii_replace_alt(str, alternate_char = " "): 
    
    new_str = ""
    
    for ch in str:
        if ord(ch) < 128:
            new_str += ch
        else:
            new_str += alternate_char
    
    return new_str


def clean_text(unclean_text):
    """
    This cleans up text in terms of allowing only ascii characters.
    It also converts it to string.
    """
    return str(removeNonAscii_replace_alt(unclean_text, alternate_char = " "))

def dedupeListWithSorting(L, key):
	"""
	This function reverse sorts and dedupes a list based on a column preserving order
	"""
	mydict = {} #Ordered dict would have been better here as per performance but is availaible for python2.7+ only
	for v in sorted(L, key=lambda L: L[1], reverse = True): # where L is your list
		mydict[v[1]] = v
	
	print mydict

	#Sort mydict based on keys -> reverse
	mydict2 = {}
	s = sorted(mydict.keys(), reverse = True)

	result = []
	for key in s:
		result.append(mydict[key])
	
	return result


def dedupeList(L, columnNum = 1):
	"""
	This function sorts and dedupes a list based on a column
	"""
	mydict = {} #Ordered dict would have been better here as per performance but is availaible for python2.7+ only
	for v in L: # where L is your list
		mydict[v[columnNum]] = v
	
	#Sort mydict based on keys -> reverse
	mydict2 = {}
	s = sorted(mydict.keys(), reverse = True)

	result = []
	for key in s:
		result.append(mydict[key])
	
	return result

if __name__ == '__main__':
	s='1,2,3'
	#s='1,2,None'
	#s='None'

	#print commaSplitter(s)
	#a = [22,3,3,4,5,6,554]
	#print a
	#print dedupeList(a)

	L =  [(1,22),(2,3),(3,3),(4,4),(5,5),(6,6),(7,554)]

	print L
	#Use a lambda function to indicate the key of sorting = column1
	print dedupeList(L, columnNum = 1)
	print getASCIIString("Fann Wong &amp; Christopher Lee's ROM")
	