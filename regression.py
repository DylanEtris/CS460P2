#!/usr/bin/python3

import math
import preprocessor as pp
import pdb
import copy
import matplotlib.pyplot as plt
import numpy as np

def classify(features, constants):
  features = features[:]
  constants = constants[:]

  features.insert(0, 1.0)
  features = np.asarray(features)
  constants = np.asarray(constants)
  return np.dot(features, constants)  

# Function: getErrors
# Inputs: raw data, constant array
# Outputs: a list of errors [e1, e2, ...] for each example in dataset
# Purpose: Acquire a list of errors for linear regression
def getErrors(data, constants):
  data = copy.deepcopy(data)

  features = []
  errors = []
  value = 0.0
  constants = constants[:]
  for example in data:
    features = example[:-1]
    value = example[-1]
    errors.append(classify(features, constants) - value)
  return errors

# Function: getParameters
# Inputs: raw data
# Outputs: a list of parameters [c0, ...cn] for a linear equation
# Purpose: Trains the parameters given a dataset
def getParameters(data):
  data = copy.deepcopy(data)
  constants = []
  errors = []
  alpha = 0.0001
  num_features = len(data[0]) - 1

  # initialize constant array
  for i in range(num_features + 1):
    constants.append(1)

  for i in range(500):
    errors = getErrors(data, constants)

    for j in range(len(data[0])):
      for k in range(len(data)):
        # Error of example k times the jth feature of example k over m 
        constants[j] -= alpha * ((errors[k]*data[k][j]) / len(data)) 

  return constants    

# Function: getMSE
# Inputs: raw data, constants
# Outputs: mean squared error
# Purpose: Calculates the mean squared error given data and the line parameters
def getMSE(data, constants):
  data = copy.deepcopy(data)
  errors = getErrors(data, constants)
  total = 0.0
  for error in errors:
    total += error ** 2
  return total / len(data)

def baseExpansion(data, power):
  data = copy.deepcopy(data)
  new_data = []
  for val in data:
    new_data.append([])
    for i in range(power):
      new_data[-1].append(val ** (i + 1))

  return new_data

def plot(path, data, params, power):
  # plot original data points
  x_axis = [example[0] for example in data]
  y_axis = [example[-1] for example in data]
  plt.plot(x_axis, y_axis, "b.")


  line_xvals = np.linspace(min(x_axis), max(x_axis), len(x_axis))
  line_xvals = line_xvals.tolist()
  #tmp = pp.normalize(line_xvals)
  #tmp = baseExpansion(tmp, power)

  tmp = baseExpansion(line_xvals, power)
  line_yvals = []
  for x in tmp:
    line_yvals.append(classify(x, params))
    
  plt.plot(line_xvals, line_yvals, "r-")
  plt.savefig(path)


def main():
  raw_data = pp.read_csv("./data_files/winequality-red.csv", True)

  # Normalize data
  data = copy.deepcopy(raw_data)
  num_features = len(data[0]) - 1
  for f in range(num_features):
    data = pp.normalize(data, f)

  # Train and Classify
  mse = 0.0
  params = []
  #params = getParameters(data)
  #mse = getMSE(data, params)

  # Part 1 report
  print("Part 1 params:")
  for param in params:
    print(param)
  print("Total Error Part 1:")
  print(mse)

  filename = "synthetic-1"
  raw_data = pp.read_csv("./data_files/" + filename + ".csv")

  # Normalize data
  data = copy.deepcopy(raw_data)
  num_features = len(data[0]) - 1
  for f in range(num_features):
    data = pp.normalize(data, f)

  # Base expansion
  power = 10
  new_data = [example[0] for example in data]
  new_data = baseExpansion(new_data, power)
  for i in range(len(data)):
    new_data[i].append(data[i][-1])

  pdb.set_trace()
  #Train and classify
  params = getParameters(new_data)
  mse = getMSE(new_data, params)

  # Part 2 report
  print("Part 2 params:")
  for param in params:
    print(param)
  print("Total Error Part 2; Base 2:")
  print(mse)
  plot("./data_plots/" + filename + ".png", raw_data, params, power)

if __name__ == '__main__':
  main()
