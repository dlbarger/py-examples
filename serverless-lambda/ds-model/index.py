#-----------------------------------------------------------------------------#
#   Script:     index.py
#   Author:     Dennis Barger, SEI
#   Created:    8/17/18
#   Source:     ds-model/index.py
#
#   Description:
#   Cluster Iris dataset using k-means algorithm.  Script is part of the Decision
#   Support AWS Prototype solution.
#-----------------------------------------------------------------------------#
try:
    import unzip_requirements
except ImportError:
    pass

import pandas as pd
from sklearn.cluster import KMeans
from StringIO import StringIO
import boto3

#-----------------------------------------------------------------------------#
#   User Defined Functions
#-----------------------------------------------------------------------------#

def putS3Object(data, bucket, key):
    try:
        s3 = boto3.resource('s3')
        csv_buffer = StringIO()
        data.to_csv(csv_buffer)
        s3.Object(bucket, key).put(Body = csv_buffer.getvalue())
        return(0)
    except Exception as e:
        print(e)
        return(1)

def getS3Object(bucket, key):
    try:
        s3 = boto3.resource('s3')
        obj = s3.Object(bucket, key)
        body = obj.get()['Body'].read()
        return(body)
    except Exception as e:
         print(e)
         return(1)
            
def runModel(event):
    try:
        # Get s3 object and convert to dataframe
        df = getS3Object(event['bucket'], event['stage_key'])
        df = StringIO(df)
        df = pd.read_csv(df)

        # Run kmeans algorithm
        kmeans = KMeans(n_clusters=3).fit(df[["sepal_length", "sepal_width", "petal_length", "petal_width"]])
        df['cluster'] = kmeans.labels_

        # Put revised dataset in s3 bucket
        resp = putS3Object(df, event['bucket'], event['output_key'])
        if resp == 0:
            errFlag = 0
            errMessage = "Successful S3 PUT"
        else:
            errFlag = 1
            errMessage = "Failed to PUT file"

        resp = {
            "bucket": event['bucket'],
            "input_key": event['input_key'],
            "stage_key": event['stage_key'],
            "output_key": event['output_key'],
            "error_flag": errFlag,
            "error_message": errMessage
        } 

        return(resp) 
    except Exception as e:
        print(e)
        raise e        

#-----------------------------------------------------------------------------#
#   Lambda handler for model logic
#-----------------------------------------------------------------------------#

def main(event, context):
    try:
        resp = runModel(event)
        return(resp)
    except Exception as e:
        raise e 

if __name__ == "__main__":

    event = {
        'bucket': 'barger-training',
        'input_key': 'data/outputs/iris_stage.csv',
        'stage_key': 'data/outputs/iris_stage.csv',
        'output_key': 'data/outputs/iris_output.csv'
    }

    context = {'context':'NA'}
    main(event, context)
