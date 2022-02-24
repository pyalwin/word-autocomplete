import pandas as pd
import Levenshtein as lev

class WordProcessor:
    def __init__(self):
        self.df = pd.DataFrame()

    def load_file(self,filepath):
        self.df = pd.read_csv(filepath, sep='\t', names=['word', 'freq'])
        self.df.dropna(inplace=True)

    def search_string(self,word):
        # Find the lavenshtein ratio between the words in source and given string
        self.df['ratio'] = self.df['word'].map(lambda x: lev.ratio(x, word))
        # Sort the results by ration and then by freq and return top 25 results
        return self.df.sort_values(by=['ratio','freq'], ascending=False).head(25)['word'].tolist()

    
