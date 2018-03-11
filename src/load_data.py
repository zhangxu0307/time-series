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




if __name__ == '__main__':

    filePath1 = "../data/daily-minimum-temperatures-in-me.csv"
    filePath2 = "../data/first-column-monthly-average-cos.csv"
    ts = read_from_csv(filePath2, "%Y-%m-%d", columnsName=["val1", "val2"])
    print(ts)
