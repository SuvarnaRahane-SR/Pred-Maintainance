from flask import *
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle
app = Flask(__name__)

def predictinpdata(input_df):
    sc=pickle.load(open('sc.pkl',"rb"))
    ct=pickle.load(open("coltransformer.pkl","rb"))
    gb=pickle.load(open("gb.pkl","rb"))
    x=ct.transform(input_df)
    x=pd.DataFrame(x,columns=['Type', 'Air temperature [K]', 'Process temperature [K]',
       'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]', 'TWF', 'HDF', 'PWF', 'OSF', 'RNF'])
    x.iloc[:,:]=sc.transform(x.iloc[:,:])
    ans=gb.predict(x)[0]
    if ans==0:
        return "Machine is Failed."
    else:
        return "Machine is Active."

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/reglink",methods=["POST"])
def getinputdata():
    Type=request.form["Type"]
    ATemperature=float(request.form["Air temperature [K]"])
    PTemperature=float(request.form["Process temperature [K]"])
    RSpeed=float(request.form["Rotational speed [rpm]"])
    Torque=float(request.form["Torque [rnm]"])
    Twear=request.form["tool wear [min]"]
    TWF=request.form["TWF"]
    HDF=request.form["HDF"]
    HWF=request.form["PWF"]
    OSF=request.form["OSF"]
    RNF=request.form["RNF"]
    input_df=pd.DataFrame(data=[[Type,ATemperature,PTemperature,RSpeed,Torque,Twear,TWF,HDF,HWF,OSF,RNF]],columns=['Type', 'Air temperature [K]', 'Process temperature [K]',
       'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]', 'TWF', 'HDF', 'PWF', 'OSF', 'RNF'])
    
    ans=predictinpdata(input_df)
    return render_template("display.html",data=ans)

    
if __name__ =='__main__':
    app.run(debug=True)