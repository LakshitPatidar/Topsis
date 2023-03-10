import sys
import os
import pandas as pd
from pandas.api.types import is_numeric_dtype
import math as m
import numpy as np


def topsis(weights, impacts, dataset):
    dataset.dropna(inplace=True)
    d = dataset.iloc[0:, 1:].values
    matrix = pd.DataFrame(d)
    if(len(matrix.columns)<3):
        print("Insufficient no of columns in dataset")
        exit()
    
    for i in range(0,len(matrix.columns)):
        if not(is_numeric_dtype(matrix[i])):
            print("Column contains non numeric values, pls insert numeric values only")
            exit()

    if(len(weights)!=(len(matrix.columns))):
        print("No of weights and impacts not equal to no columns")
        exit()
    
    for i in range(0,len(impacts)):
        if(impacts[i]!='+' and impacts[i]!='-'):
            print("Error!! impacts should be either + or -")
            exit()
    matrix = matrix.astype(float)
    sumOfSquares = []
    for col in range(0, len(matrix.columns)):
        X = matrix.iloc[0:, [col]].values
        sum = 0
        for value in X:
            sum = sum + m.pow(value, 2)
        sumOfSquares.append(m.sqrt(sum))

    j = 0
    while(j < len(matrix.columns)):
        for i in range(0, len(matrix)):
            matrix[j][i] = matrix[j][i]/sumOfSquares[j]
        j = j+1

    k = 0
    while(k < len(matrix.columns)):
        for i in range(0, len(matrix)):
            matrix[k][i] = matrix[k][i]*weights[k]
        k = k+1

    bestValue = []
    worstValue = []

    for col in range(0, len(matrix.columns)):
        Y = matrix.iloc[0:, [col]].values

        if impacts[col] == "+":
            maxValue = max(Y)
            minValue = min(Y)
            bestValue.append(maxValue[0])
            worstValue.append(minValue[0])

        if impacts[col] == "-":
            maxValue = max(Y)
            minValue = min(Y)
            bestValue.append(minValue[0])
            worstValue.append(maxValue[0])

    SiPlus = []
    SiMinus = []

    for row in range(0, len(matrix)):
        temp = 0
        temp2 = 0
        wholeRow = matrix.iloc[row, 0:].values
        for value in range(0, len(wholeRow)):
            temp = temp + (m.pow(wholeRow[value] - bestValue[value], 2))
            temp2 = temp2 + (m.pow(wholeRow[value] - worstValue[value], 2))
        SiPlus.append(m.sqrt(temp))
        SiMinus.append(m.sqrt(temp2))

    Pi = []

    for row in range(0, len(matrix)):
        Pi.append(SiMinus[row]/(SiPlus[row] + SiMinus[row]))

    Rank = []
    sortedPi = sorted(Pi, reverse=True)
    for row in range(0, len(matrix)):
        for i in range(0, len(sortedPi)):
            if Pi[row] == sortedPi[i]:
                Rank.append(i+1)

    newColNames = []
    for name in dataset.columns:
        newColNames.append(name)
    
    dataset['Topsis Score'] = Pi
    dataset['Rank'] = Rank

    newColNames.append('Topsis Score')
    newColNames.append('Rank')
    dataset.columns = newColNames
    return dataset