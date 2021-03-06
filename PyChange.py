"""
Author: Thomas Gumbsch
Date: 16.3.2017
Lab: Machine learning and computational biology
Insitute: D-BSSE at ETHZ
"""
import numpy as np
import pandas as pd
import argparse

from lib.Preprocessing import preprocessing


from lib.cpp_kernel.cppChange import CppChange


def PyChange(seq, transform='std', method='CUSUM'):
    """
    Changepoint detection of input sequence
    """
    tseq = preprocessing(seq, transform)
    cp = solve(tseq, method)
    return cp


def solve(seq, method):
    """
    Apply method to sequence
    """
    cp = []
    if method in ['MaChaMP', 'CUSUM', 'EWMA', 'QChart']:
        C = CppChange(seq, method)
        cp = C.changepoints
        del C
    else:
        print("Not a known module")
        cp = []
    return cp


def init_random_csv():
    """
    Sample csv data set
    """
    d = pd.DataFrame({'A': np.concatenate((np.cumsum(np.random.randn(50)), np.cumsum(np.random.randn(50) + 3), np.cumsum(np.random.randn(100)))), 'B': np.concatenate((['C1'] * 100, ['C2'] * 100)), 'T': range(200)})
    d.to_csv('random.csv')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Computes changes in time sereis with python with different methods')
    parser.add_argument('--filename', help='Filename with .csv extension as from QtFy.')
    parser.add_argument('--cell', help='Cellid column name, separate time series have diffrent cell ids.')
    parser.add_argument('--values', help='Expression level column name')
    parser.add_argument('--time', help='timepoint column name')
    parser.add_argument('--method', choices=['MaChaMP', 'CUSUM', 'EWMA', 'Q-Chart'], default='MaChaMP', help='Changepoint detection method')
    parser.add_argument('--preprocessing', choices=['none', 'diff', 'logdiff', 'percdiff', 'logpercdiff'], default='none', help='transformation of time series')
    args = parser.parse_args()
    name = str(args.filename)
    cell = str(args.cell)
    TF = str(args.values)
    method = str(args.method)
    time = str(args.time)
    transform = str(args.preprocessing)

    # init_random_csv()

    data = pd.read_csv(name)
    cells = data[cell].unique()
    changes = pd.DataFrame({'CellID': [], 'CP': []})

    for c in cells:
        seq = data[data[cell] == c][TF].dropna().values.tolist()
        cp = PyChange(seq, transform, method)
        changes = pd.concat((changes, pd.DataFrame({'CellID': [c] * len(cp), 'CP': cp, 'Timepoint': [data[(data[cell] == c) & (data[TF] == seq[change])][time].values.tolist()[0] for change in cp]})), ignore_index=True)

    changes.to_csv('Changes' + name)

    # Iterate over all unique Cell ids, get time series and apply Test
    # save in changes
