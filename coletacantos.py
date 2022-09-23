import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

data = pd.read_excel('dados.xlsx', index_col=[0])

options = Options()
options.headless = True
options.add_argument("--mute-audio")
driver = webdriver.Chrome(executable_path="chromedriver.exe",options=options)
driver.maximize_window()

#data = data.drop('Unnamed: 0',1)
#data = data.drop('Unnamed: 0.1',1)
#data = data.drop('Unnamed: 0.2',1)

#data.to_excel('dadosht.xlsx')

df = data.loc[data['target 1 canto'] != 1]
df = df.loc[df['target 1 canto'] != 0]

try:
    x = 0
    for i in df['link']:
        driver.get(i)
        ctc = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[3]/div[2]/div[1]/div[3]/div[7]/div[1]/span[1]').text
        ctc = int(ctc)
        ctf = driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[4]/span/div/div[3]/div[2]/div[1]/div[3]/div[7]/div[1]/span[3]').text
        ctf = int(ctf)
        total_cantos = ctc + ctf
        #data.loc[(data['tempo ultimo gol'] < 1) & ((data['gols casa'] > 0) | data['gols fora'] > 0)]
        df = data.loc[data['link'] == i]
        sum = df['cantos casa'].iloc[0] + df['cantos fora'].iloc[0]
        if total_cantos > sum:
            data.loc[data['link'] == i, ['target 1 canto']] = 1
        else:
            data.loc[data['link'] == i, ['target 1 canto']] = 0
        if total_cantos > sum+1:
            data.loc[data['link'] == i, ['target 2 cantos']] = 1
        else:
            data.loc[data['link'] == i, ['target 2 cantos']] = 0 
        x += 1
        print(x)
        

    data.to_excel('dados.xlsx')
    driver.quit()

    #print(sum)
    #data = data.loc[data['cantos casa'] > 10]
    #for i in data['link']:
    #    print(i)
    print(data[['target 1 canto']])

except Exception as e:
    data.to_excel('dados.xlsx')
    driver.quit()
    print(e)
    
