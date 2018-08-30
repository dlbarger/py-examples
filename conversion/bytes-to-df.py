'''
Script:     bytes-to-df.py
Author:     Dennis Barger
Created:    8/29/2018

Description:
Converts bytes object to pandas data frame.
'''

import pandas as pd
import boto3
from io import StringIO

def getS3Object(bucket, key):
    try:
        s3 = boto3.resource('s3')
        obj = s3.Object(bucket, key)
        body = obj.get()['Body'].read()
        return(body)
    except Exception as e:
        print(e)
        return(1)

def main(bucket, key):
    try:
        d = getS3Object(bucket, key)
        t = type(d)
        print(t)
        print("Help")

        s = str(d, 'utf-8')
        ds = StringIO(s)
        df = pd.read_csv(ds)
        #print(pd.unique(df['species']))
        col = df.columns
        print(col[1])
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main('barger-training','data/inputs/iris.csv')
