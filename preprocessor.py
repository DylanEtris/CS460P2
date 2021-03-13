#!/usr/bin/python3
import csv
import sys
import pdb
import operator
import copy

def normalize(data, feature_num = None):
  data = copy.deepcopy(data)
  if feature_num != None:
    features = [example[feature_num] for example in data]
    max_f = max(features)
    min_f = min(features)
    for i in range(len(data)):
      data[i][feature_num] = (data[i][feature_num] - min_f) / (max_f - min_f)
  else:
    max_f = max(data)
    min_f = min(data)
    for f in range(len(data)):
      data[f] = (data[f] - min_f) / (max_f - min_f)
  return data

# Function: read_csv
# Inputs:   path to csv file
# Outputs:  data - [[feature1, feature1, ...],
#                 [feature2, feature2, ...],
#                 ...
#                 [label, label, ...]
#                ]
# Purpose:  Opens and reads CSV file
def read_csv(path, headers = False):
  data_file = open(path, "r")
  data = list(csv.reader(data_file))
  data_file.close()
  if headers:
    data.pop(0)

  for i in range(len(data)):
    for j in range(len(data[i])):
      try:
        data[i][j] = float(data[i][j])
      except:
        data[i][j] = data[i][j]
  return data

# Function: sort_data
# Inputs:   Array of Arrays, with feature_num being sub-index
# Outputs:  Input, but sorted by feature_num
# Purpose:  Sort an array of arrays by sub array index
def sort_data(data, feature_num):
  for example in data:
    example[feature_num] = float(example[feature_num])
  return sorted(data, key=operator.itemgetter(feature_num))

# Function: write_csv
# Inputs:   example set (data), path to .csv file
# Outputs:  None
# Purpose:  Write data to .csv file
def write_csv(path, data):
  output_file = open(path, 'w')
  csv_writer = csv.writer(output_file)
  for x in data:
    csv_writer.writerow(x)
  output_file.close()

def equidense(num_bins, data, feature_num):
  bin_length = len(data) / num_bins
  current_bound = bin_length
  current_bin = 0
  binned_data = []
  i = 0
  for example in data:
    example[feature_num] = current_bin
    binned_data.append(data[i])
    if i == current_bound:
      current_bin += 1
      current_bound += bin_length
    i += 1
  return binned_data
  

# Function: equidistant
# Inputs:   bin_length:   float
#           data:         [[feature_1, feature_2, ..., class_label],
#                         ...,
#                         ]
#           feature_num:  index of feature to bin
# Outputs:  binned_data:  Same format as data, with feature_num put into bins
# Purpose:  sort the given feature into bins using equidistant method
def equidistant(num_bins, data, feature_num):
  #Get Bin Length
  maximum = max([float(example[feature_num]) for example in data])
  minimum = min([float(example[feature_num]) for example in data])
  data_range = maximum - minimum
  bin_length = data_range / num_bins

  #Get original Bounds
  current_bin = 0
  previous_bound = minimum 
  current_bound = minimum + bin_length
  binned_data = []
  i = 0
  while i < len(data):
    if data[i][feature_num] >= previous_bound and data[i][feature_num] <= current_bound:
      data[i][feature_num] = current_bin
      binned_data.append(data[i])
      i += 1
    else:
      current_bin = current_bin + 1
      previous_bound = current_bound
      if current_bin == num_bins - 1:
        current_bound = maximum
      else:
        current_bound += bin_length
  return binned_data

def bin_example(example, minimum, maximum, num_bins, feature_num):
  boundaries = np.arange(minimum, maximum, num_bins)
  bin_num = 0
  for i in range(len(boundaries) - 1):
    f = example[feature_num]
    pb = boundaries[i]
    cb = boundaries[i+1]
    if f > pb and f < cb:
      example[feature_num] = i
  return example

# Function: bin_data
# Inputs:   An array of examples, num_bins, the feature to bin, and either 'equidistant' or 'equidense'
# Outputs:  A modified array of examples with feature_num placed into bins
# Purpose:  Select either equidistant or equidense binning methods and place the specified features
#           into those bins
def bin_data(data, num_bins, feature_num, bin_method = 'equidistant'):
  bin_length = 0
  try:
    data = sort_data(data, feature_num)
  except:
    return new_data # Must already be in strings, which are guaranteed to be discrete

  if bin_method == 'equidistant':
    binned_data = equidistant(num_bins, data, feature_num)
  if bin_method == 'equidense':
    binned_data = equidense(num_bins, data, feature_num)

  return binned_data

# Function: main
# Inputs:   None
# Outputs:  None
# Purpose:  Main
def main(input_file, num_bins, feature_num):
  data = []
  data = read_csv(input_file)
  data = bin_data(data, num_bins, feature_num, bin_method='equidense')
  write_csv('./data_files/binned_data.csv', data)

if __name__ == '__main__':
  if len(sys.argv) < 3:
    print('Usage: ./binner.py <input.csv> <num_bins> <feature_num>')
  else:
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
