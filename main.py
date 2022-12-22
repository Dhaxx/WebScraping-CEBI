import webscraping
driver = webscraping.webdriver.Chrome()
driver.get("http://transparencia.cebi.com.br/005/Despesa/BuscaPagamentos")

def main():
    i = 0

    for x in range(10):
        i += 1
        webscraping.init(i, driver)
        webscraping.init_ex(i, driver)
        print(f'{i}º mês feito!')

if __name__ == "__main__":
    main()