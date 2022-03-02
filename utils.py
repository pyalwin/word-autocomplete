import pandas as pd
import numpy as np
# import Levenshtein as lev

def memoize(func):
    mem = {}
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in mem:
            mem[key] = func(*args, **kwargs)
        return mem[key]
    return memoizer

class WordProcessor:
    def __init__(self):
        self.df = pd.DataFrame()

    def load_file(self,filepath):
        self.df = pd.read_csv(filepath, sep='\t', names=['word', 'freq'])
        self.df.dropna(inplace=True)


    @memoize    
    def calculate_distance(self,a, b):
        ## Create m*n matrix
        distances = np.zeros((len(a) + 1, len(b) + 1))

        # Set the first column to index
        for x in range(len(a) + 1):
            distances[x][0] = x

        # Set the first row to index
        for y in range(len(b) + 1):
            distances[0][y] = y
            
        i = 0
        j = 0
        k = 0
        
        for x in range(1, len(a) + 1):
            for y in range(1, len(b) + 1):
                if (a[x-1] == b[y-1]):
                    distances[x][y] = distances[x - 1][y - 1]
                else:
                    i = distances[x][y - 1]
                    j = distances[x - 1][y]
                    k = distances[x - 1][y - 1]
                    
                    if (i <= j and i <= k):
                        distances[x][y] = i + 1
                    elif (j <= i and j <= k):
                        distances[x][y] = j + 1
                    else:
                        distances[x][y] = k + 1
        return distances[len(a)][len(b)]

    @memoize
    def search_string(self,word):
        # Find the lavenshtein ratio between the words in source and given string
        # self.df['ratio'] = self.df['word'].map(lambda x: lev.ratio(x, word))
        print(self.df.head())
        self.df['distance'] = self.df['word'].map(lambda x: self.calculate_distance(x, word))
        # self.df['distance'] = self.df['word'].map(lambda x: levenshtein(x, word))
        # Sort the results by ration and then by freq and return top 25 results
        print(self.df.sort_values(by=['distance', 'freq'],ascending=[True, False]).head())
        return self.df.sort_values(by=['distance','freq'],ascending=[True, False]).head(25)['word'].tolist()

