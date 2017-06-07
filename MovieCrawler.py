# coding=utf-8
import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
amazonAPI = "https://www.amazon.com/dp/"
beforeFirstParenthesesPattern = re.compile("(.*?)\(")
beforeFirstBracketPattern = re.compile("(.*?)\[")

months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8,
          "September": 9, "October": 10, "November": 11, "December": 12}
removeUselessNumberOfURL = re.compile("(\d+-\d+-\d+)")
movieNum = 0
emptyObj = {"name": None, "imdbScore": None,
            "summary": None,
            "directors": None, "writers": None,
            "actors": None,
            "tags": None, "countries": None,
            "languages": None, "releaseTime": None, "duration": None,
            "posterURL": None}

# 爬Amazon
def crawl(id):
    global movieNum
    print("第", movieNum, "部电影: ", id, " 开始处理...")
    movieNum += 1
    url = amazonAPI + id
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    aTags = soup.select('div[class="content"] ul li a')
    for a in aTags:
        if "imdb" in a['href']:
            print("有IMDB链接")
            imdbURL = removeUselessNumberOfURL.sub(string=a['href'], repl="")
            print("IMDBURL:", imdbURL)
            return getMovieInfo(imdbURL)
    print("没有IMDB链接，结束")
    return emptyObj
# 
# def getIMDBSearchURL(name):
#     return "http://www.imdb.com/find?ref_=nv_sr_fn&q=" + "+".join(name.split()) + "&s=tt"
# 
# def getIMDBMovieURL(name):
#     baseURL = "http://www.imdb.com/"
#     response = session.get(getIMDBSearchURL(name), headers=headers)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     URI = soup.find_all('td', class_='result_text')
#     if len(URI) == 0:
#         return None
#     for content in URI[0].contents:
#         if "Video" in content or "TV" in content:
#             return None
#     return baseURL + URI[0].find_all('a')[0]['href']


def getMovieInfo(imdb):
    response = requests.get(imdb, headers=headers)
    return getMovieInfoByText(response.text)

def getMovieInfoByText(text):
    movie = {}
    soup = BeautifulSoup(text, 'html.parser')
    movie['name'] = soup.find_all('div', class_='title_wrapper')[0].find("h1").contents[0].strip()
    scores = soup.find_all('div', class_='ratingValue')
    if len(scores) == 0:
        print("失败，提前结束")
        return emptyObj
    else:
        movie['imdbScore'] = scores[0].find_all('strong')[0]['title'].split()[0]
    movie['summary'] = soup.find_all('div', class_='summary_text')[0].get_text().strip()
    index = 0
    for h4 in soup.find_all(name='h4', class_='inline'):
        if "Director" in h4.contents[0]:
            movie['directors'] = getStringList(soup, 0)
    if 'directors' not in movie:
        movie['directors'] = None
        index -= 1
    for h4 in soup.find_all(name='h4', class_='inline'):
        if "Writer" in h4.contents[0]:
            movie["writers"] = getStringList(soup, 1 + index)
    if 'writers' not in movie:
        movie['writers'] = None
        index -= 1
    for h4 in soup.find_all(name='h4', class_='inline'):
        if "Star" in h4.contents[0]:
            movie["actors"] = getStringList(soup, 2 + index)
    if 'actors' not in movie:
        movie['actors'] = None
    tags = []
    for a in soup.find_all('div', {'class': 'see-more inline canwrap', 'itemprop': 'genre'})[0].find_all('a'):
        tags.append(a.contents[0].strip().replace("-", "_"))
    movie['tags'] = tags
    hasDetails = -1
    # 如果没有Official Sites这个入口，那么所有索引都减1
    for h4 in soup.find_all(name='h4', class_='inline'):
        if "Official Sites" in h4.contents[0]:
            hasDetails = 0
            break
    movie['countries'] = getLanguageOrCountry(soup, 1 + hasDetails)
    movie['languages'] = getLanguageOrCountry(soup, 2 + hasDetails)
    try:
        timeStr = beforeFirstParenthesesPattern.findall(
            soup.find_all(id='titleDetails')[0].find_all('div', class_='txt-block')[3 + hasDetails].contents[
                2].strip())[0]
    except IndexError:
        print("失败，提前结束")
        return emptyObj
    strs = timeStr.split()
    movie['releaseTime'] = strs[2] + "-" + ("%02d" % int(months[strs[1]])) + "-" + ("%02d" % int(strs[0]))
    if len(soup.find_all('time')) != 0:
        times = soup.find_all('time')[0].contents[0].split()
        if len(times) == 1:
            min = int(times[0].replace('min', ''))
        else:
            hour, min = times[0], times[1]
            min = int(min.replace('min', '')) + int(hour.replace('h', '')) * 60
        movie['duration'] = min
    else:
        movie['duration'] = 0
    movie['posterUrl'] = soup.find_all('div', class_='poster')[0].find_all('img')[0]['src']
    movie['imdbReviewTime'] = soup.find_all('span',class_='small')[0].get_text().replace(',','').strip()
    return movie


def getStringList(soup, index):
    list = []
    for span in soup.find_all('div', class_='credit_summary_item')[index].find_all('span', class_='itemprop'):
        list.append(span.contents[0].strip())
    return list


def getLanguageOrCountry(soup, index):
    list = []
    for a in soup.find_all(id='titleDetails')[0].find_all('div', class_='txt-block')[index].find_all('a'):
        list.append(a.contents[0].strip())
    return list

def crawlForPredication(imdb):
    response = requests.get(imdb, headers=headers)
    result = dict()
    result['movie'] = getMovieInfoByText(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    spans = soup.find_all('span',class_='subText')
    target_span = None
    for span in spans:
        for a in span.find_all('a'):
            if 'user' in a.contents[0]:
                target_span = span
    a = target_span.find_all('a')
    result['num_user_for_reviews'] = a[0].get_text().strip().replace(' user','')
    result['num_critic_for_reviews'] = a[1].get_text().strip().replace(' critic','')
    for h4 in soup.find_all('h4',class_='inline'):
        if 'Budget' in h4.get_text().strip():
            result['budget'] = h4.next_sibling.replace('$','').replace(',','').strip()
    print(result)
    return result

if __name__ == "__main__":
    # print(crawl("B000Q7ZO8U"))
    crawlForPredication("http://www.imdb.com/title/tt5655222/?ref_=inth_ov_tt")
    # print(getMovieInfo("http://www.imdb.com//title/tt1667485/?ref_=fn_tt_tt_1"))
    # url = "http://www.imdb.com/title/tt0360486/?_encoding=UTF8&ref_=amzn_dp_dvd"
    # print(removeUselessNumberOfURL.sub(string=url, repl=""))
