import pandas as pd
import sys

first_file = sys.argv[1]
second_file = sys.argv[2]

def corr(first_file, second_file):
  first_df = pd.read_csv(first_file,index_col=0)
  second_df = pd.read_csv(second_file,index_col=0)
  # assuming first column is `prediction_id` and second column is `prediction`
  prediction = first_df.columns[0]
  # correlation
  print "Finding correlation between: %s and %s" % (first_file,second_file)
  print "Column to be measured: %s" % prediction
  print "Pearson's correlation score: %0.5f" % first_df[prediction].corr(second_df[prediction],method='pearson')
  print "Kendall's correlation score: %0.5f" % first_df[prediction].corr(second_df[prediction],method='kendall')
  print "Spearman's correlation score: %0.5f" % first_df[prediction].corr(second_df[prediction],method='spearman')

corr(first_file, second_file)
