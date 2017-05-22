import sys

if len(sys.argv) < 2 :
	print("arguments length is 0. input string to argument for convert.")
	sys.exit()

if len(sys.argv) > 2 :
	print("arguments length is over 2. input only one string to argument for convert.")
	sys.exit()

print('file name : '+str(sys.argv[1]))

