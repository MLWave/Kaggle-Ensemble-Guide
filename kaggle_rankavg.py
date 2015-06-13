from __future__ import division
from glob import glob
import sys
from collections import defaultdict

glob_files = sys.argv[1]
output_file = sys.argv[2]

print(glob_files)
with open(output_file,"wb") as outfile:
	all_ranks = defaultdict(list)
	for file_nr, glob_file in enumerate( glob(glob_files) ):
		file_ranks = []
		print(glob_file)
		for e, line in enumerate( open(glob_file) ):
			if e == 0 and file_nr == 0:
				outfile.write( line )
			elif e > 0:
				r = line.strip().split(",")
				file_ranks.append( (float(r[1]), e, r[0]) )
		for rank, item in enumerate( sorted(file_ranks) ):
			all_ranks[(item[1],item[2])].append(rank)	
	average_ranks = []
	for k in sorted(all_ranks):
		average_ranks.append((sum(all_ranks[k])/len(all_ranks[k]),k))
	ranked_ranks = []
	for rank, k in enumerate(sorted(average_ranks)):
		ranked_ranks.append((k[1][0],k[1][1],rank/(len(average_ranks)-1)))
	for k in sorted(ranked_ranks):
		outfile.write("%s,%s\n"%(k[1],k[2]))
	print("wrote to %s"%output_file)