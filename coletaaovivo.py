from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import threading
import time
from time import sleep
from bs4 import BeautifulSoup




data = pd.read_excel('dados.xlsx', index_col=[0])

while True:
    try:
        #abre o aiscore
        options = Options()
        options.headless = True
        options.add_argument("--mute-audio")
        driver = webdriver.Chrome(executable_path="chromedriver.exe",options=options)
        driver.maximize_window()
        driver.implicitly_wait(10) 
        #pega todos os links ao vivo(com 85 min)
        while True:
            links = []
            tempos = []
            driver.get("https://www.google.com")
            driver.get("https://www.aiscore.com/pt/")
            i = 2
            total = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[2]/div[1]/div[2]/div[2]/ul/li[2]/span[2]').text
            itotal = total[1]
            while(i > 0):
                if total[i] != ")":
                    itotal = itotal + total[i]
                    i+=1
                else:
                    i = 0
            itotal = int(itotal)
            total = 0
            while(total<itotal):
                i = 0
                while(i < len(driver.find_elements_by_class_name("match-container"))):
                    link = driver.find_elements_by_class_name("match-container")[i].get_attribute('href')
                    sts = driver.find_elements_by_class_name("status")[i].text
                    container = driver.find_elements_by_class_name("match-container")[i]
                    j = 0
                    repet = False
                    while(j < len(links)):
                        if(link == links[j]):
                            repet = True
                        j+=1
                    if(repet == False):
                        inteiro = False
                        try:
                            if len(sts) < 3:
                                sts = int(sts)
                                inteiro = True
                            else:
                                sts = sts.replace('+','')
                                sts = int(sts)
                                inteiro = True
                        except:
                            pass
                        if inteiro == True:
                            ad = False
                            if sts >= 86 and sts <=88:
                                ad = True
                            if ad == True:
                                links.append(link)
                        total+=1
                        if(total > itotal+1):
                            i = len(driver.find_elements_by_class_name("match-container"))   
                    i+= 1
                sleep(1)
                driver.execute_script("arguments[0].scrollIntoView();", container)

            #em cada link pega os dados da partida
            x = 0
            while(x < len(links)):
                rep = False
                for i in data['link']:
                    if links[x] == i:
                        rep = True      
                if rep == False:
                    try:
                        driver.get(links[x]+'/odds')
                        try:
                            util = True     
                            oddc = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]').text
                            oddc = float(oddc)
                            oddf = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[3]').text
                            oddf = float(oddf)
                            odds = [oddc-oddf,oddf-oddc] # handcap inicial
                        except Exception as e:
                            print("odd error",e)
                            util = False
                        if util == True:
                            driver.get(links[x])
                            try:
                                try:
                                    element = driver.find_element_by_xpath('//*[@id="app"]/div[6]/div/div[2]/i')
                                    element.click()
                                except:
                                    pass
                                element = driver.find_element_by_xpath('//*[@id="Live"]/div[1]/div[1]/div[1]')
                                element.click()
                            except Exception as e:
                                print(e)
                            #driver.execute_script("window.scrollTo(0, 900 )")
                            try:
                                iframe = driver.find_element_by_xpath('//*[@id="Live"]/div[1]/div[2]/iframe').get_attribute('src')
                            except:
                                iframe = driver.find_element_by_xpath('//*[@id="Live"]/div[1]/div[3]/iframe').get_attribute('src')
                            try:  
                                tempo = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[2]/div[2]/div[2]/div[2]/div/span/span[1]').text
                                tempo = tempo.replace('+','')
                                tempo = int(tempo)
                                oddlc = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[1]/div[1]/div[2]/div[1]/span').text
                                oddlc = round(float(oddlc),2)
                                oddlf = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[1]/div[1]/div[2]/div[3]/span').text
                                oddlf = round(float(oddlf),2)
                                golc = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[2]/div[2]/div[2]/div[1]').text
                                golc = int(golc)
                                golf = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[2]/div[2]/div[2]/div[3]').text
                                golf = int(golf)
                                possec = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[3]/div[2]/div[1]/div[3]/div[1]/div[1]/span[1]').text
                                possec = int(possec)
                                possef = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[3]/div[2]/div[1]/div[3]/div[1]/div[1]/span[3]').text
                                possef = int(possef)
                                cc = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[3]/div[2]/div[1]/div[3]/div[2]/div[1]/span[1]').text
                                cc = int(cc)
                                cf = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[3]/div[2]/div[1]/div[3]/div[2]/div[1]/span[3]').text
                                cf = int(cf)
                                cgc = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[3]/div[2]/div[1]/div[3]/div[3]/div[1]/span[1]').text
                                cgc = int(cgc)
                                cgf = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[3]/div[2]/div[1]/div[3]/div[3]/div[1]/span[3]').text
                                cgf = int(cgf)
                                atqc = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[3]/div[2]/div[1]/div[3]/div[4]/div[1]/span[1]').text
                                atqc = int(atqc)
                                atqf = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[3]/div[2]/div[1]/div[3]/div[4]/div[1]/span[3]').text
                                atqf = int(atqf)
                                atqpc = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[3]/div[2]/div[1]/div[3]/div[5]/div[1]/span[1]').text
                                atqpc = int(atqpc)
                                atqpf = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[3]/div[2]/div[1]/div[3]/div[5]/div[1]/span[3]').text
                                atqpf = int(atqpf)
                                faltasc = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[3]/div[2]/div[1]/div[3]/div[6]/div[1]/span[1]').text
                                faltasc = int(faltasc)
                                faltasf = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[3]/div[2]/div[1]/div[3]/div[6]/div[1]/span[3]').text
                                faltasf = int(faltasf)
                                ctc = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[3]/div[2]/div[1]/div[3]/div[7]/div[1]/span[1]').text
                                ctc = int(ctc)
                                ctf = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[3]/div[2]/div[1]/div[3]/div[7]/div[1]/span[3]').text
                                ctf = int(ctf)
                                cac = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[3]/div[2]/div[1]/div[3]/div[8]/div[1]/span[1]').text
                                cac = int(cac)
                                caf = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[3]/div[2]/div[1]/div[3]/div[8]/div[1]/span[3]').text
                                caf = int(caf)
                                cvc = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[3]/div[2]/div[1]/div[3]/div[9]/div[1]/span[1]').text
                                cvc = int(cvc)
                                cvf = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[3]/div[2]/div[1]/div[3]/div[9]/div[1]/span[3]').text
                                cvf = int(cvf)
                            #no iframe da partida pega: tempo do ultimo gol, tempo do ultimo escanteio, numero de escanteios depois do gol
                                driver.get(iframe)
                                codigo = driver.find_element_by_xpath('/html/body/div/div/div[2]/div[3]/div[2]').get_attribute('outerHTML')
                                soup = BeautifulSoup(codigo, 'html.parser')
                                errorlencont = 0
                                lenerror = False
                                while(len(soup.find_all("svg"))<3):
                                    sleep(0.5)
                                    codigo = driver.find_element_by_xpath('/html/body/div/div/div[2]/div[3]/div[2]').get_attribute('outerHTML')
                                    soup = BeautifulSoup(codigo, 'html.parser')
                                    print('#')
                                    errorlencont += 1
                                    if errorlencont > 10:
                                        lenerror = True
                                        break
                                if lenerror == False:
                                    soup = BeautifulSoup(codigo, 'html.parser')
                                    soup.find_all("use")
                                    gol = '#icon-jinqiu1'
                                    canto = '#icon-jiaoqiu1'
                                    tempo_ultimo_gol = 0
                                    cantos_apos_ultimogol = 0

                                    for element in soup.find_all("svg", attrs={"class": "icon home"}):
                                        if element.use['xlink:href'] == gol:
                                            if tempo_ultimo_gol > int(element['data-val']):
                                                pass
                                            else:
                                                tempo_ultimo_gol = int(element['data-val'])
                                                
                                    for element in soup.find_all("svg", attrs={"class": "icon away"}):
                                        if element.use['xlink:href'] == gol:
                                            if tempo_ultimo_gol > int(element['data-val']):
                                                pass
                                            else:
                                                tempo_ultimo_gol = int(element['data-val'])
                                                
                                    atual_style = ''
                                    for element in soup.find_all("svg", attrs={"class": "icon home"}):
                                        if element.use['xlink:href'] == canto:
                                            if tempo_ultimo_gol <= int(element['data-val']):
                                                if atual_style != element['style']:
                                                    cantos_apos_ultimogol += 1
                                                    atual_style = element['style']
                                    atual_style = ''
                                    for element in soup.find_all("svg", attrs={"class": "icon away"}):
                                        if element.use['xlink:href'] == canto:
                                            if tempo_ultimo_gol <= int(element['data-val']):
                                                if atual_style != element['style']:
                                                    cantos_apos_ultimogol += 1
                                                    atual_style = element['style']
                                    
                                    new_row = {'link':links[x], 'tempo':tempo, 'odd pre casa':oddc, 'odd pre fora':oddf, 'odd live casa':oddlc, 'odd live fora':oddlf,
                            'gols casa':golc, 'gols fora':golf, 'posse casa':possec, 'posse fora':possef, 'chutes casa':cc, 'chutes fora':cf,
                            'chutes no gol casa':cgc, 'chutes no gol fora':cgf, 'ataques casa':atqc, 'ataques fora':atqf,
                            'ataques perigosos casa':atqpc, 'ataques perigosos fora':atqpf, 'faltas casa':faltasc, 'faltas fora':faltasf,
                            'cantos casa':ctc, 'cantos fora':ctf, 'cartao amarelo casa':cac, 'cartao amarelo fora':caf,
                            'cartao vermelho casa':cvc, 'cartao vermelho fora':cvf, 'tempo ultimo gol':tempo_ultimo_gol, 'cantos pos ultimo gol':cantos_apos_ultimogol}

                                    data = data.append(new_row, ignore_index=True)
                                    data.to_excel('dados.xlsx', index=False)
                                    print('salvo\n')
                                else: 
                                    print("lenerror")
                            except Exception as e:
                                print(e)
                                print('nao salvo\n')
                                pass
                    except Exception as e:
                        print("ERRO NA ANÁLISE",e)
                x+=1
    except Exception as e:
        print(e)
        pass 