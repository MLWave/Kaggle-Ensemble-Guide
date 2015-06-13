from collections import defaultdict
from glob import glob 
import sys

glob_files = sys.argv[1]
loc_outfile = sys.argv[2]

def kaggle_bag(glob_files, loc_outfile, method="average", weights="uniform"):
	if method == "average":
		scores = defaultdict(float)
	with open(loc_outfile,"wb") as outfile:
		for i, glob_file in enumerate( glob(glob_files) ):
			print "parsing:", glob_file
			for e, line in enumerate( open(glob_file) ):
				if i == 0 and e == 0:
					outfile.write(line)
				if e > 0:
					row = line.strip().split(",")
					
					
					scores[(e,row[0])] += float(row[1])
		for j,k in sorted(scores):
			outfile.write("%s,%f\n"%(k,scores[(j,k)]/(i+1)))

kaggle_bag(glob_files, loc_outfile)