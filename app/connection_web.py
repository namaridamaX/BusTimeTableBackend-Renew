import urllib
import urllib.request as req
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_pdf():
    WEB_URL = "https://www.chitose.ac.jp/info/access"
    SAVE_URL = "pdf/Bus.pdf"

    #サイトと接続
    res = req.urlopen(WEB_URL)
    soup = BeautifulSoup(res,"html.parser")
    result = soup.select("a[href]")

    #hrefタグの抽出
    link_list = []
    for link in result:
        href = link.get("href")
        link_list.append(href)

    #pdfファイルの抽出
    pdf_list = [temp for temp in link_list if temp.endswith('pdf')]
    print(pdf_list[0])

    #相対パスから絶対パスに変換
    abs_pdf_list = []
    for relative in pdf_list:
        temp_url = urljoin(WEB_URL, relative)
        abs_pdf_list.append(temp_url)
    print(abs_pdf_list)

    #pdfフォルダにBus.pdfとして保存
    urllib.request.urlretrieve(abs_pdf_list[0],SAVE_URL)
    print("saved!!")