# -*- coding: iso-8859-15 -*-
from dwca import *
from singleAssessments import *
from distributionAssessments import *
from datetime import datetime
import os

def dwcaSlicer(dwca_path):

	dwca_size = os.path.getsize(dwca_path)
	slices = dwca_size/100000+1
	dwca_content = openDwca(dwca_path)
	colnames,datalines = headersDwca(dwca_content)
	slice_size = len(datalines)/slices
	
	sliced_dwca = []
	
	# For each slice...
	for i in range(slices):
		if i == 0:
			slice_lines = datalines[:(slice_size-1)]
		elif i == (slices-1):
			slice_lines = datalines[(slice_size*i)-1:]
		else:
			slice_lines = datalines[(slice_size*i)-1:((slice_size*(i+1))-1)]

		dwca_slice = readDwca2list(colnames,slice_lines)
		sliced_dwca.append(dwca_slice)
	
	return sliced_dwca

def slicedStats(sliced_dwca):
	
	sliced_stats = {}
	
	for single_slice in sliced_dwca:
		single_stats = all2dict(single_slice,False)
		
		if sliced_stats == {}:
			sliced_stats = single_stats
			sliced_species = distinctSingleTerm(single_slice,'scientificName').keys()
		else:
			for stat in sliced_stats.keys():
				if stat <> 'speciesCount':
					sliced_stats[stat] += single_stats[stat]
			
			temp = distinctSingleTerm(single_slice,'scientificName').keys()
			for sciname in temp:
				if sciname not in sliced_species:
					sliced_species.append(sciname)
	
	sliced_stats['speciesCount'] = len(sliced_species)
	
	return sliced_stats

def slicedYearDistro(sliced_dwca):
	
	sliced_distro = {}
	sliced_spdistro = {}
	
	for single_slice in sliced_dwca:

		single_distro = recsPerYear(single_slice)
		
		for couple in single_distro:
			year = couple[0]
			yearly_species = []
			for record in single_slice:
				if year == record['year']:
					if record['scientificName'] not in yearly_species:
						yearly_species.append(record['scientificName'])
				sliced_spdistro[year] = yearly_species


		
		if sliced_distro == {}:
			for i in single_distro:
				sliced_distro[i[0]] = [i[1],sliced_spdistro[i[0]]]
		
		else:
			for bit in single_distro:
				year2check = bit[0]
				newvalue = bit[1]
				species_list = sliced_spdistro[year2check]
				
				if year2check in sliced_distro.keys():
					sliced_distro[year2check][0] += newvalue
					for i in species_list:
						if i in sliced_distro[year2check][1]:
							continue
						else:
							sliced_distro[year2check][1].append(i)
				else:
					tempelement = [newvalue,species_list]
					sliced_distro[year2check] = tempelement
	
	return sliced_distro

def slicedCumYearDistro(sliced_dwca):
	
	sliced_distro = slicedYearDistro(sliced_dwca)
	noncum = sorted(sliced_distro.keys())	
	sliced_cumdistro = []
	cumsp = []
	cont = 0
	
	for i in noncum:
		try:
			int(i)
		except ValueError:
			continue
		if int(i)<1750 or int(i)>datetime.now().year:
			continue
		
		if cont == 0:
			sliced_cumdistro.append([i,sliced_distro[i][0],len(sliced_distro[i][1])])
			for sp in sliced_distro[i][1]:
				cumsp.append(sp)
			cont += 1
		else:
			newrec = sliced_distro[i][0]
			newtotrec = newrec + sliced_cumdistro[cont-1][1]

			newsp = 0
			for sp in sliced_distro[i][1]:
				if sp in cumsp:
					continue
				else:
					cumsp.append(sp)
					newsp += 1
			newtotsp = newsp + sliced_cumdistro[cont-1][2]
			
			newrow = [i,newtotrec,newtotsp]
			sliced_cumdistro.append(newrow)
			cont += 1
	
	return sliced_cumdistro

def slicedPercCumYearDistro(sliced_dwca):
	
	sliced_perccumdistro = []
	sliced_cumdistro = slicedCumYearDistro(sliced_dwca)
	
	maxrec = sliced_cumdistro[-1][1]
	maxsp = sliced_cumdistro[-1][2]
	
	for i in sliced_cumdistro:
		year = i[0]
		rec = round(((i[1]*1.0)/maxrec)*100,4)
		sp = round(((i[2]*1.0)/maxsp)*100,4)
		
		sliced_perccumdistro.append([year, rec, sp])
	
	return sliced_perccumdistro

def slicedTermDistro(sliced_dwca, term):
	
	try:
		sliced_dwca[0][0][term]
	except KeyError:
		errorMsg = 'The term '+str(term)+' does not exist in the selected DwC-A'
		raise MappingError(errorMsg)
	
	sliced_termdict = {}
	
	for single_slice in sliced_dwca:
		
		for record in single_slice:
			term_value = record[term]
			if term_value not in sliced_termdict.keys():
				sliced_termdict[term_value] = 1
			else:
				sliced_termdict[term_value] += 1
	
	sliced_termdistro = []
	for i in sorted(sliced_termdict.keys()):
		sliced_termdistro.append([i,sliced_termdict[i]])
	
	return sliced_termdistro

def slicedKingdomDistro(sliced_dwca):
	sliced_termdistro = slicedTermDistro(sliced_dwca, 'kingdom')
	return sliced_termdistro
def slicedPhylumDistro(sliced_dwca):
	sliced_termdistro = slicedTermDistro(sliced_dwca, 'phylum')
	return sliced_termdistro
def slicedClassDistro(sliced_dwca):
	sliced_termdistro = slicedTermDistro(sliced_dwca, 'class')
	return sliced_termdistro
def slicedBasisDistro(sliced_dwca):
	sliced_termdistro = slicedTermDistro(sliced_dwca, 'basisOfRecord')
	return sliced_termdistro
def slicedCountryDistro(sliced_dwca):
	sliced_termdistro = slicedTermDistro(sliced_dwca, 'country')
	return sliced_termdistro

if __name__ == '__main__':

#	dwca_path = './DWCAs/arctos.zip'	
	dwca_path = './DWCAs/utep_verts.zip'
	sliced_dwca = dwcaSlicer(dwca_path)
	
#	print '{0} slices.'.format(len(sliced_dwca))
#	print '{0} records on the first slice.'.format(len(sliced_dwca[0]))
#	print '{0} records on the last slice.'.format(len(sliced_dwca[-1]))
	
	sliced_stats = slicedStats(sliced_dwca)
	print sliced_stats
	
#	sliced_distro = slicedYearDistro(sliced_dwca)
#	print sliced_distro
	
#	sliced_cumdistro = slicedCumYearDistro(sliced_dwca)
#	print sliced_cumdistro

	sliced_perccumdistro = slicedPercCumYearDistro(sliced_dwca)
	print sliced_perccumdistro
	
	sliced_termdistro = slicedBasisDistro(sliced_dwca)
	print sliced_termdistro
	
