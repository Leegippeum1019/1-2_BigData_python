import os
import sys
import urllib.request
import datetime
import time
import json
import csv

client_id = '1IvRa9bU3kfc6Gjh5wqu'
client_secret = 'LVvHIE0pHl'

#[CODE1]
def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

#[CODE2]
def getNaverSearch(node, srcText, page_start, display):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % node
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(srcText), page_start, display)

    url = base + node + parameters
    responseDecode = getRequestUrl(url) #[CODE1]

    if responseDecode is None:
        return None
    else:
        return json.loads(responseDecode)

#[CODE3]
def getPostData(post, jsonResult, csvResult, cnt):
    title = post['title']
    description = post['description']
    org_link = post['originallink']
    link = post['link']

    pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')

    jsonResult.append({'cnt': cnt, 'title': title, 'description': description, 'org_link': org_link, 'link': link, 'pDate': pDate})
    csvResult.append([cnt, title, description, org_link, link, pDate])
    return

#[CODE0]
def main():
    node = 'news'  # 크롤링할 대상
    srcText = input("검색어를 입력하세요: ")
    cnt = 0
    jsonResult = []
    csvResult = []

    jsonResponse = getNaverSearch(node, srcText, 1, 100) #[CODE2]
    total = jsonResponse['total']

    while ((jsonResponse is not None) and (jsonResponse['display'] != 0)):
        for post in jsonResponse['items']:
            cnt += 1
            getPostData(post, jsonResult, csvResult, cnt) #[CODE3]

        start = jsonResponse['start'] + jsonResponse['display']
        jsonResponse = getNaverSearch(node, srcText, start, 100) #[CODE2]

    print('전체 검색: %d 건' % total)

    # JSON 파일 저장
    with open("%s_naver_%s.json" % (srcText, node), 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(jsonFile)

    # CSV 파일 저장
    with open("%s_naver_%s.csv" % (srcText, node), 'w', newline='', encoding='utf-8-sig') as csvfile:
        csvWriter = csv.writer(csvfile)
        # CSV 파일에 헤더 추가
        csvWriter.writerow(['cnt', 'title', 'description', 'org_link', 'link', 'pDate'])
        # 데이터 추가
        csvWriter.writerows(csvResult)

    print("가져온 데이터: %d 건" % (cnt))
    print("%s_naver_%s.json 및 %s_naver_%s.csv SAVED" % (srcText, node, srcText, node))

if __name__ == '__main__':
    main()