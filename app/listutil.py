import datetime
import json
import os.path
import re
import pytz
import tabula
import pandas as pd
import PyPDF2
from datetime import datetime, timedelta, timezone
PDF_PATH = "pdf/Bus.pdf"


# PDFファイルを読み取りList型にする
def PdfToList():
    dfs = tabula.read_pdf(PDF_PATH, lattice=True, pages=1)
    none_null_df_list = [df.dropna(axis=1) for df in dfs]
    bus_list = [none_null_df_list.pop(0), none_null_df_list.pop(0)]
    return bus_list


# 期限の日にちを取得して,その日と比較する
def SerchPdf():
    FullWidthDigits = "０１２３４５６７８９"
    HalfWidthDigits = "0123456789"
    conv_map = str.maketrans(FullWidthDigits,HalfWidthDigits)
    dt_now = datetime.now(pytz.timezone('Asia/Tokyo')) # 現在の時間
    if (os.path.getsize(PDF_PATH) == 0): return True
    with open(PDF_PATH,"rb") as f:
        reader = PyPDF2.PdfReader(f)
        page = reader.pages[0] # PyPDF2がversion3.0に変更によりこっちを使うようになりました
        pdf_text = page.extract_text() # PyPDF2がversion3.0に変更によりこっちを使うようになりました]
        seikiList = re.findall('\d+月\d+日', pdf_text) # 正規表現でListから期限を抜き出す
        trans_data = seikiList[len(seikiList)-1]
        chenged_data = str(dt_now.year) + "年" + trans_data.translate(conv_map) # y年m月d日に変換

        bus_pdf_date = datetime.strptime(chenged_data,'%Y年%m月%d日') # date型に変換

        #timezoneの付与
        jst_timedelta = timedelta(hours=+9)
        jst = timezone(jst_timedelta, 'JST')
        bus_pdf_date = bus_pdf_date.astimezone(jst)
        if bus_pdf_date < dt_now : return True

        return False

def get_time(start, goal, time, bus_list):
    # time = "12:00"
    # bus_list[start] = "13:00"
    index_array = []

    want_date_time = datetime.strptime(time, "%H:%M") # 文字列型をdate型に変換
    print("want_date_time" + str(want_date_time))

    # bus_listから時刻を抜き出し、比較してindex_arrayに行番号を入れていく
    for i, x in enumerate(bus_list[start]) :

        y = bus_list[goal][i]
        if(x != '-' and x != '' and y != '-' and y != '') :

            bus_list_date_time = datetime.strptime(x, "%H:%M")
            print("bus_list_date_time" + str(bus_list_date_time))

            if(want_date_time < bus_list_date_time) :
                index_array.append(i)

                if(len(index_array) == 3) : # 3つ揃ったらreturn
                    return index_array

    # 3つ揃わなかった場合、残っているところに100を入れる
    for i in range(0, 3-len(index_array) ) :
        index_array.append(100)

    return index_array

def translate_json(start, goal, index_array, bus_list) :

    dict_bus_time = {
        "start_time": {
            "1": bus_list[start][index_array[0]],
            "2": bus_list[start][index_array[1]],
            "3": bus_list[start][index_array[2]]
        },
        "goal_time": {
            "1": bus_list[goal][index_array[0]],
            "2": bus_list[goal][index_array[1]],
            "3": bus_list[goal][index_array[2]]
        }
    }
    json_time_data = json.dumps(dict_bus_time, ensure_ascii=False)

    return json_time_data
