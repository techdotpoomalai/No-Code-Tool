import os
import pandas as pd

class Nocodemodel():
    def __init__(self) :
        file=os.listdir("Document")
        df = pd.read_csv(f"Document/"+file[0])
        self.df=df

    
    def load_df(self):
        return self.df