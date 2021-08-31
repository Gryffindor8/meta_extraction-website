from tkinter import *
from tkinter.ttk import Treeview,Style
import urllib.request
import urllib.request
from collections import OrderedDict
from urllib.parse import urlparse
import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import threading
from tkinter import messagebox


def title_descript(urls):
    r = requests.get(urls)
    soup = BeautifulSoup(r.content, features="html.parser")
    title = soup.title.string
    title=title.strip()
    count = len(title.split())
    return count, title


def link_extract(domain):

    parser = 'html.parser'
    resp = urllib.request.urlopen(domain)
    domain = urlparse(domain).netloc
    print("doma",domain)
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
    print("linkss",links)
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


def strt():
    x = scrapeListBox.get_children()
    # print('get_children values: ', x, '\n')
    # if x != '()':  # checks if there is something in the first row
    for child in x:
        scrapeListBox.delete(child)
    dom=url_entry_box.get()
    if "https://" not in dom:
        dom = "https://" + dom
    if ".com" not in dom:
        dom = dom + ".com"
    lk = link_extract(dom)
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

            all_links.append(c)
        except:
            pass

    data.append(gpt_counts)
    data.append(gpt_titles)
    data.append(missing_url)
    data.append(missing_descrip)
    data.append(non_counts)
    data.append(non_gpt_titles)
    data.append(url)
    data.append(descrip)
    print("zzzzzzzzz",missing_url)


    data2 = [missing_url, gpt_counts, gpt_titles, missing_descrip]
    # df = pd.DataFrame(all_links, index=["Url", "Title", "Description", "words"])
    # df = df.T
    # df.to_csv("All_url.csv", encoding="utf-8", index=True, header=True)
    df2 = pd.DataFrame(data2, index=["Url", "Words","Title", "Description"])
    df2 = df2.T
    df2.to_csv("Missing_description.csv", encoding="utf-8", index=True, header=True)



    return missing_url, gpt_titles, missing_descrip, gpt_counts
  # return url, descrip, gpt_titles, gpt_counts

def scrapeShow():

    summ=strt()
    a=summ[0]#url
    b=summ[1]#descrip
    c=summ[2]#gpt_titles
    d=summ[3]

    mm =[list(t) for t in zip(a, d,b,c)]
    if len(mm)==0:
        messagebox.showinfo("Alert","Already Have Meta Description")

    tempList = mm
    for i, (link, status,title, medescription) in enumerate(tempList, start=1):
        scrapeListBox.insert("", "end", values=( link, status,title, medescription))


            #yaha py to generate kiya ho ga wo
    # e=summ[4]
    # f=summ[5]
    # g=summ[6]
    # h=summ[7]
    # mm = [list(t) for t in zip(e, f, g, h)]
    # tempList = mm
    # for i, (link, status, title, medescription) in enumerate(tempList, start=1):
    #     autoListBox.insert("", "end", values=(link, status, title, medescription))


# def autoDoubleClick( event):
#     try:
#         cur_item = autoListBox.item(autoListBox.focus(item=None))
#         col = autoListBox.identify_column(event.x)
#
#         if col == '#1':
#             root.clipboard_clear()
#             root.clipboard_append(cur_item['values'][0])
#         if col == '#2':
#             root.clipboard_clear()
#             root.clipboard_append(cur_item['values'][1])
#         if col == '#3':
#             root.clipboard_clear()
#             root.clipboard_append(cur_item['values'][2])
#         if col == '#4':
#             root.clipboard_clear()
#             root.clipboard_append(cur_item['values'][3])
#     except IndexError:
#         pass

def scrapeDoubleClick( event):
    try:
        cur_item = scrapeListBox.item(scrapeListBox.focus(item=None))
        col = scrapeListBox.identify_column(event.x)

        if col == '#1':
            root.clipboard_clear()
            root.clipboard_append(cur_item['values'][0])
        if col == '#2':
            root.clipboard_clear()
            root.clipboard_append(cur_item['values'][1])
        if col == '#3':
            root.clipboard_clear()
            root.clipboard_append(cur_item['values'][2])
        if col == '#4':
            root.clipboard_clear()
            root.clipboard_append(cur_item['values'][3])
    except IndexError:
        pass

if __name__ == "__main__":
    root = Tk()
    root.title('MetaMaster')
    root.geometry('1135x680')
    root.resizable(False, False)


    frame1 = Frame(root, bg="grey", padx=187, pady=5)
    frame1.grid(row=0, column=0)

    name = Label(frame1,text='MetaMaster',fg="white",bg="grey",font=("Helvetica",14)).pack(padx=5, pady=5,side="left")
    url = StringVar()
    url_entry_box = Entry(frame1,  textvariable=url,width=40, highlightthickness=2,font=("Helvetica", 16))
    url_entry_box.pack(padx=5, pady=5,side="left")
    url_startbutton=Button(frame1,width=5,fg="grey",text="Start",font=("Helvetica",14)
                           ,command=scrapeShow).pack(padx=5, pady=5,side="left")
    # url_stopbutton = Button(frame1, width=5,fg="grey", text="Stop", font=("Helvetica", 14),command=threading.Thread(target=stops).start()).pack(padx=5, pady=5,side="left")

    frame2 = Frame(root, padx=0)
    frame2.grid(row=1, column=0)
    sname = Label(frame2,text='Scrape',fg="grey",font=("Helvetica bold",10)).pack(padx=5, pady=5)

    verscrlbar = Scrollbar(frame2, orient="vertical")
    verscrlbar.pack(side='right', fill="y")

    horscrlbar = Scrollbar(frame2, orient="horizontal")
    horscrlbar.pack(side='bottom', fill="x")

    cols = ('Link', 'Word Count', 'Title', 'Meta Description')
    scrapeListBox = Treeview(frame2, columns=cols, show='headings', height="20", style="mystyle.Treeview",
                             selectmode='browse', yscrollcommand=verscrlbar.set, xscrollcommand=horscrlbar.set)

    for col in cols:
        scrapeListBox.heading(col, text=col)

    style = Style()
    style.configure("mystyle.Treeview.Heading", font=('Helvetica', 10, 'bold'))
    scrapeListBox.pack(padx=5, pady=5, side="left")

    scrapeListBox.column("#1", minwidth=10, width=350, stretch=NO)
    scrapeListBox.column("#2", minwidth=10, width=90, stretch=NO)
    scrapeListBox.column("#3", minwidth=10, width=250, stretch=NO)
    scrapeListBox.column("#4", minwidth=10, width=410, stretch=NO)
    scrapeListBox.bind("<Double-1>", scrapeDoubleClick)

    verscrlbar.configure(command=scrapeListBox.yview)
    horscrlbar.configure(command=scrapeListBox.xview)

    # frame3 = Frame(root, padx=0)
    # frame3.grid(row=2, column=0)
    # aname = Label(frame3,text='Autofill',fg="grey",font=("Helvetica bold",10)).pack(padx=5, pady=5)
    #
    # verscrlbar = Scrollbar(frame3, orient="vertical")
    # verscrlbar.pack(side='right', fill="y")
    #
    # horscrlbar = Scrollbar(frame3, orient="horizontal")
    # horscrlbar.pack(side='bottom', fill="x")
    #
    # cols = ('Link', 'Word Count', 'Title', 'Meta Description')
    # autoListBox = Treeview(frame3, columns=cols, show='headings', height="10", style="mystyle.Treeview",
    #                    selectmode='browse', yscrollcommand=verscrlbar.set, xscrollcommand=horscrlbar.set)
    #
    # for col in cols:
    #     autoListBox.heading(col, text=col)
    #
    # style = Style()
    # style.configure("mystyle.Treeview.Heading", font=('Helvetica', 10, 'bold'))
    # autoListBox.pack(padx=5, pady=5, side="left")
    #
    # autoListBox.column("#1", minwidth=10, width=350, stretch=NO)
    # autoListBox.column("#2", minwidth=10, width=50, stretch=NO)
    # autoListBox.column("#3", minwidth=10, width=250, stretch=NO)
    # autoListBox.column("#4", minwidth=10, width=450, stretch=NO)
    # autoListBox.bind("<Double-1>", autoDoubleClick)
    #
    # verscrlbar.configure(command=autoListBox.yview)
    # horscrlbar.configure(command=autoListBox.xview)


    # scrapeShow()
    # autoShow()

    root.mainloop()

# import requests
# from bs4 import BeautifulSoup
# from transformers import pipeline
# url="https://www.parsehub.com/"
# page = requests.get(url).text
# soup = BeautifulSoup(page, "html.parser")
# ss=[]
# for i in soup.stripped_strings:
#     ss.append(i)
# ss = ''.join(map(str, ss))
# ss=" ".join(ss.split())
# bart_summarizer = pipeline("summarization")
# TEXT_TO_SUMMARIZE=ss
# summary = bart_summarizer(TEXT_TO_SUMMARIZE, min_length=50, max_length=100)

# print(len(summary[0]["summary_text"]))
# print(summary)
