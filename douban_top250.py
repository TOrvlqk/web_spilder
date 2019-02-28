import requests
from bs4 import BeautifulSoup


def open_url(url):
    #使用代理
    # proxies={'HTTP':'113.121.154.147:9999'}
    headers={'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.90 Safari/537.36 2345Explorer/9.6.0.18627'}
    # res=requests.get(url,headers=headers,proxies=proxies)
    res = requests.get(url, headers=headers)
    return res
def find_movies(res):
    soup=BeautifulSoup(res.text,'html.parser')
    #爬取电影名
    movies=[]
    targets=soup.find_all('div',class_='hd')
    for i in targets:
        movies.append(i.a.span.text)
    #爬取评分
    ranks=[]
    targets= soup.find_all('span',class_='rating_num')
    for each in targets:
        ranks.append('本片评分:%s'%each.text)
    #爬取基本资料
    message=[]
    targets= soup.find_all('div',class_='bd')
    for each in targets:
        try:
            message.append(each.p.text.split('\n')[1].strip()+each.p.text.split('\n')[2].strip())
        except:
            continue
    result=[]
    movie_length=len(movies)
    for i in range(movie_length):
        result.append(movies[i]+ranks[i]+message[i]+'\n')
    return  result




def find_depth(res):
    soup = BeautifulSoup(res.text,'html.parser')
    depth=soup.find('span',class_="next").previous_sibling.previous_sibling.text

    return int(depth)
def main():
    host='https://movie.douban.com/top250'
    res=open_url(host)
    depth = find_depth(res)
    result=[]
    for i in range(depth):
        url=host+'/?start='+str(25*i)
        res=open_url(url)
        result.extend(find_movies(res))
    with open('豆瓣电影top250.txt','w',encoding='utf-8') as f:
        for each in result:
            f.write(each)

if __name__ == '__main__':
    main()
