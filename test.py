#!/usr/bin/python3

import regression as rg

def main():
  features = []
  params = []
  print("Test: classify should classify correctly")
  features = [0.2, 0.4]
  params = [1, 1, 1]
  print('Passed' if rg.classify(features, params) == 1.6 else 'Failed')

if __name__ == '__main__':
  main()
