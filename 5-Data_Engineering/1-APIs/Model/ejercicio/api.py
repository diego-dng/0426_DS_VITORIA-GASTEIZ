from flask import Flask, jsonify, request
import pickle
import pandas as pd
import sqlite3


app = Flask(__name__)
app.config["DEBUG"] = True

def crear_db():
    df = pd.read_csv("data/advertising.csv", index_col= 0)
    df["newpaper"] = df["newpaper"].str.replace("s", "").astype(float)
    con = sqlite3.connect("data/adv.db")
    cursor = con.cursor()
    df.to_sql("advertising", con, if_exists= "replace", index= False)
    con.close()
    return "base de datos preparada"    




@app.route("/", methods = ["GET"])
def main():
    res = crear_db()
    return "API" + res

# INGEST
@app.route("/ingest", methods = ["POST"])
def ingest():
    #http://127.0.0.1:5000/ingest
    """
    {'data': [[100, 100, 200, 3000], [200, 230, 500, 4000]]}
    """
    try:
        nuevos_r = request.get_json().get("data", None)
        con = sqlite3.connect("data/adv.db")
        cursor = con.cursor()
        query = "Insert into advertising values(?,?,?,?)"
        for i in nuevos_r:
            cursor.execute(query, i)
            con.commit()
            
        con.close()
        return {'message': 'Datos ingresados correctamente'}, 200
    except Exception as e:
        return {"error":str(e)}, 500



# PREDICT
@app.route("/predict", methods = ["GET"])
def predict():
    # http://127.0.0.1:5000/predict
    """
        {"data":[[100, 100, 200]]}
    """
    model = pickle.load(open('data/advertising_model.pkl','rb'))
    lista = request.get_json().get("data", None)

    if lista is None:
        return "Missing args, the input values are needed to predict"
    else: 
        prediction = model.predict(lista)
        return jsonify({"prediction":str(round(prediction[0],2)) + 'k €'})
    

# RETRAIN
@app.route("/retrain", methods = ["GET"])
def retrain():
    # http://127.0.0.1:5000/retrain

    try: 
        con = sqlite3.connect("data/adv.db")
        cursor = con.cursor()
        query = "select * from advertising"
        resp = cursor.execute(query).fetchall()
        df = pd.DataFrame(resp)
        model = pickle.load(open('data/advertising_model.pkl','rb'))
        model.fit(df.iloc[:, :-1], df.iloc[:, -1])

        return {'message': 'Modelo reentrenado correctamente.'}, 200
    except Exception as e:
        return {"error": str(e)}, 500
        

app.run(port= 8000)

