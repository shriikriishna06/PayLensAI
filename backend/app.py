import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
from fastapi.responses import FileResponse
from model.train import encoded_data

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)
#load model
model=joblib.load(r"model\model.pkl")
X=encoded_data.drop(columns=["Salary_LPA"])


#pydantic model for validation
class SalaryInput(BaseModel):
    Experience:float
    Role:str
    Location:str
    Education:str
    Company_Type:str


#API
@app.post("/predict")
def predict(request:SalaryInput):
    try:
        user_input = pd.DataFrame([{
        "Experience": request.Experience,
        "Role": request.Role,
        "Location": request.Location,
        "Education": request.Education,
        "Company_Type": request.Company_Type
        }])

        user_encoded = pd.get_dummies(user_input, dtype=int)
        user_encoded = user_encoded.reindex(
        columns=X.columns,
        fill_value=0
        )
        #prediction on user input
        sal=model.predict(user_encoded)
        
        
        return {"salary": int(sal[0])}
    except Exception as e:
        return {"error":str(e)}

# @app.get("/")
# def home():
#     return FileResponse("index.html")
# @app.get("/script.js")
# def script():
#     return FileResponse("script.js")
