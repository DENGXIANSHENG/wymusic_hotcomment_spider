
# coding:utf-8
import requests,re,time,random
import lxml,html
from bs4 import BeautifulSoup
from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData,ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import mysql
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')  

Base = declarative_base()
weburl='http://music.163.com'
url='http://music.163.com/discover/playlist/?order=hot&cat=%E5%8D%8E%E8%AF%AD&limit=35&offset=0'
proxyurl = 'http://www.xicidaili.com/nn/'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
class playList(Base):
    # 表的名字:
    __tablename__ = 'playList'

    # 表的结构:
    songListId = Column(Integer, primary_key=True)
    listName = Column(String(255))
    listAddr = Column(String(255))
    spiderStatus = Column(Integer)

class hotComment(Base):
    __tablename__='hotComment'
    songName = Column(String(255))
    songId = Column(Integer)
    comment = Column(String(10240))
    likeCount = Column(Integer)
    userNikeName = Column(String(255))
    id = Column(Integer, primary_key=True)


engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/wyyyy?charset=utf8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)



s = requests.session()
s.keep_alive = False
res=requests.get(url)
# print res.raise_for_status()
def loopGetPlayList(t):
    hl=BeautifulSoup(t,'lxml')
    #lists=re.search('playlist\?id=\d+',res.text)
    lists=hl.select('.msk')
    for v in range(len(lists)):

        try:
            session = DBSession()
            if (session.query(playList).filter(playList.listAddr == lists[v].attrs['href'],
                                               playList.spiderStatus == 1).first() == None):
                print '正在获取"' + lists[v].attrs['title'] + '"歌单内歌曲热评'
                if (session.query(playList).filter(playList.listAddr == lists[v].attrs['href'],
                                                   playList.spiderStatus == 0).first() == None):
                    new_playlist = playList(listName=lists[v].attrs['title'], listAddr=lists[v].attrs['href'],
                                            spiderStatus=0)
                    session.add(new_playlist)
                    session.commit()
                    session.close()

                result=loopGetSongHotComment(lists[v].attrs)
                if(result==False):
                    loopGetSongHotComment(lists[v].attrs)
                session.query(playList).filter(playList.listAddr == lists[v].attrs['href']).update({'spiderStatus': 1})
                session.commit()
                session.close()
        except BaseException,e:
            #session.rollback()
            print e


    nextpage=hl.select('.znxt')[0].attrs['href']
    #print weburl+nextpage
    if(nextpage=='javascript:void(0)'):
        return;
    loopGetPlayList(requests.get(weburl+nextpage).text)

def loopGetSongHotComment(play):
    session = DBSession()
    playlistv=play
    r=requests.get(weburl+play['href'],headers=headers)
    songhl=BeautifulSoup(r.text,'lxml')
    songlist=songhl.select('.f-hide a')
    print len(songlist)
    if(len(songlist)==0):
        time.sleep(600)
        loopGetSongHotComment(playlistv)
    for v in range(len(songlist)):
        songNum=re.search('\d+',songlist[v]['href'])
        if (session.query(hotComment).filter(hotComment.songId==songNum.group(0)).first() == None):
            purl = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(songNum.group(0)) + '?csrf_token='
            pdata = {
                'params': '86izqm9pXMfwPlcexEU5A57j2c/9aShEiYA/nv6gKn1o5fz0Hxaw5sjHMNdDBdL+L63Jzs4r1Wee0ZA6QxHjrHdQijT8zudyZ4/oibEZYEjcY9r86kam+OS5hdqTzhso2CxjaqzXn4cm4a9q3LCM8QOf/8ytq65C+3NgvhEvYWTmVbSaENWteytzqgvu34/+',
                'encSecKey': '1718ddeb7329e40e5b16fc6cc951f8a16e42c1e7eb4fb27a01c3528e1689951780dc05aa422f2785e5a63ccf7d2708d3aa522901f39528d3feb01a873274bc0a1aab8292306dfb27596bde259afa8b2c70d3df582dc5eb881987ae9c0c6b2df77e701d4b7f51002f5f541bfa8f3286b95c51abe413a5ec9d44e942831a67a9bc'
            }
            time.sleep(2)
            hotRes = requests.post(purl, data=pdata,headers=headers)
            if(len(hotRes.text)==0):
                return False
            comment = hotRes.json()['hotComments']
            for cv in range(len(comment)):
                try:

                    csongname = songlist[v].getText()
                    print csongname
                    csongdd = songNum.group(0)
                    cconnent = comment[cv]['content']
                    clikecount = comment[cv]['likedCount']
                    cusernikename = comment[cv]['user']['nickname']
                    newComment = hotComment(songName=csongname, songId=csongdd, comment=cconnent, likeCount=clikecount,
                                            userNikeName=cusernikename)
                    session.add(newComment)
                    session.commit()
                    session.close()
                    time.sleep(0.1)
                except BaseException,e:
                    print e
                    session.rollback()
                    print 'hotCommentrollback'
        else:
            print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            continue


def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list

def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies




loopGetPlayList(res.text)

