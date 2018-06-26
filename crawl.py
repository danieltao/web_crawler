from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import os
import threading
import time
import logging

def getImage( url, folder):
    # check dir
    if not os.path.exists(folder):
        os.makedirs(folder)

    # cook soup
    soup = BeautifulSoup(urlopen(url), "html.parser")

    # look for image class and get src
    srcs = []
    img_class = soup.find("div", attrs={"class": "quote-content"})
    for img in img_class.find_all("img"):
        if "placeholder" not in img.get('src'):
            srcs.append(img.get("src").replace("?x-oss-process=image/resize,w_800/format,webp", ""))

    # download images
    for i in range(len(srcs)):
        urlretrieve(srcs[i], folder + str(i) + ".jpg")

def run(url, savepath, keywords):
    # load url
    page = urlopen(url)
    soup = BeautifulSoup(page, "html.parser")

    # find the desired div
    bbs = soup.find("ul", attrs={"class": "for-list"})

    # get links
    links = []
    for link in bbs.find_all('a', attrs={"class": "truetit"}):
        links.append(link.get('href'))

    # get names
    names = []
    for link in bbs.find_all('a', attrs={"class": "truetit"}):
        names. append(link.get_text())

    # get the links we are interested in by keyword in name
    interested_links = []
    url = 'https://bbs.hupu.com'
    if not len(keywords) == 0:
        for key in keywords:
            for i in range(len(names)):
                if key in names[i]:
                    interested_links.append(url + links[i])
    else:
        for i in range(len(names)):
            interested_links.append(url + links[i])

    # get images
    for l in interested_links:
        getImage(l, savepath)

if __name__ == "__main__":
    keywords = ["美腿", "实战利器", "这波", "打分", "爆照"]
    start = time.time()
    url = "https://bbs.hupu.com/selfie"
    threads = []
    for i in range(1, 10):
        t = threading.Thread(target=run, args=(url + "-" + str(i + 1), "./images/" + str(i) + "/", keywords))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    end = time.time()
    print("the program uses " + str(end - start) + "seconds to run with 10 threads")