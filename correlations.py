import pandas as pd
import sys

first_file = sys.argv[1]
second_file = sys.argv[2]

def corr(first_file, second_file):
  first_df = pd.read_csv(first_file)
  second_df = pd.read_csv(second_file)
  goal = first_df.columns[1]
  print "Finding correlation between: %s and %s" % (first_file,second_file)
  print "Column to be measured: %s" % goal
  print "Pearson's correlation score: %0.5f" % first_df[goal].corr(second_df[goal],method='pearson')
  print "Kendall's correlation score: %0.5f" % first_df[goal].corr(second_df[goal],method='kendall')
  print "Spearman's correlation score: %0.5f" % first_df[goal].corr(second_df[goal],method='spearman')

corr(first_file, second_file)