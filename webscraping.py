import time
from datetime import datetime
import decimal
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib3
import conexao as cnx

# url = "http://transparencia.cebi.com.br/005/Despesa/BuscaPagamentos"
cur = cnx.conexao_destino.cursor()

if len(urllib3.__version__.split('.')) < 3:
    urllib3.__version__ = urllib3.__version__ + '.0'

def init(mes, driver):
    option = Options()
    option.headless = True
    # driver = webdriver.Chrome()

    # driver.get(url)

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

    df_full = pd.read_html((str(table).replace('.','')).replace(',','.'))[0]
    df = df_full[['Data', 'Empenho', 'Pago']]

    i = 0
    nempg_ant = None
    val_pag_ant = None

    for x in range(len(df)):
        data_pag = datetime.strptime(df.loc[i, ['Data']][0], '%d/%m/%Y')
        print(data_pag)
        nempg = int((df.loc[i, ['Empenho']][0]).replace('/2022',''))
        val_pag = (df.loc[i, ['Pago']][0]) + val_pag_ant if nempg_ant == nempg else ((df.loc[i, ['Pago']][0]))

        ordpg = cur.execute(f"""SELECT ORDPG  from ordpag WHERE ordpg in (select ordpg from subord where pkemp in (select pkemp from despes where nempg = '{nempg}' 
                                and tpem <> 'EX')) and valor = '{val_pag}' and CAST(SUBSTRING(DATAE FROM 6 FOR 2) AS integer) = {str(mes)}""").fetchone()
        
        if ordpg != None:
            ordpg = ordpg[0]
            cur.execute(f"""update ordpag set dtpag = '{data_pag}', datae = '{data_pag}' where ordpg = '{ordpg}'""")

            cur.execute(f"""update cheqord set dtlan = '{data_pag}' where ordpg = {ordpg}""")


            cur.execute(f"""update DESSUB set dtpag = '{data_pag}' WHERE pkemp IN (SELECT pkemp FROM SUBORD WHERE ordpg = '{ordpg}') and vadem = '{val_pag}'
                            and CAST(SUBSTRING(VENCI FROM 6 FOR 2) AS integer) = {str(mes)}""")
        else:
            pass

        i += 1
        nempg_ant = nempg
        val_pag_ant = val_pag
    cnx.commit()

def init_ex(mes, driver):
    option = Options()
    option.headless = True
    # driver = webdriver.Chrome()

    # driver.get(url)

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
                                    //select[@class='form-control']//option[text()='Despesa Extra']''').click()

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

    df_full = pd.read_html((str(table).replace('.','')).replace(',','.'))[0]
    df = df_full[['Data', 'Empenho', 'Pago']]

    i = 0
    nempg_ant = None
    val_pag_ant = None

    for x in range(len(df)):
        data_pag = datetime.strptime(df.loc[i, ['Data']][0], '%d/%m/%Y')
        print(data_pag)
        nempg = int((df.loc[i, ['Empenho']][0]).replace('/2022',''))
        val_pag = (df.loc[i, ['Pago']][0]) + val_pag_ant if nempg_ant == nempg else ((df.loc[i, ['Pago']][0]))

        ordpg = cur.execute(f"""SELECT ORDPG  from ordpag WHERE ordpg in (select ordpg from subord where pkemp in (select pkemp from despes where nempg = '{nempg}' 
                                and tpem = 'EX')) and valor = '{val_pag}'""").fetchone()
        
        if ordpg != None:
            ordpg = ordpg[0]
            cur.execute(f"""update ordpag set dtpag = '{data_pag}', datae = '{data_pag}' where ordpg = '{ordpg}'""")

            cur.execute(f"""update cheqord set dtlan = '{data_pag}' where ordpg = {ordpg}""")

            cur.execute(f"""update DESSUB set dtpag = '{data_pag}' WHERE pkemp IN (SELECT pkemp FROM SUBORD WHERE ordpg = '{ordpg}') and vadem = '{val_pag}'""")
        else:
            pass

        i += 1
        nempg_ant = nempg
        val_pag_ant = val_pag
    cnx.commit()