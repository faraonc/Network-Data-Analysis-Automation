#usage: python3 RFReporter3.py <filename.csv> -v
#Author: Conard James B. Faraon

"""This creates several objects of class RFReport3.py and places each object in a separate thread.
See official documentation for further details."""

import argparse
import threading
import time
import os
from rf_report_makers import RFReport3

#parse arguments here
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="Shows various messages from debugging and processing.", action="store_true")
parser.add_argument("root_csv", help="Root Metrics CSV File.")
args = parser.parse_args()

def main():
	start = time.time()
	print("Generating RF Performance Report# 3 based from ", args.root_csv, "\n")

	dirname = createDirectory()

	if args.verbose:
		print("Started Multi-threading for RFReporter3", "\n")

	threadLock = threading.Lock()
	threads = []

	rf_reporter_3_UL = RFReport3.RFReport3("Uplink", args.root_csv, dirname)
	rf_reporter_3_DL = RFReport3.RFReport3("Downlink", args.root_csv, dirname)
	rf_reporter_3_DT = RFReport3.RFReport3("Lite_Data_Test", args.root_csv, dirname)
	rf_reporter_3_ST = RFReport3.RFReport3("Lite_Data_Secure_Test", args.root_csv, dirname)

	rf_reporter_3_UL.start()
	rf_reporter_3_DL.start()
	rf_reporter_3_DT.start()
	rf_reporter_3_ST.start()

	threads.append(rf_reporter_3_UL)
	threads.append(rf_reporter_3_DL)
	threads.append(rf_reporter_3_DT)
	threads.append(rf_reporter_3_ST)

	#wait for all threads to complete
	#TODO better way to wait for threads, currently a blocking call
	if args.verbose:
		print("RFReporter3 Main thread is waiting for other threads.")

	for t in threads:
		thread_name = t.name
		print("Waiting on ", thread_name)
		t.join()
		print("Finished waiting for ",thread_name)

	print("Exiing RFReporter 3 Main Thread\n")

	end = time.time()
	print("RFReporter3 Elapsed Time: ", (end - start), " s\n")

def createDirectory():
	dirname = args.root_csv[:-4] + "_RFReport#3"
	if not os.path.exists(dirname):
		if args.verbose:
			print("Make a directory for ", dirname)
		os.makedirs(dirname)

	return dirname

main()