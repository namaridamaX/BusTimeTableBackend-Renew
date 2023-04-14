import datetime
import os.path
import re
import pytz
import tabula
import pandas as pd
import PyPDF2
from datetime import datetime, timedelta, timezone
PDF_Path = "pdf/Bus.pdf"
def ReadPdf():
    # PDFファイルの読み取り（dfsの形式はList）
    dfs = tabula.read_pdf(PDF_Path, lattice=True, pages=1)
    return dfs
def ListDfs(dfs):
    df_list = [df.dropna(axis=1) for df in dfs]
    df_list = [df_list.pop(0), df_list.pop(0)]
    return df_list
def SerchPdf():
    FullWidthDigits = "０１２３４５６７８９"
    HalfWidthDigits = "0123456789"
    conv_map = str.maketrans(FullWidthDigits,HalfWidthDigits)
    dt_now = datetime.now(pytz.timezone('Asia/Tokyo')) #現在の時間
    if (os.path.getsize(PDF_Path) == 0): return True
    with open(PDF_Path,"rb") as f:
        reader = PyPDF2.PdfReader(f)
        page = reader.pages[0] #PyPDF2がversion3.0に変更によりこっちを使うようになりました
        pdf_text = page.extract_text() #PyPDF2がversion3.0に変更によりこっちを使うようになりました]
        seikiList = re.findall('\d+月\d+日', pdf_text)
        trans_data = seikiList[len(seikiList)-1]
        chenged_data = str(dt_now.year) + "年" + trans_data.translate(conv_map)

        bus_pdf_date = datetime.strptime(chenged_data,'%Y年%m月%d日')

        jst_timedelta = timedelta(hours=+9)
        jst = timezone(jst_timedelta, 'JST')
        bus_pdf_date = bus_pdf_date.astimezone(jst)
        if(bus_pdf_date < dt_now): return True
        return False