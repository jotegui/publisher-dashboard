# IMPORTANT NOTE
# These assessments are only performed on IPT downloaded
# DarwinCore Archives. Due to the lack of metadata of other
# types of archives and given the fact that IPT will become
# the standard for data publishing, .csv.gz archives will
# NOT be assessed

from dwca import *
from datetime import datetime

def recsPerTerm(dwca, term):
	
	result = []
	
	try:
		recsPerTerm = distinctSingleTerm(dwca, term)
	except MappingError as e:
		return result
	sortedTerms = sorted(recsPerTerm, key=lambda key: recsPerTerm[key])
	resortedTerms = []
	for i in range(len(sortedTerms)):
		resortedTerms.append(sortedTerms[len(sortedTerms)-i-1])
	
	for i in resortedTerms:
		record = [i, recsPerTerm[i]]
		result.append(record)
	
	return result

def recsPerKingdom(dwca):
	result = recsPerTerm(dwca, 'kingdom')
	return result
	
def recsPerCountry(dwca):
	result = recsPerTerm(dwca, 'country')
	return result
	
def recsPerYear(dwca):
	result = recsPerTerm(dwca, 'year')
	return result

def recsPerBasis(dwca):
	result = recsPerTerm(dwca, 'basisOfRecord')
	return result

def cumRecsPerYear(dwca):
	noncum = sorted(recsPerYear(dwca))
	result = []
	cont = 0

	for i in range(len(noncum)):
		try:
			int(noncum[i][0])
		except ValueError:
			continue
		if int(noncum[i][0])<1750 or int(noncum[i][0])>datetime.now().year:
			continue
		if cont == 0:
			result.append(noncum[i])
			cont += 1
		else:
			result.append([noncum[i][0],noncum[i][1]+result[cont-1][1]])
			cont += 1
	
	return result

def speciesPerTerm(dwca, term):
	
	speciesPerTerm = distinctMultiTerm(dwca, ['scientificName',term])
	
	termIndex = 'a'
	scinameIndex = 'a'
	for i in range(len(speciesPerTerm['headers'])):
		if speciesPerTerm['headers'][i] == term:
			termIndex = i
		if speciesPerTerm['headers'][i] == 'scientificName':
			scinameIndex = i
	speciesPerTerm = speciesPerTerm['body']
	
	unOrdered = {}
	result = []
	
	for i in speciesPerTerm.keys():
		if i[scinameIndex] == '':
			continue
		if i[termIndex] in unOrdered.keys():
			unOrdered[i[termIndex]] += 1
		else:
			unOrdered[i[termIndex]] = 1
			
	sortedTerms = sorted(unOrdered, key=lambda key: unOrdered[key])
	resortedTerms = []
	for i in range(len(sortedTerms)):
		resortedTerms.append(sortedTerms[len(sortedTerms)-i-1])
	
	for i in resortedTerms:
		record = [i, unOrdered[i]]
		result.append(record)
	
	return result

def speciesPerBasis(dwca):
	result = speciesPerTerm(dwca, 'basisOfRecord')
	return result

def speciesPerKingdom(dwca):
	result = speciesPerTerm(dwca, 'kingdom')
	return result

def speciesPerCountry(dwca):
	result = speciesPerTerm(dwca, 'country')
	return result

def speciesPerYear(dwca):
	result = []
	term = 'year'
	try:
		speciesPerTerm = distinctMultiTerm(dwca, ['scientificName', term])
	except MappingError as e:
		return result
	
	years = sorted(distinctSingleTerm(dwca, term))
	
	termIndex = 'a'
	scinameIndex = 'a'
	for i in range(len(speciesPerTerm['headers'])):
		if speciesPerTerm['headers'][i] == term:
			termIndex = i
		if speciesPerTerm['headers'][i] == 'scientificName':
			scinameIndex = i
	speciesPerTerm = speciesPerTerm['body']
	cumspecies = []

	for year in years:
		species = []
		try:
			int(year)
		except ValueError:
			continue
		for combi in speciesPerTerm.keys():
			if combi[termIndex] <> year:
				continue
			else:
				if combi[scinameIndex] in cumspecies:
					continue
				else:
					species.append(combi[scinameIndex])
					cumspecies.append(combi[scinameIndex])
		
		result.append([year,len(species)])

	return result

def cumSpeciesPerYear(dwca):
	noncum = speciesPerYear(dwca)
	result = []
	cont = 0

	for i in range(len(noncum)):
		try:
			int(noncum[i][0])
		except ValueError:
			continue
		if int(noncum[i][0])<1750 or int(noncum[i][0])>datetime.now().year:
			continue
		if cont == 0:
			result.append(noncum[i])
			cont += 1
		else:
			result.append([noncum[i][0],noncum[i][1]+result[cont-1][1]])
			cont += 1
	
	return result

if __name__ == "__main__":

	from vertnet_cred import *
	
	dwca = dwca2list('./DWCAs/'+'isu_mammals.zip')
	
	cumSpeciesPerYear = cumSpeciesPerYear(dwca)
	#print cumSpeciesPerYear
	
#	print 'Distributions according to a term:'
#	print 'Records per Kingdom:'
#	recsPerKingdom = recsPerKingdom(dwca)
#	for i in recsPerKingdom:
#		if i[0] == '':
#			i[0] = '[Empty]'
#		print i[0],':',i[1]
#
#	print
#	
#	print 'Species per Kingdom:'
#	speciesPerKingdom = speciesPerKingdom(dwca)
#	for i in speciesPerKingdom:
#		if i[0] == '':
#			i[0] = '[Empty]'
#		print i[0],':',i[1]
#	
#	print
#	
#	print 'Records per Country:'
#	recsPerCountry = recsPerCountry(dwca)
#	for i in recsPerCountry:
#		if i[0] == '':
#			i[0] = '[Empty]'
#		print i[0],':',i[1]
#	
#	print
#
#	print 'Species per Country:'
#	speciesPerCountry = speciesPerCountry(dwca)
#	for i in speciesPerCountry:
#		if i[0] == '':
#			i[0] = '[Empty]'
#		print i[0],':',i[1]
#
#	print
#	
#	print 'Records per Year:'
#	recsPerYear = recsPerYear(dwca)
#	for i in recsPerYear:
#		if i[0] == '':
#			i[0] = '[Empty]'
#		print i[0],':',i[1]
#	
#	print
#
#	print 'Species per Year:'
#	speciesPerYear = speciesPerYear(dwca)
#	for i in speciesPerYear:
#		if i[0] == '':
#			i[0] = '[Empty]'
#		print i[0],':',i[1]
#	
#	print
#	
#	print 'Records per Basis:'
#	recsPerBasis = recsPerBasis(dwca)
#	for i in recsPerBasis:
#		if i[0] == '':
#			i[0] = '[Empty]'
#		print i[0],':',i[1]
#	
#	print
#	
#	print 'Species per Basis:'
#	speciesPerBasis = speciesPerBasis(dwca)
#	for i in speciesPerBasis:
#		if i[0] == '':
#			i[0] = '[Empty]'
#		print i[0],':',i[1]
