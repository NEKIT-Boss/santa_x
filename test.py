#!/usr/env/bin python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

ERROR_CODE = 1
NO_ERROR_CODE = 0

program_name = "main.py"
file_name_to_test = sys.argv[1]
test_iterations = int(sys.argv[2])

failed = False
failed_index = -1
	
with open(os.devnull, "w") as trash:
	for i in range(0, test_iterations):
		result = subprocess.call(["python", program_name, file_name_to_test], stdout=trash)
		if (result):
			failed = True
			failed_index = i
			break
	
if (not failed):
	print "Excellent!"
else:
	print "Something went wrong on {} iteration!".format(failed_index)			
