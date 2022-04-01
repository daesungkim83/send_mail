from email.mime.text import MIMEText
import re
from pip import main
import requests
from bs4 import BeautifulSoup
import smtplib
from account import *
from email.message import EmailMessage
import time
import sys
from datetime import datetime

def create_soup(url):
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def print_news(index, title, link):
    print("{}. {}".format(index+1, title))
    print("  (링크 : {})".format(link))


def scrape_weather():
    print("[오늘의 날씨]")
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%98%A4%EB%8A%98%EC%9D%98%EB%82%A0%EC%94%A8"
    soup = create_soup(url)
    cast = soup.find("p", attrs={"class":"summary"}).get_text()
    curr_temp = soup.find("div", attrs={"class":"temperature_text"}).get_text().strip()
    min_temp = soup.find("span", attrs={"class":"lowest"}).get_text().strip()
    max_temp = soup.find("span", attrs={"class":"highest"}).get_text().strip()
    rain_rate = soup.find("div", attrs={"class":"cell_weather"})
    morning = rain_rate.find_all("span", attrs={"class":"rainfall"})[0].get_text().strip()
    afternoon = rain_rate.find_all("span", attrs={"class":"rainfall"})[1].get_text().strip()
    sunset = soup.find("li", attrs={"class":"item_today type_sun"}).get_text().strip()
    etc = soup.find("dl", attrs={"class":"summary_list"})
    humidity = etc.find_all("dd", attrs={"class":"desc"})[1].get_text().strip()
    wind1 = etc.find_all("dt", attrs={"class":"term"})[2].get_text().strip()
    wind2 = etc.find_all("dd", attrs={"class":"desc"})[2].get_text().strip()





    print("{} ({} / {})".format(curr_temp, min_temp, max_temp))
    print(cast)    
    print("오전 강수확률 {} / 오후 강수확률 {}".format(morning, afternoon))
    print("습도 {}  /  {} {}".format(humidity, wind1, wind2))
    print(sunset)
    print()
    

def scrape_headline():
    print("[헤드라인 뉴스]")
    url = "https://news.daum.net"
    soup = create_soup(url)
    news = soup.find("div", attrs={"class":"box_g box_news_issue"})
    heads = news.find_all("a", attrs={"class":"link_txt"}, limit=7)

    for index, head in enumerate(heads):
        title = (head.get_text().strip())
        link = (head["href"])
        print_news(index, title, link)
        print("-"*100) # 줄긋기
    print()
        

def scrape_itnews():
    print("[IT 뉴스]")
    url = "https://news.daum.net/digital#1"
    soup = create_soup(url)
    it = soup.find("ul", attrs={"class":"list_newsmajor"})
    it_heads = it.find_all("a", attrs={"class":"link_txt"}, limit=7)
 

    
    for index, it_head in enumerate(it_heads):
        title = (it_head.get_text().strip())
        link = (it_head["href"])
        print_news(index, title, link)
        print("-"*100) # 줄긋기
    print()
        

def scrape_english():
    print("[오늘의 영어회화]")
    url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_lnb_eng_I_others_english&logger_kw=haceng_submain_lnb_eng_I_others_english#;"
    soup = create_soup(url)
    sentences = soup.find_all("div", attrs={"id":re.compile("^conv_kor_t")})
    print("(영어지문)")
    for sentence in sentences[len(sentences)//2:]: #8문장이 있다고 가정할때, index 기준 4~7까지 잘라서 가져옴
        print(sentence.get_text().strip())
    
    print()
    print("(한글지문)")
    for sentence in sentences[:len(sentences)//2:]: #8문장이 있다고 가정할때, index 기준 0~3까지 잘라서 가져옴
        print(sentence.get_text().strip())
    print()
    
        

if __name__=="__main__":
    scrape_weather() # 오늘의 날씨 정보 가져오기
    scrape_headline()
    scrape_itnews()
    scrape_english()


# temp = sys.stdout

sys.stdout = open('info.txt','w',encoding="utf8")
scrape_weather() # 오늘의 날씨 정보 가져오기
scrape_headline()
scrape_itnews()
scrape_english()

sys.stdout.close()

# sys.stdout = temp    

time.sleep(5)


date = datetime.today().strftime("%Y-%m-%d-%H")



with open("info.txt", "r", encoding="utf8") as fp:
    # text/plain 메시지를 만듭니다
    msg = EmailMessage()
    msg["Subject"] = "오늘의 정보 - {}시".format(date) # 제목
    msg["From"] = "daesungkim83@gmail.com" # 보내는 사람
    msg["To"] = "daesungkim83@gmail.com" # 받는사람

    msg.set_content(fp.read()) # 본문
    

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

# print("메일 전송완료")
# print

#print