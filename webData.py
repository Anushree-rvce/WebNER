import requests
from bs4 import BeautifulSoup

def specifications(url):
    '''
    This funtion is used to extract the required details of any product
    :param url: The URL of any given webpage
    :return: None
    '''
    #Identify the product ID
    x = url.index('pid')
    pid = url[x+4:]
    print("pid: "+pid)

    #Get the webpage
    page = requests.get(url)
    bs = BeautifulSoup(page.content)

    #Create a .txt file to store the data
    filename = "K:\\WebScrapping\\Data\\"+pid+".txt"
    filePtr = open(filename,"w")

    #Fetches the product name from the page
    product_name = bs.find("h1",attrs={"class":"_3eAQiD"})
    prod = "Product Name: "+product_name.text
    prod = prod.encode('utf-8')
    print prod
    filePtr.write(prod)
    filePtr.write("\n")

    #Specific class names of those attribute values that are required
    attr = {"Ratings": "hGSR34 _2beYZw", "Price": "_1vC4OE _37U4_g", "Desc": "bzeytq _3cTEY2"}
    details = bs.findAll("div", attrs={"class": attr.values()})

    #Write the values into the file
    for i,j in zip(attr,details):
        s = i+": "+j.text.strip()
        s = s.encode('utf-8')
        filePtr.write(s)
        filePtr.write("\n")
        print s
    filePtr.write("\n")

    #The below class contains the entire product specifications
    spec_tag = bs.findAll("div", attrs={"class": "_2Kp3n6"})
    for tag in spec_tag:
        #Each element within this div class is explored and written into the file
        head = tag.find("div").text + ":-"
        filePtr.write(head)
        filePtr.write("\n")
        #print (head)
        points = tag.findAll("li")
        for j in points:
            feature_name = j.findAll("div")
            feature_value = j.findAll("li")
            for k, l in zip(feature_name,feature_value):
                feature = k.text+": "+l.text
                feature = feature.encode('utf-8')
                filePtr.write(feature)
                filePtr.write("\n")
                #print feature
        filePtr.write("\n")
    filePtr.close()
if __name__=="__main__":
    #booksv2.txt - contains the urls of books available on flipkart
    #mobilesv2.txt - contains the urls of books available on flipkart
    #watchesv2.txt - contains the urls of books available on flipkart
    with open("booksv2.txt","r") as f:
        urls = f.read().split("\n")
    for url in urls:
        specifications(url)

