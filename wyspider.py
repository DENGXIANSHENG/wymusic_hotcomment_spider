
# coding:utf-8
import requests,re,time,random,bs4
import lxml,html
from bs4 import BeautifulSoup

weburl='http://music.163.com'
url='http://music.163.com/discover/playlist/?order=hot&cat=%E5%8D%8E%E8%AF%AD&limit=35&offset=0'
proxyurl = 'http://www.xicidaili.com/nn/'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        'Connection':'keep-alive'
    }

res=requests.get(url)
# print res.raise_for_status()
def loopGetPlayList(t):
    hl=BeautifulSoup(t,'lxml')
    #lists=re.search('playlist\?id=\d+',res.text)
    lists=hl.select('.msk')
    for v in range(len(lists)):
        try:
            loopGetSongHotComment(lists[v].attrs)
               
        except BaseException,e:
            #session.rollback()
            print e


    nextpage=hl.select('.znxt')[0].attrs['href']
    #print weburl+nextpage
    if(nextpage=='javascript:void(0)'):
        return;
    loopGetPlayList(requests.get(weburl+nextpage).text)

def loopGetSongHotComment(play):
   
    playlistv=play
    r=requests.get(weburl+play['href'],headers=headers)
    songhl=BeautifulSoup(r.text,'lxml')
    songlist=songhl.select('.f-hide a')
    print '得到'+str(len(songlist))
    for v in range(len(songlist)):
        songNum=re.search('\d+',songlist[v]['href'])
        print '1'
        purl = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(songNum.group(0)) + '?csrf_token='
        pdata = {
            'params': 'vSRanZoxZIVtHtu60/7fpGPEe5BhGoJw/22jrbpTtrIHPRWjkbGBDVh8ac+HP++Ftj7DvXk1Dv7XUiUgfcaKlzOA5m0qqtb9TOsqDR0qSPMA50w+N63Yj0VSHNGftdL9wTRNfB0paugtIdwQ21PHNzdm2ZIZ3mcxxKpuAo1J0RBqkHgR8Ha4KhBAU0BujnNy',                'encSecKey': '1a3b612a65a75e44fe78b9424d8c24eba2cbe2c2799aa5f48fc6f32e9b071e30849d51fcafd6812dd7f62eb4879f2c5c596761f61a699c048bf7f3dbf9b84f8ff3df8c7efc27905a9f42df374b82d5b3e25825e82c536c8ed36356c0b0989e0bcec18c3034594cbd7e498e912525525ff00557da903b7a41e32aa0214499c02e'
        }
        
        ip_list = get_ip_list(proxyurl, headers
                              =headers)
        proxies = get_random_ip(ip_list)
        hotRes = requests.post(purl, data=pdata,headers=headers,proxies=proxies)
        comment = hotRes.json()['hotComments']
        print comment+'nn'
        for cv in range(len(comment)):
            try:

                csongname = songlist[v].getText()
                print csongname
                    
                
            except BaseException,e:
                print e
                    
                print 'hotCommentrollback'



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
    print proxy_ip
    return proxies

loopGetPlayList(res.text)


