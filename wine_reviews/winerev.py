import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
#import matplotlib.pyplot as plt

DATA_FILE = './data/winemag_reviews.csv'

def getData(data_file):
    try:
        data = pd.read_csv(data_file, sep = ',')
        return(data)
    except Exception as e:
        return(e)

def setHist(data, bins, xlabel, ylabel, title):
    import matplotlib.pyplot as plt
    try:
        range = ()
        plt.hist(data, bins, range)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.show()
    except Exception as e:
        return(e)

def runKMeansCluster(data, clusters):
    try:
        if isinstance(data, pd.DataFrame):
            kmeans = KMeans(n_clusters = clusters).fit(data)
            data['cluster'] = kmeans.labels_
            return(data)
        else:
            return('Warning:  No dataframe')
    except Exception as e:
        return(e)

def main(data):
    try:
        df_src = getData(data)
        df_input = df_src[['points','price']]
        df_input.dropna(inplace = True)
        df_output = runKMeansCluster(df_input, 5)
        return(df_output)
    except Exception as e:
        return(e)

if __name__ == '__main__':
    response = main(DATA_FILE)
    print(response.head(100))
else:
    print('Error with main()')
