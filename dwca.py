import zipfile
from xml.dom import minidom

class MappingError(Exception):
	def __init__(self,value):
		self.value=value
	def __str__(self):
		return repr(self.value)

def typeChecker(type1, type2, position):
	if type(type1) != type(type2):
		errorMsg = 'The '+position+' argument must be '+str(type(type2))
		raise MappingError(errorMsg)

def openDwca(dwca_path):

	try:
		f = open(dwca_path,'r')
	except IOError as e:
		raise MappingError('File does not exist')
	
	try:
		z = zipfile.ZipFile(f)
	except zipfile.BadZipfile as e:
		raise MappingError('Not an IPT file. IPT DwC-A are zip files')
		
	dwcacontent = z.read('occurrence.txt').split('\n')
	z.close()
	f.close()
	
	if dwcacontent[-1] == '':
		dwcacontent = dwcacontent[:-1]
	
	return dwcacontent

def headersDwca(dwcacontent):
	headerline = dwcacontent[0]
	colnames = headerline.split('\t')
	datalines = dwcacontent[1:]
	
	return colnames,datalines

def readDwca2list(colnames,datalines):
	
	dwcalist = []

	for line in datalines:
		dwcaline = {}
		splitline = line.split('\t')
	
		for cont in range(len(splitline)):
			thisheader = colnames[cont]
			thisvalue = splitline[cont]
			dwcaline[thisheader] = thisvalue
	
		dwcalist.append(dwcaline)

	return dwcalist

def readDwca2tuple(colnames,datalines):
	
	#dwcatuple = ()

	#for line in datalines:
	#	dwcaline = {}
	#	splitline = line.split('\t')
	#
	#	for cont in range(len(splitline)):
	#		thisheader = colnames[cont]
	#		thisvalue = splitline[cont]
	#		dwcaline[thisheader] = thisvalue
	#
	#	dwcatuple = dwcatuple + (dwcaline,)
	
	dwcalist = readDwca2list(colnames,datalines)
	dwcatuple = tuple(dwcalist)
	
	return dwcatuple

def dwca2list(dwca_path):
	dwcacontent = openDwca(dwca_path)
	colnames,datalines = headersDwca(dwcacontent)
	dwca = readDwca2list(colnames,datalines)
	return dwca

def dwca2tuple(dwca_path):
	dwcacontent = openDwca(dwca_path)
	colnames,datalines = headersDwca(dwcacontent)
	dwca = readDwca2tuple(colnames,datalines)
	return dwca

def meta2dict(dwca_path):
	
	try:
		f = open(dwca_path,'r')
	except IOError as e:
		raise MappingError('File does not exist')
	
	try:
		z = zipfile.ZipFile(f)
	except zipfile.BadZipfile as e:
		raise MappingError('Not an IPT file. IPT DwC-A are zip files')
	
	metadata = {}
	
	emlcontent = z.read('eml.xml')
	eml = minidom.parseString(emlcontent)
	
	# Title
	try:
		title = eml.getElementsByTagName('title')[0].firstChild.data
	except IndexError:
		title = ''
	metadata['title'] = title
	
	# UUID
	UUID = eml.firstChild.attributes['packageId'].value.split('/')[0]
	if UUID == 'http:':
		UUID = ''
	metadata['UUID'] = UUID
	
	# Citation
	try:
		citation = eml.getElementsByTagName('citation')[0].firstChild.data
	except IndexError:
		citation = ''
	metadata['citation'] = citation
	
	# DateStamp
	try:
		datestamp = eml.getElementsByTagName('dateStamp')[0].firstChild.data.split("T")[0]
	except IndexError:
		datestamp = ''
	metadata['datestamp'] = datestamp
	
	# Intellectual Rights
	try:
		IR = eml.getElementsByTagName('intellectualRights')[0].childNodes[1].firstChild.data
	except IndexError:
		IR = ''
	metadata['IR'] = IR

	# Lead Organization & Country - taken from Creator element
	try:
		creator = eml.getElementsByTagName('creator')[0]
		try:
			organization = creator.getElementsByTagName('organizationName')[0].firstChild.data
		except IndexError:
			organization = ''
		try:
			country = creator.getElementsByTagName('country')[0].firstChild.data
		except IndexError:
			country = ''
	except IndexError:
		organization = ''
		country = ''
	metadata['organization'] = organization
	metadata['country'] = country
	
	return metadata



def listOfTerms(dwca):
	
	terms = dwca[0].keys()
	terms.sort()
	
	return terms
	
def extractSingleTerm(dwca, term):
	
	result = []
	try:
		dwca[0][term]
	except KeyError:
		errorMsg = 'The term '+str(term)+' does not exist in the selected DwC-A'
		raise MappingError(errorMsg)
	
	for i in dwca:
		result.append(i[term])
	
	return result

def distinctSingleTerm(dwca, term):
	
	result = {}
	
	nonDistinct = extractSingleTerm(dwca, term)
	
	for i in nonDistinct:
		if i in result.keys():
			result[i] += 1
		else:
			result[i] = 1
	
	return result

def extractMultiTerm(dwca, listofterms):
		
	for term in listofterms:
		try:
			dwca[0][term]
		except KeyError:
			errorMsg = 'The term '+str(term)+' does not exist in the selected DwC-A'
			raise MappingError(errorMsg)
	
	result = []
	
	for i in dwca:
		newrecord = {}
		for j in listofterms:
			newrecord[j] = i[j]
		result.append(newrecord)
	
	return result

def distinctMultiTerm(dwca, listofterms):
	
	result = {}
	body = {}
	
	nonDistinct = extractMultiTerm(dwca, listofterms)
	headers = nonDistinct[0].keys()

	for i in nonDistinct:
		combi = tuple(i.values())
		if combi in body.keys():
			body[combi] += 1
		else:
			body[combi] = 1
	
	result = {'headers':headers,'body':body}
	
	return result

	
if __name__ == "__main__":
	
	from vertnet_cred import *
	
	#dwca = dwca2list(dwca_path+'isu_mammals.zip')
	#listOfTerms = listOfTerms(dwca)
	#singleTerm = extractSingleTerm(dwca,'decimalLatitude')
	#distinctSingleTerm = distinctSingleTerm(dwca,'decimalLatitude')
	#listofterms = ['decimalLatitude','decimalLongitude']
	#multiTerm = extractMultiTerm(dwca,listofterms)
	
	#distinctMultiTerm = distinctMultiTerm(dwca, listofterms)
	#print distinctMultiTerm['body'].values()
	#print 'Distinct Lat|Lon:',len(distinctMultiTerm['body'])
	#print 'Total records:',sum(distinctMultiTerm['body'].values())
	
	#eml = meta2dict(dwca_path+'crcm_verts.zip')
	#eml = meta2dict(dwca_path+'isu_mammals.zip')
	eml = meta2dict(dwca_path+'orn.zip')
	print eml
	eml = meta2dict(dwca_path+'ttrs_birds.zip')
	print eml
