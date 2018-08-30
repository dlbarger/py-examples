#-----------------------------------------------------------------------------#
#   Script:     index.py
#   Author:     Dennis Barger, SEI
#   Created:    8/17/18
#   Source:     ds-get-data\index.py
#
#   Description:
#   Ingest data from S3 source and transform.
#-----------------------------------------------------------------------------#
try:
    import unzip_requirements
except ImportError:
    pass
    
import pandas as pd
from StringIO import StringIO
import boto3

#-----------------------------------------------------------------------------#
#   User Defined Functions
#-----------------------------------------------------------------------------#

def putS3Object(data, bucket, key):
    '''
    Function:   putS3Object
    Arguments:  
    -   data = content to load into s3
    -   bucket = target s3 bucket
    -   key = target s3 file
    Return:
    -   Success = 0; Failure = 1    

    Description:
    Utilize boto3 package to put data into s3 object.
    '''
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
    '''
    Function:   getS3Object
    Arguments:  
    -   bucket = source s3 bucket
    -   key = source s3 file
    Return:
    -   Body = dataframe of s3 source file

    Description:
    Utilize boto3 package to get file from S3
    '''
    try:
        s3 = boto3.resource('s3')
        obj = s3.Object(bucket, key)
        body = obj.get()['Body'].read()
        return(body)
    except Exception as e:
         print(e)
         return(1)
            
#def fetchData(bucket, input_key, output_key):
def fetchData(event):
    '''
    Function:   main()
    Event Arguments:
    -   bucket = S3 bucket
    -   input_key = source S3 file
    -   stage_key = staged S3 file
    -   output_key = target S3 file

    Description:
    Main logic for model.
    '''
    try:
        # Get s3 object and convert to dataframe
        df = getS3Object(event['bucket'], event['input_key'])
        df = StringIO(df)
        df = pd.read_csv(df)
        df.columns = ['sepal_length','sepal_width','petal_length','petal_width','species']   

        # Put revised dataset in s3 bucket
        resp = putS3Object(df, event['bucket'], event['stage_key'])
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
        raise e    

#-----------------------------------------------------------------------------#
#   Lambda handler for model logic
#-----------------------------------------------------------------------------#

def main(event, context):
    try:
        resp = fetchData(event)
        return(resp)

    except Exception as e:
        raise e


if __name__ == "__main__":

    event = {
        'bucket': 'barger-training',
        'input_key': 'data/inputs/iris.csv',
        'stage_key': 'data/outputs/iris_stage.csv',
        'output_key': 'data/outputs/iris_output.csv'
    }

    context = {'context':'NA'}
    main(event, context)        
