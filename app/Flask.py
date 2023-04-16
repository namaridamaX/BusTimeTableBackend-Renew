from flask import Flask
from flask_cors import CORS
import connection_web
import pdf_tolist
import pandas as pd


app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

@app.route('/',methods=["GET"])
def send_table():

    if(pdf_tolist.SerchPdf()):
        #バスの時刻表を取得
        connection_web.get_pdf()
        print("true")

    dfs = pdf_tolist.ReadPdf()
    df_list = pdf_tolist.ListDfs(dfs)
    pdf_tolist.SerchPdf()
    bus_list = pd.concat([df_list[0], df_list[1]], axis=1)
    print(bus_list)
    pdf_tolist.SerchPdf()
    json_data = bus_list.to_json()

    return json_data


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080)



