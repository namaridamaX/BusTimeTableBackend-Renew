import pandas as pd
from flask import Flask
# from flask_cors import CORS
import connection_web


app = Flask(__name__)
# CORS(app)
app.config['JSON_AS_ASCII'] = False

@app.route('/',methods=["GET"])
def send_table():

    #バスの時刻表を取得
    connection_web.get_pdf()


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080)



