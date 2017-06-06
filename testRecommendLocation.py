# -*- coding: utf-8 -*-

import unittest
import recommendLocation

import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# python3 -m unittest -v testRecommendLocation.py

class TestExtract(unittest.TestCase):

	def testLocation(self):
		self.assertTrue(recommendLocation.testAnalysis('af0b3b5e551180310106982d9c94786507e397236cf93f345011850f'), 
			{
				"event_hashkey": "af0b3b5e551180310106982d9c94786507e397236cf93f345011850f",
				"locations" : "None",
				"time_set" : {
					"extract_start": "None",
					"extract_end": "None",
					"event_start": "12:00",
					"event_end": "13:00"
				},
				"event_types" : [
					{ "id" : "CPI02" }
				]
			})


# Testcase 1 : all
#testAnalysis('3275008b3da8adf4874f6e09cc127c75cf46711b3031cdebd1db9a29')
# Testcase 2 : without purpose
#testAnalysis('907d71d0b0809116217205674096ec15929c1dbe5afa9057d98cd439')
# Testcase 3 : without extractTime
#recommendLocation.testAnalysis('af0b3b5e551180310106982d9c94786507e397236cf93f345011850f')
# Testcase 4 : without location
#testAnalysis('217f53d8b6511daaf659f2911872a72b8be22c39c27714e3e2859f0e')

