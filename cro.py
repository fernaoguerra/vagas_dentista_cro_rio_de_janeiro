import requests
from bs4 import BeautifulSoup
import time
import csv
import shutil
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from credential import key

def getTable():
    options = Options()
    options.add_argument("--disable-popup-blocking")
    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)
    #browser = webdriver.Chrome(chromedriver)
    browser.get('http://www.sistemas-cro-rj.org.br/classificados/anuncio_pesquisar_resultado.php?cidade=93&bairro=&categoria=4&pesquisar=Pesquisar')
    time.sleep(5)

    soup = BeautifulSoup(browser.page_source, features="html.parser")

    table = soup.find("table", {"class": "adminlist"})
    #print (table)

    filename = "vagas_cro.csv"
    f =open(filename, "w")

    headers = "Cidade,Bairro,Categoria,Anuncio,id\n"
    f.write(headers)

    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    data = []

    amount = 0
    adId = []
    cidade =[]
    bairro =[]
    categoria =[]
    anuncio =[]

    for row in rows:
        cells = row.findAll("td")
        cidade = cells[0].find(text=True).replace("\n","").replace(",","")
        bairro = cells[1].find(text=True).replace("\n","").replace(",","")
        categoria = cells[2].find(text=True).replace("\n","").replace(",","")
        anuncio = cells[3].find(text=True).replace("\n","").replace(",","")
        adId = cells[4].a['href']
        url = "http://www.sistemas-cro-rj.org.br/classificados/" + adId
        data.append(cells)
        f.write(cidade + "," + bairro + "," + categoria + "," + anuncio + "," + url + "\n")
        amount= amount +1
    print (amount)
    f.close()
    compareVagas()
    shutil.copy('vagas_cro.csv', 'vagas_cro2.csv')
        


def compareVagas():
    s=open('vagas_cro.csv')
    try:
        o=open('vagas_cro2.csv')
    except:
        shutil.copy('vagas_cro.csv', 'vagas_cro2.csv')
        o=open('vagas_cro2.csv')

    csv_0 = csv.reader(s)
    csv_1 = csv.reader(o)

    list1= []
    list2= []

    for row in csv_0:
        list1.append(row[4])

    for row in csv_1:
        list2.append(row[4])

    difference = list((set(list1).difference(list2)))
    print(type(difference))
    print(difference)
    x=0
    for d in difference:
        print (str(difference[0]))

    s.close()
    o.close()

    #Print no telegram
    payload = " "
    payload = {'value1': difference}
    url = 'https://maker.ifttt.com/trigger/vagascro/with/key/'+key
    r = requests.post(url, data=payload)
    print (r)

getTable()
#compareVagas()
































