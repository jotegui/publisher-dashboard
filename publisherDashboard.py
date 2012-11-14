#import json
#import cgi
#import urllib
#from google.appengine.api import urlfetch
from dwca import *
from slicedDwca import *
from singleAssessments import *
from distributionAssessments import *
import webapp2
import os
import zipfile
import jinja2
from datetime import datetime

jinja_environment = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
	def get(self):

		# Variable setup
		selectedDwca = self.request.get('dwca')
		dwcaPath = './DWCAs/'
		
		# Build DWCA list
		fileList = os.listdir(dwcaPath)
		dwcaList = []
		
		for i in fileList:
			try:
				z = zipfile.ZipFile(dwcaPath+i)
			except zipfile.BadZipfile:
				continue
			fileName = i[:-4]
			dwcaList.append(fileName)
		sDwcaList = sorted(dwcaList)
		
		# Prepare DWCA list <select>
		dropdown = '<form action="." method="GET" id="form">'
		dropdown += '<table><tr><td>'
		dropdown += '<select name="dwca" onChange="document.getElementById(\'img\').style.visibility=\'visible\';this.form.submit()">'
		dropdown += '<option value="">Select a DwC-A</option>'
		for i in sDwcaList:
			dropdown += '<option value="'+i+'"'
			if i == selectedDwca:
				dropdown += ' selected="True"'
			dropdown += '>'+i+'</option>'
		dropdown += '</select></td>'
		dropdown += '<td><img id="img" src="./files/loading.gif" style="visibility:hidden;"></img></td>'
		dropdown += '</tr></table></form>'
		
		# Output for the <select> block
		#self.response.headers['Content-Type'] = 'text/HTML'
		self.response.out.write(dropdown)
		
		self.response.write('<hr>')

		# Load the DWCA file and do the stuff
		if selectedDwca <> '':
			filePath = dwcaPath+selectedDwca+'.zip'
			dwcaSize = os.path.getsize(filePath)
			slices = dwcaSize/100000+1
			
			yearDistro = []
			percYearDistro = []
			kingdomDistro = []
			basisDistro = []
			countryDistro = []
			
			# Just one slice
			if slices <= 1:
				dwca = dwca2list(filePath)
				stats = all2dict(dwca)
				cumRecsYear = cumRecsPerYear(dwca)
				cumSpeciesYear = cumSpeciesPerYear(dwca)
				yearDistro = []
				if cumRecsYear <> [] and cumSpeciesYear <> []:
					for i in range(len(cumRecsYear)):
						yearDistro.append([cumRecsYear[i][0], cumRecsYear[i][1], cumSpeciesYear[i][1]])
				kingdomDistro = recsPerKingdom(dwca)
				basisDistro = recsPerBasis(dwca)
				countryDistro = recsPerCountry(dwca)
				
			# Several slices
			else:
				sliced_dwca = dwcaSlicer(filePath)
				stats = slicedStats(sliced_dwca)
				percYearDistro = slicedPercCumYearDistro(sliced_dwca)
				yearDistro = slicedCumYearDistro(sliced_dwca)
				try:
					kingdomDistro = slicedKingdomDistro(sliced_dwca)
				except MappingError:
					kingdomDistro = []
				try:
					basisDistro = slicedBasisDistro(sliced_dwca)
				except MappingError:
					basisDistro = []
				try:
					countryDistro = slicedCountryDistro(sliced_dwca)
				except MappingError:
					countryDistro = []
				
		# Export values for the template
			template_values = {
				'dwca': selectedDwca,
				'stats': stats,
				'georeferencePerc': round((stats['georeferenceCount']*100)/stats['recordCount'],2),
				'datedPerc': round((stats['datedCount']*100)/stats['recordCount'],2),
				'kingdomPerc': round((stats['kingdomCount']*100)/stats['recordCount'],2),
				'basisPerc': round((stats['basisCount']*100)/stats['recordCount'],2),
				'yearPerc': round((stats['yearCount']*100)/stats['recordCount'],2),
				'scinamePerc': round((stats['scinameCount']*100)/stats['recordCount'],2),
				'yearDistro' : yearDistro,
				'percYearDistro' : percYearDistro,
				'kingdomDistro' : kingdomDistro,
				'basisDistro' : basisDistro,
				'countryDistro' : countryDistro
			}

		# Load the template
			template = jinja_environment.get_template('content.html')
			self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([('/*.*', MainPage)], debug=True)
