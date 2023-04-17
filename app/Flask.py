from flask import *
import connection_web
from flask_cors import CORS
import pdf_tolist
import pandas as pd



app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def send_table():

        # jsonデータの取得と文字列型に変換して変数に格納
        # start_json_data = request.json['start']
        start_data = '本部棟発\rMAIN CAMPUS' # 出発駅の情報 start_data = '千歳駅発\rChitose Sta.'
        # goal_json_data = request.json['goal']
        goal_data = '南千歳駅着\rMinami-Chitose Sta.'  # 到着駅の情報 goal_data = '本部棟着\rMAIN CAMPUS'
        # time_json_data = request.json['time']
        time_data = '12:00'  # 出発時間の情報 time_data = '12:00'

        dfs = pdf_tolist.ReadPdf()
        df_list = pdf_tolist.ListDfs(dfs)
        pdf_tolist.SerchPdf()
        bus_list = pd.concat([df_list[0], df_list[1]], axis=1)
        index_array = pdf_tolist.get_time(start_data, goal_data, time_data, bus_list)
        print(bus_list)
        # json_data = bus_list.to_json()

        print("POSTが実行されました")

        return index_array


@app.route('/', methods=["GET"])
def send_tabel():

        if( pdf_tolist.SerchPdf() ):

            connection_web.get_pdf()  #バスの時刻表を取得
            print("true")

        # jsonデータの取得と文字列型に変換して変数に格納
        start_json_data = request.json['start']
        start_data = str(start_json_data) # 出発駅の情報 start_data = '千歳駅発\rChitose Sta.'
        goal_json_data = request.json['goal']
        goal_data = str(goal_json_data) # 到着駅の情報 goal_data = '本部棟着\rMAIN CAMPUS'
        time_json_data = request.json['time']
        time_data = str(time_json_data) # 出発時間の情報 time_data = '12:00'

        dfs = pdf_tolist.ReadPdf()
        df_list = pdf_tolist.ListDfs(dfs)
        pdf_tolist.SerchPdf()
        bus_list = pd.concat([df_list[0], df_list[1]], axis=1)
        print(bus_list)
        json_data = bus_list.to_json()

        print("POSTが実行されました")

        return json_data


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080)



