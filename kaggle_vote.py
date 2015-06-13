from collections import defaultdict, Counter
from glob import glob
import sys

glob_files = sys.argv[1]
loc_outfile = sys.argv[2]

def kaggle_bag(glob_files, loc_outfile, method="average", weights="uniform"):
	if method == "average":
		scores = defaultdict(list)
	with open(loc_outfile,"wb") as outfile:
		for i, glob_file in enumerate( glob(glob_files) ):
			print "parsing:", glob_file
			for e, line in enumerate( open(glob_file) ):
				if i == 0 and e == 0:
					outfile.write(line)
				if e > 0:
					row = line.strip().split(",")
					
					
					scores[(e,row[0])].append(row[1])
		for j,k in sorted(scores):
			outfile.write("%s,%s\n"%(k,Counter(scores[(j,k)]).most_common(1)[0][0]))
		print("wrote to %s"%loc_outfile)	

kaggle_bag(glob_files, loc_outfile)