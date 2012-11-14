# IMPORTANT NOTE
# These assessments are only performed on IPT downloaded
# DarwinCore Archives. Due to the lack of metadata of other
# types of archives and given the fact that IPT will become
# the standard for data publishing, .csv.gz archives will
# NOT be assessed

from dwca import *

def recordCount(dwca):
	if type(dwca) != type({}):
		total = len(dwca)
	else:
		total = len(dwca[dwca.keys()[0]])

	return total

def speciesCount(dwca):
	species = distinctSingleTerm(dwca, 'scientificName')
	empty = False
	for i in species.keys():
		if i == '':
			empty = True
	if empty:
		total = len(species.keys())-1
	else:
		total = len(species.keys())
	
	return total
	
	
def georeferenceCount(dwca):
	coordinates = distinctMultiTerm(dwca, ['decimalLatitude','decimalLongitude'])
	coordinates = coordinates['body']
	for i in coordinates.keys():
		try:
			float(i[0]), float(i[1])
		except ValueError:
			coordinates[i] = 0
			
	total = sum(coordinates.values())
	
	return total

def datedCount(dwca):
	dated = distinctMultiTerm(dwca, ['year','month','day'])
	dated = dated['body']
	for i in dated.keys():
		try:
			float(i[0]), float(i[1]), float(i[2])
		except ValueError:
			dated[i] = 0
	
	total = sum(dated.values())
	
	return total

def termCount(dwca, term):
	termCount = distinctSingleTerm(dwca, term)
	termCount[''] = 0
	total = sum(termCount.values())
	
	return total

def kingdomCount(dwca):
	total = termCount(dwca, 'kingdom')
	return total

def basisCount(dwca):
	total = termCount(dwca, 'basisOfRecord')
	return total

def yearCount(dwca):
	total = termCount(dwca, 'year')
	return total

def scinameCount(dwca):
	total = termCount(dwca, 'scientificName')
	return total

def all2dict(dwca,perc = True):
	
	try:
		arecordCount = recordCount(dwca)
	except MappingError:
		arecordCount = 0
	try:
		aspeciesCount = speciesCount(dwca)
	except MappingError:
		aspeciesCount = 0
	try:
		ageoreferenceCount = georeferenceCount(dwca)
	except MappingError:
		ageoreferenceCount = 0
	try:
		adatedCount = datedCount(dwca)
	except MappingError:
		adatedCount = 0
	try:
		akingdomCount = kingdomCount(dwca)
	except MappingError:
		akingdomCount = 0
	try:
		abasisCount = basisCount(dwca)
	except MappingError:
		abasisCount = 0
	try:
		ayearCount = yearCount(dwca)
	except MappingError:
		ayearCount = 0
	try:
		ascinameCount = scinameCount(dwca)
	except MappingError:
		ascinameCount = 0

	
	result = {
		'recordCount': arecordCount,
		'speciesCount': aspeciesCount,
		'georeferenceCount': ageoreferenceCount,
		'datedCount': adatedCount,
		'kingdomCount': akingdomCount,
		'basisCount': abasisCount,
		'yearCount': ayearCount,
		'scinameCount': ascinameCount
	}
	
	if perc == True:
		result['georeferencePerc'] = round(ageoreferenceCount*100/arecordCount,2)
		result['datedPerc'] = round(adatedCount*100/arecordCount,2)
		result['kingdomPerc'] = round(akingdomCount*100/arecordCount,2)
		result['basisPerc'] = round(abasisCount*100/arecordCount,2)
		result['yearPerc'] = round(ayearCount*100/arecordCount,2)
		result['scinamePerc'] = round(ascinameCount*100/arecordCount,2)
	
	return result

if __name__ == "__main__":
	
	dwca_path = './DWCAs/'
	dwca = dwca2list(dwca_path+'fmnh_fishes.zip')
	all2dict = all2dict(dwca,True)
	print all2dict
	
