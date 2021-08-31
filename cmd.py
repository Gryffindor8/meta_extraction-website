import threading
import time
import urllib.request
from collections import OrderedDict
from urllib.parse import urlparse

import pandas as pd
from bs4 import BeautifulSoup


def link_extract(domain):
    parser = 'html.parser'
    resp = urllib.request.urlopen(domain)
    domain = urlparse(domain).netloc
    domain = "https://" + domain
    soup = BeautifulSoup(resp, parser)
    links2 = []
    links3 = []
    for link in soup.find_all('a', href=True):
        if (str(link['href'])[0]) == "/" and len(str(link["href"])) > 2:
            links2.append(domain + link["href"])
    for link in soup.find_all('a', href=True):
        if domain in (str(link["href"])):
            links2.append(domain + link["href"])
        else:
            links3.append(link["href"])
    links2 = list(OrderedDict.fromkeys(links2))
    return links2, links3


def description(lnks, external):
    for url in lnks:
        try:
            desciption = ' '
            description_selectors = [
                {"name": "description"},
                {"name": "og:description"},
                {"property": "description"}
            ]
            parser = 'html.parser'
            t11 = time.time()
            resp = urllib.request.urlopen(url)
            t2 = time.time()
            response = t2 - t11
            status_code = resp.getcode()
            print(status_code)
            if status_code == 200:
                status = "OK"
            else:
                status = "Error"

            soup = BeautifulSoup(resp, parser)
            title = soup.title.string
            text = (soup.get_text())
            count = len(text.split())
            # print(count)
            for selector in description_selectors:
                description_tag = soup.find(attrs=selector)
                if description_tag and description_tag.get('content'):
                    desciption = description_tag['content']
                    break
                else:
                    desciption = "None"
            print("link:", url.replace("\n", ""), "\nTitle:", title.replace("\n", ""), "\nDescription:",
                  desciption.replace("\n", ""),
                  "\nWord Count:", count, "\n", " Response_time", t2 - t11)
            print("---------------------------------------------------")
            if count < 150:
                short = True
            else:
                short = False
            data1 = [url, count, title, desciption, status_code, status, response, short]
            df = pd.DataFrame(data1,
                              index=["Url", "Words", "Title", "Description", "Response", "staus_code",
                                     "Load_time", "Short_content"])
            df = df.T
            df.to_csv("All_links.csv", encoding="utf-8", mode='a', index=False, header=False)
            if desciption == "None" or short:
                data2 = [url, count, title, "None", status, status_code, response, short]
                df2 = pd.DataFrame(data2, index=["Url", "Words", "Title", "Description", "Response", "staus_code",
                                                 "Load_time", "Short_content"])
                df2 = df2.T
                df2.to_csv("Missing_description.csv", encoding="utf-8", mode='a', index=False, header=False)
        except:
            pass
    data3 = [external]
    df = pd.DataFrame(data3, index=["External_links"])
    df = df.T
    df.to_csv("External_links.csv", encoding="utf-8", index=False, header=True)


def strt(dom):
    print("Started......")
    print("Wait! Link Scraping.....")
    external2 = []
    external3 = []

    if "https://" not in dom:
        dom = "https://" + dom
    lk, external = link_extract(dom)
    lk2 = []
    lk3 = []
    print("Depth1 links")
    lk = list(OrderedDict.fromkeys(lk))
    for k in lk:
        print(k)
        try:
            t, external2 = link_extract(k)
            for j in t:
                print(j)
                lk2.append(j)
        except:
            pass
    print("Depth2 Link")
    lk2 = list(OrderedDict.fromkeys(lk2))
    for k in lk2:
        try:
            t, external3 = link_extract(k)
            for j in t:
                print(j)
                lk3.append(j)
        except:
            pass
    mergedlist = (lk + lk2 + lk3)
    extrnl = (external2 + external3 + external)
    mergedlist = list(OrderedDict.fromkeys(mergedlist))
    extrnl = list(OrderedDict.fromkeys(extrnl))
    mergedlist.append(dom)
    # print(mergedlist)
    data2 = [" ", " ", " ", " ", " ", "", " ", ""]
    df2 = pd.DataFrame(data2,
                       index=["Url", "Words", "Title", "Description", "Response", "staus_code",
                              "Load_time", "Short_content"])
    df2 = df2.T
    df2.to_csv("Missing_description.csv", encoding="utf-8", index=False)
    df2.to_csv("All_links.csv", encoding="utf-8", index=False)

    if len(mergedlist) > 10:
        l1 = int(len(mergedlist) / 2)
        lst1 = mergedlist[0:l1]
        lst2 = mergedlist[l1:]
        t3 = threading.Thread(target=description, args=(lst1, extrnl,))
        t2 = threading.Thread(target=description, args=(lst2, extrnl,))
        t3.start()
        t2.start()
        t3.join()
        t2.join()
    else:
        description(mergedlist, extrnl)


if __name__ == '__main__':
    while True:
        try:
            t1 = time.time()
            site = str(input("please input the domain name:"))
            print("starting....")
            #site = "https://www.python.org/"
            # site = "https://chasereiner.com"
            strt(site)
            print("Stopped.....")
            print("Time Spent:", time.time() - t1)
        except:
            pass
