from pathlib import Path
import sys
import csv

if len(sys.argv) < 3 :
	print("arguments length is under 1. input string to argument for convert.")
	sys.exit()

if len(sys.argv) > 3 :
	print("arguments length is over 3. input two string to argument for convert.")
	sys.exit()

print('file name : '+str(sys.argv[1]))


pathString ='./csv/'+str(sys.argv[1])
argvSplit = str(sys.argv[1]).split('.')
writePath = './csv/'+argvSplit[0]+'2.'+argvSplit[1]

path = Path(pathString)

if path.exists() == False:
	print(path+" is doesn't exist file")
	sys.exit()

with open(pathString, newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in spamreader:
		split = ' '.join(row).split(',,,,NNP,지명')
		convertedPart = split[1].replace(split[0],str(sys.argv[2]))
		converted = split[0]+',,,,NNP,지명'+convertedPart
		
		with open(writePath, 'a', newline='') as file:
			file.write(converted+'\n')