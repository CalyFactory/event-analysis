from pathlib import Path
import sys
from manager import db_manager

rows = db_manager.query('select station_name, old_address from SUBWAY_INFO')

for row in rows:
	if type(row.old_address) is str:
		splitedAddress = row.old_address.split(' ')

		#print(row.station_name)
		print(row.station_name+' / '+splitedAddress[2])

