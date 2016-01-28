from index import indexer
import sys
my_index=indexer()

try:
    if sys.argv[1]=="drop":
        my_index.index.drop()
except:
    pass

my_index.path="/home/cocco2/Documents/magistrale_1/complessi/citazioni/aps-dataset-metadata-2013"

my_index.postinglist()
