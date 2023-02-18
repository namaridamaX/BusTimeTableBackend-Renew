import requests
import urllib.request

def get_pdf():
    url = "https://www.chitose.ac.jp/info/access"
    path = "//*[@id='paragraph_107_1615971519']/div/div/div[2]/a"
    savefile = "pdf/Bus.pdf"

    response = urllib.request.urlopen(url).read()
    urllib.request.urlretrieve(url,savefile)



    print(response)