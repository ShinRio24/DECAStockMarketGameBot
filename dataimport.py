from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from stat import S_IREAD
import datetime
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()

def rdailyimporter(nr):
    if type(nr) == int:
        tem = os.listdir("rdata/")
        nr = tem[nr - 1][:-4]

    with open('rdata/{}.xml'.format(nr), 'r') as f:
        data = f.read()


    bdata = BeautifulSoup(data, 'html.parser')

    teamname = bdata.find_all('teamname')
    for x in range(len(teamname)):
        teamname[x] = teamname[x].text.lower()

    totalequity = bdata.find_all('totalequity')
    for x in range(len(totalequity)):
        totalequity[x] = totalequity[x].text

    sp500growth = bdata.find_all('sp500growth')
    for x in range(len(sp500growth)):
        sp500growth[x] = sp500growth[x].text

    schoolname = bdata.find_all('schoolname')
    for x in range(len(schoolname)):
        schoolname[x] = schoolname[x].text.replace(" ","_").lower()

    lrank = bdata.find_all('rank')
    rank=[]
    for x in range(len(lrank)//2):
        rank.append(lrank[x*2].text)



    l = {}
    for i, x in enumerate(teamname):
        l[x] = {"totalequity": totalequity[i], "sp500growth": sp500growth[i], "schoolname": schoolname[i],
                "rank": rank[i]}
    return l



def ndailyimporter(nn):
    if type(nn)==int:
        tem=os.listdir("rdata/")
        nn=tem[nn-1][:-4]

    with open('ndata/{}.xml'.format(nn), 'r') as f:
        data = f.read()

    bdata = BeautifulSoup(data, 'html.parser')

    teamname = bdata.find_all('teamname')
    for x in range(len(teamname)):
        teamname[x] = teamname[x].text.lower()

    totalequity = bdata.find_all('totalequity')
    for x in range(len(totalequity)):
        totalequity[x] = totalequity[x].text

    sp500growth = bdata.find_all('sp500growth')
    for x in range(len(sp500growth)):
        sp500growth[x] = sp500growth[x].text

    schoolname = bdata.find_all('schoolname')
    for x in range(len(schoolname)):
        schoolname[x] = schoolname[x].text.replace(" ","_").lower()

    lrank = bdata.find_all('rank')
    rank=[]
    for x in range(len(lrank)//2):
        rank.append(lrank[x*2].text)
    l = {}
    for i, x in enumerate(teamname):
        l[x] = {"totalequity": totalequity[i], "sp500growth": sp500growth[i], "schoolname": schoolname[i],
                "rank": rank[i]}
    return l

def rlimporter():
    c = len(os.listdir('rdata/'))
    l={}
    for x in range(1,c+1):
        l[x]=rdailyimporter(x)
    return l

def nlimporter():
    c = len(os.listdir('rdata/'))
    l={}
    for x in range(1,c+1):
        l[x]=ndailyimporter(x)
    return l


def download(nr,nn):
    PATH = 'C:\Program Files (x86)\chromedriver5.exe'
    driver = webdriver.Chrome(PATH)
    driver.get('https://www.stockmarketgame.org/login.html')
    s = datetime.datetime.now()
    d = str(s.month) + "-" + str(s.day)
    time.sleep(5)

    credentials = driver.find_element(By.NAME, "ACCOUNTNO")
    credentials.send_keys(os.getenv("decaLogin"))
    time.sleep(1)
    credentials = driver.find_element(By.NAME, "USER_PIN")
    credentials.send_keys("decaPass")
    time.sleep(2)

    driver.find_element(By.XPATH,"/html/body/div[1]/div/section/section/div/form/p[3]/input").click()
    time.sleep(3)

    #get the xml and save to nr and nn
    driver.get('https://www.stockmarketgame.org/cgi-bin/haipage/page.html?tpl=Administration/game/rank_dataxml&ranklevel=REGION')
    time.sleep(2)
    ts='r'
    c = driver.page_source
    text_file = open("{0}data/{1}.xml".format(ts, d), "w")
    n = text_file.write(c)
    text_file.close()

    os.chmod("{0}data/{1}.xml".format(ts, d), S_IREAD)
    time.sleep(3)


    driver.get('http://www.smgww.org/cgi-bin/haipage/page.html?tpl=Administration/game/rank_dataxml&ranklevel=COORD')
    time.sleep(2)
    ts = 'n'
    c = driver.page_source
    text_file = open("{0}data/{1}.xml".format(ts, d), "w")
    n = text_file.write(c)
    text_file.close()
    os.chmod("{0}data/{1}.xml".format(ts, d), S_IREAD)
    time.sleep(3)

    driver.close()


def fulldownload():
    configure()
    c = len(os.listdir('rdata/'))
    download(c + 1, c + 1)
    return 1

if __name__=="__main__":
    fulldownload()