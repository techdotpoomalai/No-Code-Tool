import json
from fastapi import FastAPI,Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import pandas as pd
import requests
import pickle
import base64
import os
import io

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React app's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers (Authorization, etc.)
)


@app.get("/")
async def main():
    return {"message": "Hello dWorld"}

@app.post("/file_upload")
async def upload_file(file: UploadFile= File(...)):
    try:
        file_location=f"Document/{file.filename}"
        with open(file_location, 'wb') as f:
            f.write(await file.read())
        
        return {"message":"success"}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/fetch_data")
async def main():
    try:
        file=os.listdir("Document")
        df = pd.read_csv(f"Document/"+file[0])
        records = df.to_dict("records")
        json_string = json.dumps(records[0])
        json_string_corrected = json_string.replace("\\", "")
        # print(json_string)
        # json_string_corrected=''
        # for x in json_string:
        #     if x == '\\':
        #         print(f'Normal; {x}')
        #     else:
        #         print(f'Ubnormal ; {x}')
        return {"message":"success"}
    except:
        return []
    
@app.post("/preprocess")
async def preprocess(colunms: list = Form(...), preprocess: list = Form(...)):
    cols=colunms
    process=preprocess
    try:
        file=os.listdir("Document")
        df = pd.read_csv(f"Document/"+file[0])
        for pross in preprocess:
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
    
@app.post("/analysis")
async def preprocess(colunms: list = Form(...), analysis: str = Form(...)):
    cols=colunms
    analy=analysis
    try:
        file=os.listdir("Document")
        df = pd.read_csv(f"Document/"+file[0])
        plt.figure(figsize=(6, 4))
        plt.plot(df[cols[0]], df[[cols[1]]])
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()
        img_str = base64.b64encode(buf.getvalue()).decode("utf-8")
        return {"src":"data:image/png;base64,{img_str}"}
    except:
        return ''
    
@app.post("/train")
async def preprocess(colunms: str = Form(...), train: str = Form(...)):
    train=train
    try:
        file=os.listdir("Document")
        df = pd.read_csv(f"Document/"+file[0])
        y=df.pop(colunms)
        X=df

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        models = {
            'Logistic Regression': LogisticRegression(max_iter=200),
            'Random Forest': RandomForestClassifier(),
            'Support Vector Classifier': SVC()
        }
        r2=''
        for name, model in models.items():
            if name==train:
                model.fit(X_train,y_train)
                y_pred = model.predict(X_test)
                with open('Document/model.pkl', 'wb') as file:
                    pickle.dump(model, file)
            r2 = r2_score(y_test, y_pred)
        return r2
    except:
        return ''
    

@app.get("/fetch_pickle")
async def fetch_picklefile():
    
    try:
        response = requests.get('Document/model.pkl')
        with open('model.pkl', 'wb') as f:
            f.write(response.content)
        return {"message":"success"}
    except:
        return {"message":"fail"}

@app.post("/predictions")
async def preprocess(value: list = Form(...)):
    pass