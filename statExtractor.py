from dwca import *
from singleAssessments import *
import os
import zipfile
import shutil

dwcaPath = './tests/'
fileList = os.listdir(dwcaPath)
fileList = sorted(fileList)
statsFolder = './stats/'

# Remove stats folder
if os.path.isdir(statsFolder):
	shutil.rmtree(statsFolder)
	print 'Folder deleted'
else:
	print 'Folder does not exist'

# Create stats folder
os.mkdir(statsFolder)
print 'Stats folder created'

for fileName in fileList:

	filePath = dwcaPath+fileName
	
	# Ignore non-IPT files
	try:
		z = zipfile.ZipFile(filePath)
	except zipfile.BadZipfile:
		continue
	z.close()
	
	dwcaSize = os.path.getsize(filePath)
	
	slices = dwcaSize/1000000+1
	
	dwcaName = fileName[:-4]
	
	# Create subdirectory for each dwca
	os.mkdir(statsFolder+'/'+dwcaName)
	print 'Created subfolder for',dwcaName
	
	if slices <= 1:
		print 'Single slice dwca'
		dwca = dwca2list(filePath)
		print 'DWCA opened'
		simpleStats = all2dict(dwca)
		print 'Stats extracted'
		for stat in simpleStats.keys():
			f = open(statsFolder+'/'+dwcaName+'/'+stat+'.txt','w')
			f.write(str(simpleStats[stat]))
			f.close()
		print 'Stats saved'
	else:
		print 'Multi slice dwca'
		dwcacontent = openDwca(filePath)
		colnames,datalines = headersDwca(dwcacontent)
		sliceSize = len(datalines)/slices
		print len(datalines),'lines'
		print slices,'slices'
		print sliceSize,'lines per slice'
		
		simpleStats = {}
		
		for i in range(slices):
			print 'Slice',(i+1)
			if i == 0:
				sliceLines = datalines[:(sliceSize-1)]
			elif i == (slices-1):
				sliceLines = datalines[(sliceSize*i):]
			else:
				sliceLines = datalines[(sliceSize*i):((sliceSize*(i+1))-1)]
			dwcaSlice = readDwca2list(colnames,sliceLines)
			print 'DWCA slice opened'

			simpleStats = all2dict(dwcaSlice,False)

			print 'Slice stats extracted'
	print simpleStats
