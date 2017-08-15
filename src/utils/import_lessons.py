import argparse
import csv
import datetime
import sys

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

sys.path.append(dir_path+'/..')

from datastore import *

def get_args():
	parser = argparse.ArgumentParser(description='read student info from csv file and stores them in database')

	parser.add_argument("csvfile", help="csv to load from")
	parser.add_argument("-n", "--name",
						default=1,
						type=int,
						help="column containing lesson name")
	parser.add_argument("-i", "--id",
						default=0,
						type=int,
						help="column containing lessons date (used as id)")
	parser.add_argument("-d", "--database",
						default="data/gamma.db",
						help="database file to use")
	parser.add_argument("--skip-first-line",
						default=True,
						action="store_true",
						help="If set, skips first line of the csv file")

	args = parser.parse_args()

	return args


if __name__ == "__main__":
	args = get_args()

	print "Import lesson data from %s"% args.csvfile

	print "- Database: %s"% args.database
	ds = Datastore(args.database )

	print "- Importing lessons"
	with open(args.csvfile, 'rb') as csvfile:
		lessonreader = csv.reader(csvfile, delimiter=';')

		if args.skip_first_line:
			next(lessonreader)  # skip header row

		for lesson in lessonreader:
			l = lesson_record(
					date=datetime.datetime.strptime(lesson[args.id], "%Y-%m-%d").date(),
					name=lesson[args.name].decode('iso8859-1') )
			print "-- ", l
			try:
				ds.add_lesson(l)
			except IntegrityError, ex:
				print "--- DB error: lesson already exists?"
				print "---", ex
