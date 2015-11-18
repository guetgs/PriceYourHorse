import pandas as pd
from kmeans_horses import Kmeans_DF


df = pd.read_json('Processor_input_dataframe.json')
max_age = max(df['Age'].values)
max_delta_h = max(df['Height (hh)']) - min(df['Height (hh)'])


def horse_horse_distance(series1, series2):
    '''
    INPUT: pandas series, pandas series
    OUTPUT: float

    Calculates a distance measure based on equality of categorical
    data and normalized difference for numeric data.
    '''
    dist = 1
    N = 8.
    for col in ['Breed', 'Color', 'Pedigree', 'Sex']:
        if (pd.isnull(series1[col])) or (pd.isnull(series2[col])):
            N -= 1
        elif series1[col] != series2[col]:
            dist += 1
    if not (pd.isnull(series1['Height (hh)']) or
            pd.isnull(series2['Height (hh)'])):
        dist += abs(series1['Height (hh)'] - series2['Height (hh)'])\
                / max_delta_h
    else:
        N -= 1
    if not (pd.isnull(series1['Temperament']) or
            pd.isnull(series2['Temperament'])):
        dist += abs(series1['Temperament'] - series2['Temperament'])
    else:
        N -= 1
    if not (pd.isnull(series1['Age']) or pd.isnull(series2['Age'])):
        dist += abs(series1['Age'] - series2['Age']) / max_age
    else:
        N -= 1
    return (dist / N - 1. / 8) * 8. / 7

if __name__ == '__main__':
    for k in [50, 100, 200]:
        filename = 'Centroids_' + str(k) + '.json'
        kmeans = Kmeans_DF(df, k, horse_horse_distance)
        centroids = kmeans.get_centroids()
        centroids.to_json(filename)
        print(str(k) + ' is done...')
