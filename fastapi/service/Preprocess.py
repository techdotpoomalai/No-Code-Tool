import pandas as pd
import os

from Nocodemodel import Nocodemodel

class Preprocess (Nocodemodel):

    def __init__(self):
        super().__init__()
        self.preprocees_df=Nocodemodel.load_df

    def preprocess_data(self):
        return self.preprocees_df
    
    def preprocess(self,cols,prepros):
        try:
            file=os.listdir("Document")
            df = pd.read_csv(f"Document/"+file[0])
            for pross in prepros:
                if pross == 'onehot_encode':
                    df_encoded=pd.get_dummies(df, columns=cols)
                    df=pd.concat([df,df_encoded],axis=1)
                elif pross == 'lable_encode':
                    label_encoder = LabelEncoder()
                    for col in cols:
                        df[col] = label_encoder.fit_transform(df[col])
                else:
                    df=df.drop([cols],axis=1,inplace=True)
            df.to_csv(f"Document/"+file[0])       
            records = df.to_dict("records")
            return records
        except:
            return []