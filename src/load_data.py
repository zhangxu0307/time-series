import pandas as pd
from pandas import DataFrame, Series
import numpy as np
from datetime import datetime, timedelta

# 从csv文件中加载时间序列数据
def read_from_csv(filePath, dataFormat, columnsName=None):

    ts = pd.read_csv(filePath)
    featureNum = len(ts.columns)-1

    if columnsName:
        if len(columnsName) == featureNum:
            ts.columns = ["date"]+columnsName
        else:
            raise Exception("Invalid feature name!")

    else:
        ts.columns = ["date"]+["value"+str(i) for i in range(1, featureNum+1)]
    ts["date"] = pd.to_datetime(ts["date"], format=dataFormat)
    ts.index = ts["date"]
    del ts["date"]
    print("time series lenght:", len(ts))
    return ts

# 从时间序列数据中构造一般的ML训练数据
def build_trainset_from_ts(ts, n_in, n_out, dropnan=True):
    
    if not isinstance(ts.index, pd.DatetimeIndex):
        raise Exception("Invalid time series data type")
    n_vars = len(ts.columns)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(ts.shift(i))
        names += [('var%d(t-%d)' % (j + 1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(ts.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j + 1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j + 1, i)) for j in range(n_vars)]
    # put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg


if __name__ == '__main__':

    filePath1 = "../data/daily-minimum-temperatures-in-me.csv"
    filePath2 = "../data/first-column-monthly-average-cos.csv"
    ts = read_from_csv(filePath2, "%Y-%m-%d", columnsName=["val1", "val2"])
    print(ts)

    dataset = build_trainset_from_ts(ts, 5, 2, dropnan=True)
    print(dataset)
