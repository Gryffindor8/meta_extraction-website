from collections import OrderedDict

import pandas as pd
import requests
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def title_descript(urls):
    r = requests.get(urls)
    soup = BeautifulSoup(r.content, features="html.parser")
    title = soup.title.string
    count = len(title.split())
    return count, title


def link_extract(domain):
    parser = 'html.parser'
    resp = urllib.request.urlopen(domain)
    domain = urlparse(domain).netloc
    domain = "https://" + domain
    soup = BeautifulSoup(resp, parser)
    links = []
    for link in soup.find_all('a', href=True):
        if (str(link['href'])[0]) == "/" and len(str(link["href"])) > 2:
            links.append(domain + link["href"])
    for link in soup.find_all('a', href=True):
        if domain in (str(link["href"])):
            links.append(domain + link["href"])
    links = list(OrderedDict.fromkeys(links))
    return links


def description(url):
    missing = False
    description_selectors = [
        {"name": "description"},
        {"name": "og:description"},
        {"property": "description"}
    ]
    parser = 'html.parser'
    resp = urllib.request.urlopen(url)
    soup = BeautifulSoup(resp, parser)
    for selector in description_selectors:
        description_tag = soup.find(attrs=selector)
        if description_tag and description_tag.get('content'):
            desciption = description_tag['content']
            break
    else:
        desciption = 'None'
        missing = True
    return missing, desciption


def strt(dom):
    if "https://" not in dom:
        dom = "https://" + dom
    if ".com" not in dom:
        dom = dom + ".com"
    lk = link_extract(dom)
    lk2 = []
    data = []
    all_links = []
    missing_descrip = []
    descrip = []
    missing_url = []
    url = []
    gpt_titles = []
    non_gpt_titles = []
    gpt_counts = []
    non_counts = []
    for k in lk:
        try:
            t = link_extract(k)
            for j in t:
                lk2.append(j)
        except:
            pass
    mergedlist = (lk + lk2)
    mergedlist = list(OrderedDict.fromkeys(mergedlist))
    mergedlist.append(dom)
    print("Link\t\t", "Title\t\t", "Description\t\t", "words")
    for i in mergedlist:
        try:
            des, text = description(i)
            c, t = title_descript(i)
            all_links.append(i)
            all_links.append(t)
            if des:
                gpt_counts.append(c)
                gpt_titles.append(t)
                missing_descrip.append("None")
                all_links.append("None")
                missing_url.append(i)
            if not des:
                non_counts.append(c)
                non_gpt_titles.append(t)
                descrip.append(text)
                all_links.append(text)
                url.append(i)
            print("link:", i.replace("\n", ""), "\nTitle:", t.replace("\n", ""), "\nDescription:",
                  text.replace("\n", ""),
                  "\nword Count:", c, "\n")
            print("---------------------------------------------------")
            all_links.append(c)
        except:
            pass

    # ==>Missing                                                                           ==>Non-Misssing
    # data = [word_cout_missing,title_of _missing_descrip,url_missing,description_missing || count_non_missing,title,
    # url,description]
    data.append(gpt_counts)
    data.append(gpt_titles)
    data.append(missing_url)
    data.append(missing_descrip)
    data.append(non_counts)
    data.append(non_gpt_titles)
    data.append(url)
    data.append(descrip)

    data2 = [missing_url, gpt_titles, missing_descrip, gpt_counts]

    if len(missing_url) > 0:
        print("\n Missing descriptions")
        print("url:", missing_url, "\tTitle:", gpt_titles, "\tDescription:", "None", "\t", "words:", gpt_counts)
        print("-----------------------------------------------------------------------------")
    else:
        print("no missing Description Found")
        print("---------------------------")
    try:
        df = pd.DataFrame(all_links, index=["Url", "Title", "Description", "words"])
        df = df.T
        df.to_csv("All_url.csv", encoding="utf-8", index=True, header=True)
        df2 = pd.DataFrame(data2, index=["Url", "Title", "Description", "words"])
        df2 = df2.T
        df2.to_csv("Missing_description.csv", encoding="utf-8", index=True, header=True)
    except:
        pass


while True:
    try:
        site = str(input("please input the domain name:"))
        strt(site)
    except:
        pass
