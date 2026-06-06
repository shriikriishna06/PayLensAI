import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split  
from joblib import dump
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "dataset/india_job_market_2026_expanded.xlsx")

data = pd.read_excel(file_path) 

df=pd.DataFrame(data)
# Remove content in brackets from Company_Type
df['Company_Type'] = df['Company_Type'].str.replace(r'\s*[\(\[].*?[\)\]]', '', regex=True).str.strip()
#encodes the categorical values
encoded_data=pd.get_dummies(df,columns=["Role","Location","Education","Company_Type"],dtype=int)

model=LinearRegression()

X=encoded_data.drop(columns=["Salary_LPA"])
y=encoded_data["Salary_LPA"]
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

#model is trained on the dataset
model.fit(X_train,y_train)
# dump(model,"backend/model/model.pkl")
