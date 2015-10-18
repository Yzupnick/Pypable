import argparse
import sys
from local_file import LocalFile
#from blob_storage import BlobStorage


parser = argparse.ArgumentParser(description = 'Easily pipe files or text anywhere')
parser.add_argument("-f", default=False, dest="files",action="store_const", const=True)
parser.add_argument("--name")
# TODO
# this "plugin architechture" is on dependent mutating state non-locally.
# I don't like it and need to come up with a better way to handle it
# This will lead to bugs down the line
LocalFile(parser=parser)

args = parser.parse_args()
contents = "".join(sys.stdin)
args.send(args, contents)
