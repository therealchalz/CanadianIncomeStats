#!/usr/bin/python
import csv

files=["tbl2ab.csv","tbl2bc.csv","tbl2mb.csv","tbl2nb.csv","tbl2nl.csv","tbl2ns.csv","tbl2nt.csv","tbl2nu.csv","tbl2on.csv","tbl2pe.csv","tbl2qc.csv","tbl2sk.csv","tbl2yt.csv"]

# must be same order as files above
provinces=["AB","BC","MB","NB","NL","NS","NT","NU","ON","PE","QC","SK","YT"]

csvFormat={"firstDataRow": 2, 
	"firstPopColumnCount": 7, 
	"firstPopColumnAmount": 8, 
	"columnIncrement": 2, 
	"maxColumnIndex": 44, 
	"firstPopColumnAmount": 8}

# row number to Population field mapping
rowFields={29:"totalIncome", 
	2:"taxableReturns", 
	3:"untaxableReturns", 
	4:"totalReturns"}
# row number to wanted column mapping (index of first population column, which gets incremented by columnIncrement)
rowDataColumn={29:csvFormat["firstPopColumnAmount"], 
	2:csvFormat["firstPopColumnCount"], 
	3:csvFormat["firstPopColumnCount"], 
	4:csvFormat["firstPopColumnCount"]}
# Population field to load function mapping
fieldLoadFunctions = {"totalIncome": (lambda x: x*1000), 
	"taxableReturns": (lambda x: x), 
	"untaxableReturns": (lambda x: x), 
	"totalReturns": (lambda x: x)}


class Population:
	def __init__(self):
		self.count=0
		self.taxableReturns=0
		self.untaxableReturns=0
		self.totalReturns=0
		self.totalIncome=0
		self.province="xx"
		self.avgIncome=0
	def finish(self):
		#self.count = self.taxableReturns + self.untaxableReturns
		self.count = self.totalReturns
		if self.count > 0:
			self.avgIncome = self.totalIncome/self.count



def parseRowForData(populations, row, rowNumber):
	try:
		rowField = rowFields[rowNumber]
	except KeyError:
		return
	if rowField is not None:
		popIdx = 0
		popCol = rowDataColumn[rowNumber]-1
		while popCol <= csvFormat["maxColumnIndex"]-1:
			if row[popCol] == '':
				setattr(populations[popIdx], rowField, 0)
			else:
				setattr(populations[popIdx], rowField, fieldLoadFunctions[rowField](int(row[popCol])))
			popIdx+=1
			popCol+=csvFormat["columnIncrement"]
			
		
def processFile(file, province):
	print "Processing ",file
	populations = []
	with open(file, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=",", quotechar="\"")

		currentRow = 1;
		line = csvreader.next()
		while currentRow < csvFormat["firstDataRow"]:
			line = csvreader.next()
			currentRow+=1

		popCol = csvFormat["firstPopColumnCount"]
		while popCol <= csvFormat["maxColumnIndex"]:
			newPop = Population()
			newPop.province = province
			popCol += csvFormat["columnIncrement"]
			populations.append(newPop)

		while line is not None:
			parseRowForData(populations, line, currentRow)
			line = next(csvreader, None)
			currentRow+=1

	for pop in populations:
		pop.finish()
		print "Pop: ", pop.avgIncome, " ", pop.count, " ", pop.province, " ", pop.totalIncome
		


if __name__ == "__main__":
	provinceIndex = 0
	for file in files:
		processFile(file, provinces[provinceIndex])
		provinceIndex+=1