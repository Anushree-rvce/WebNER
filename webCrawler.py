from bs4 import BeautifulSoup
import requests
from os.path import isfile
from os import rename,remove

XML_FILE = ""
DOMAIN =  "http://www.flipkart.com"
ProductID = []

def uniquePid(link):
    '''
    checks for unique product IDs to remove duplicates
    :param link: the link name (string)
    :return: returns False if the link is not unique is not a valid product page, else returns the link in formatted manner
    '''
    if not 'pid' in link:
        return False
    x = link.index('pid')
    if '&' in link:
        y = link.index('&')
        link = link[:y]
    pid = link[x+4:]
    if pid in ProductID:
        return False
    else:
        ProductID.append(pid)
        return link


def getBasicURLS():
    '''
    Gets the start urls from the given xml file
    :return: returns all the start urls
    '''
    try:
        if len(XML_FILE)!=0:
            content = BeautifulSoup(open(XML_FILE))
            allBasicURL = content.find_all("loc")
            return allBasicURL
        else:
            raise Exception("XML FILE name not found")
    except Exception as err:
        print(str(err))
        raise err

def getPageURLS(webpageContent, writeMode = 0):
    '''
    This gives all the urls present in a given webpage
    :param webpageContent:
    :param writeMode: 0 - Do no write to file, 1 - write to file
    :return: number of links extracted and the filename(if created)
    '''
    contentBS = BeautifulSoup(webpageContent)
    anchorTags = contentBS.find_all('a',attrs={'target':'_blank'})
    links = []
    count = 0
    for tag in anchorTags:
        productLink = tag.get('href')
        if productLink=="/returnpolicy":
            break
        if productLink==None:
            continue
        links.append(DOMAIN + productLink)
        count += 1
    if writeMode==1:
        filename = XML_FILE[:-4]+".txt"
        with open(filename,"a") as filePtr:
            for link in links:
                filePtr.write(link)
                filePtr.write("\n")
        print("Links stored in the file: "+filename)
        return count,filename
    return count

def removeDuplicates(filename):
    '''
    This module removes duplicates of the product website entries
    :param filename: Name of the file from which duplicate links have to be removed
    :return: None
    '''
    newFileName = filename.replace(".txt","2.txt")
    newFilePtr = open(newFileName,"w")
    with open(filename,"r") as filePtr:
        links = filePtr.read().split("\n")
        actualCount = len(links)
        neatCount = 0
        for link in links:
            neatURL = uniquePid(link)
            if neatURL == False:
                continue
            newFilePtr.write(neatURL)
            newFilePtr.write("\n")
            neatCount += 1
    print("Number of duplicates removed: "+str(actualCount-neatCount))
    newFilePtr.close()


if __name__=="__main__":
    filename = raw_input("Enter the XML file name: ")
    if isfile(filename):
        XML_FILE = filename
        URLS = getBasicURLS()
    else:
        raise Exception((filename+" does not exist"))

    for url in URLS:
        webpage = requests.get(url.string)
        no_of_links,filename = getPageURLS(webpage.content,writeMode=1)
        print("url: "+url.string+" Number of links: "+str(no_of_links))
        removeDuplicates(filename)

