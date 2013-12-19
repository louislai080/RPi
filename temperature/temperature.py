#!/usr/bin/env python

import sys
import subprocess
def get_current_temp(): 
	#return subprocess.check_output("get_temp.sh",shell=True)
	return subprocess.check_output(["/bin/sh", "get_temp.sh"])
