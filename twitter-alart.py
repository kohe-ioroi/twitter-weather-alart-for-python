import urllib.request,time,datetime,threading
import tweepy
from bs4 import BeautifulSoup

#別途BeautifulSoupとtweepyをインストールする必要があります。
consumer_key = "key"
consumer_secret = "secret"

_auther_ = "Kohe_Ioroi"
def weather():
    weather_finalupdate = ""
    while True:
        weather_html = urllib.request.urlopen('http://weather.livedoor.com/warn/28').read()
        weather_soup = BeautifulSoup(weather_html,"html.parser")
        weather_table = weather_soup.findAll('table')[0]
        weather_list1 = weather_table.find('tr')
        weather_list2 = weather_list1.findAll('td')[1]
        weather_keihou = []
        weather_chuuihou = []
        if weather_list2.findAll('span',class_="alarmred") == []:
            pass
        else:
            for weather_list3 in weather_list2.findAll('span',class_="alarmred"):
                weather_keihou.append(weather_list3.text)
        if weather_list2.findAll('span',class_="alarmyellow") == []:
            pass
        else:
            for weather_list3 in weather_list2.findAll('span',class_="alarmyellow"):
                weather_chuuihou.append(weather_list3.text)
        if weather_keihou == []:
            weather_keihoutext = "ありません。"
        else:
            weather_keihoutext = "、"+'・'.join(weather_keihou)+"です。"
        if weather_chuuihou == []:
            weather_chuuitext = "ありません。"
        else:
            weather_chuuitext = "、"+'・'.join(weather_chuuihou)+"です。"
        weather_chiikidata = "発表地域は"+(weather_list1.find('td').text)
        weather_keihoudata = "現在発表されている警報は"+weather_keihoutext
        weather_chuuihoudata = "現在発表されている注意報は"+weather_chuuitext
        weather_timedata = weather_list1.findAll('td',align="right")[0].text
        weather_text = weather_keihoudata+"\n"+weather_chuuihoudata+"\n\n"+"最新:"+weather_timedata+"\n\n\nシステム通信時刻:"+str(datetime.datetime.now())+"\n\n最新の情報はこちら→[http://weather.livedoor.com/warn/detail/28/2810000]"
        if weather_finalupdate == [weather_keihoudata,weather_chuuihoudata]:
            pass
        else:
            weather_auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            weather_auth.set_access_token("Hoge")
            weather_api = tweepy.API(weather_auth)
            weather_api.update_status(weather_text)
            weather_finalupdate = [weather_keihoudata,weather_chuuihoudata]
        time.sleep(10)
def typhoon():
    typhoon_finalupdate = ""
    while True:
        typhoon_html = urllib.request.urlopen('http://weather.livedoor.com/typhoon/').read()
        typhoon_soup = BeautifulSoup(typhoon_html,"html.parser")
        typhoon_data = []
        typhoon_table = typhoon_soup.findAll('table')[0]
        for typhoon_list1 in typhoon_table.findAll('tr'):
            typhoon_data.append(typhoon_list1.find('td').text)
        typhoon_name = typhoon_data[0]
        typhoon_map = typhoon_data[1]
        typhoon_hpa = typhoon_data[5]
        typhoon_spd = typhoon_data[6]
        typhoon_dir = typhoon_data[7]
        earthquake_send = "台風名:"+typhoon_name+"\n台風の位置:"+typhoon_map+"\n中心気圧:"+typhoon_hpa+"\n最大風速:"+typhoon_spd+"\n進行:"+typhoon_dir+"\n\n"+"\n\n\nシステム通信時刻:"+str(datetime.datetime.now())+"\n\n最新の情報はこちら→[http://weather.livedoor.com/typhoon/]"
        if typhoon_finalupdate == [typhoon_map,typhoon_hpa,typhoon_spd,typhoon_hpa]:
            pass
        else:
            typhoon_auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            typhoon_auth.set_access_token("Hoge", "Hoge")
            typhoon_api = tweepy.API(typhoon_auth)
            typhoon_api.update_status(earthquake_send)
            typhoon_finalupdate = [typhoon_map,typhoon_hpa,typhoon_spd,typhoon_hpa]
        time.sleep(3600)
def earthquake():
    earthquake_finalupdate = ""
    earthquake_flag = False
    while True:
        earthquake_html = urllib.request.urlopen('http://weather.livedoor.com/earthquake/').read()
        earthquake_soup = BeautifulSoup(earthquake_html,"html.parser")
        earthquake_data = []
        earthquake_table = earthquake_soup.findAll('table')[3]
        for earthquake_list1 in earthquake_table.findAll('tr'):
            for earthquake_list2 in earthquake_list1.findAll('td'):
                if "神戸" in earthquake_list2.text:
                    earthquake_flag = True
        if earthquake_flag == True:
            earthquake_table = earthquake_soup.findAll('table')[2]
            for earthquake_list1 in earthquake_table.findAll('tr'):
                for earthquake_list2 in earthquake_list1.findAll('td'):
                    if earthquake_list2.text != "":
                        earthquake_data.append(earthquake_list2.text.replace("\xa0","").replace("\n","").replace(" ",""))
            earthquake_time = earthquake_data[0]
            earthquake_place = earthquake_data[1]
            earthquake_point = earthquake_data[2]
            earthquake_mag = earthquake_data[3]
            earthquake_quake = earthquake_data[4]
            earthquake_send = "発生時刻:"+earthquake_time+"\n震源地:"+earthquake_place+"\n\nマグニチュード:"+earthquake_mag.replace("マグニチュード","")+"\n震度:"+earthquake_quake.replace("震度","")+"\n\n"+"\n\n\nシステム通信時刻:"+str(datetime.datetime.now())+"\n\n最新の情報はこちら→[http://weather.livedoor.com/earthquake/]"
            if earthquake_finalupdate == [earthquake_time,earthquake_point,earthquake_mag]:
                pass
            else:
                earthquake_auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                earthquake_auth.set_access_token("Hoge", "Hoge")
                earthquake_api = tweepy.API(earthquake_auth)
                earthquake_api.update_status(earthquake_send)
            earthquake_finalupdate = [earthquake_time,earthquake_point,earthquake_mag]
        else:
            pass
        time.sleep(10)
thread=threading.Thread(target=weather)
thread.setDaemon(True)
thread.start()
thread=threading.Thread(target=typhoon)
thread.setDaemon(True)
thread.start()
thread=threading.Thread(target=earthquake)
thread.setDaemon(True)
thread.start()
thread_list = threading.enumerate()
thread_list.remove(threading.main_thread())
for thread in thread_list:
    thread.join()
