import urllib
import urllib.request as req
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_pdf():
    url = "https://www.chitose.ac.jp/info/access"
    savefile = "pdf/Bus.pdf"

    #サイトと接続
    res = req.urlopen(url)
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
        temp_url = urljoin(url, relative)
        abs_pdf_list.append(temp_url)
    print(abs_pdf_list)

    #pdfフォルダにBus.pdfとして保存
    urllib.request.urlretrieve(abs_pdf_list[0],savefile)
    print("saved!!")