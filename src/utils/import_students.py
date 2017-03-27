import argparse

def get_args():
    parser = argparse.ArgumentParser(description='read student info from csv file and stores them in database')

    parser.add_argument("csvfile", help="csv to load from")
    parser.add_argument("-n", "--name",
                        default=5,
                        type=int,
                        help="column containing student name")
    parser.add_argument("-i", "--id",
                        default=3,
                        type=int,
                        help="column containing student id")
    parser.add_argument("-d", "--database",
                        default="data/gamma.db",
                        help="database file to use")

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = get_args()

    print "Import student data from %s"% args.csvfile
    print "- Database: %s"% args.database
