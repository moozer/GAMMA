import argparse
import csv

import sys

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

sys.path.append(dir_path+'/..')

from datastore import *

def get_args():
    parser = argparse.ArgumentParser(description='read student info from csv file and stores them in database')

    parser.add_argument("csvfile", help="csv to load from")
    parser.add_argument("-n", "--name",
                        default=4,
                        type=int,
                        help="column containing student name")
    parser.add_argument("-i", "--id",
                        default=2,
                        type=int,
                        help="column containing student id")
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

    print "Import student data from %s"% args.csvfile

    print "- Database: %s"% args.database
    ds = Datastore(args.database )

    print "- Importing students"
    with open(args.csvfile, 'rb') as csvfile:
        studreader = csv.reader(csvfile, delimiter=';')

        if args.skip_first_line:
            next(studreader)  # skip header row

        for stud in studreader:
            s = student_record(id=stud[2],
                               name=stud[4].decode('iso8859-1') )
            print "-- ", s
            try:
                ds.add_student(s)
            except IntegrityError, ex:
                print "--- DB error: User already exists?"
                print "---", ex
