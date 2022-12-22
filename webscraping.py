import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib3
import conexao as cnx

url = "http://transparencia.cebi.com.br/005/Despesa/BuscaPagamentos"
cur = cnx.conexao_destino.cursor()

if len(urllib3.__version__.split('.')) < 3:
    urllib3.__version__ = urllib3.__version__ + '.0'

def init(mes):
    option = Options()
    option.headless = True
    driver = webdriver.Chrome()

    driver.get(url)
    time.sleep(2)

    driver.find_element("xpath",f'''//div[@class='page-container']//div[@class='page-content']//form
                                    //div[@class='container']//div[@class='tab-pane active']//div[@class='tools']
                                    //div[@class='portlet light bordered']//div[@class='portlet-body']
                                    //div[@class='portlet-body form']//div[@class='row']//div[@class='col-md-12']
                                    //div[@class='form-group padLeft10']//div[@class='col-md-2']//div
                                    //select[@class='form-control']//option[@value='{(mes)}']''').click()

    driver.find_element("xpath",'''//div[@class='page-container']//div[@class='page-content']//form
                                    //div[@class='container']//div[@class='tab-pane active']//div[@class='tools']
                                    //div[@class='portlet light bordered']//div[@class='portlet-body']
                                    //div[@class='portlet-body form']//div[@class='row']//div[@class='col-md-6 col-sm-6']
                                    //div[@class='col-md-5 padLeft25']//div[@class='form-group']//div
                                    //select[@class='form-control']//option[text()='Empenhos']''').click()

    driver.find_element("xpath",'''//div[@class='page-container']//div[@class='page-content']//form
                                    //div[@class='container']//div[@class='tab-pane active']//div[@class='tools']
                                    //div[@class='portlet light bordered']//div[@class='portlet-body']
                                    //div[@class='portlet-body form']//div[@class='row']//div[@class='col-md-12']
                                    //div[@class='col-md-1']//div[@class='form-group']''').click()

    element = driver.find_element("xpath",'''//div[@class='page-container']//div[@class='page-content']//form
                                    //div[@class='container']//div[@class='tab-pane active']//div[@class='portlet box blue']
                                    //div[@class='portlet-body']//div[@class='table-scrollable']''')

    html_content = element.get_attribute('outerHTML')

    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    df_full = pd.read_html(str(table))[0]
    df = df_full[['Data', 'Empenho', 'Pago']]
    i = 0

    for x in range(len(df)):
        data_pag = df.loc[i, ['Data']][0]
        nempg = df.loc[i, ['Empenho']][0]
        val_pag = df.loc[i, ['Pago']][0]
        
        cur.execute(f"update")
        cur.execute(f"update")
        cur.execute(f"update")
        cur.execute(f"update")
        cur.execute(f"update")
        i += 1

    cnx.commit()
    time.sleep(2)
    driver.quit()