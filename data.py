from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
poorname=[] #List to store the name of the product
pprices=[]
for i in range(0,15):
 url="https://www.poorvika.com/s?categories_slug=categories_slug%3A%3D%5B%60smartphones%60%5D&stock_status=stock_status%3A%3D%5B%60In+Stock%60%5D&page="+str(i)
 response = requests.get(url)
 htmlcontent = response.content
 soup = BeautifulSoup(htmlcontent,"html.parser")
 print(soup.prettify)
 for data in soup.findAll('div',class_='product-cardlist_card__description__eduH5'):
    print(data)
    names=data.find('b')
    price=data.find('span', attrs={'class':'whitespace-nowrap'})
    poorname.append(names.text) # Add product name to list
    pprices.append(price.text[2:])
    respo= dict(zip(poorname,pprices))
#print(respo)
#print(len(products))
#print(len(prices))
pdf=pd.DataFrame({"Productname":poorname,"Product Prices":pprices})
print(pdf)
pdf.to_csv("amazon.csv")
res = dict(zip(poorname,pprices))
print(res)
#inp1=input()
#price1=res.get(inp1)
########################### FLIPKART ###########################
flipname=[] #List to store the name of the product
fprices=[]
for i in range(0,15):
 url="https://www.flipkart.com/mobiles/pr?sid=tyy,4io&otracker=categorree&page="+str(i)
 response = requests.get(url)
 htmlcontent = response.content
 soup = BeautifulSoup(htmlcontent,"html.parser")
 print(soup.prettify)
 for data in soup.findAll('div',class_='_3pLy-c row'):
    print(data)
    names=data.find('div',class_='_4rR01T').get_text()
    price=data.find('div', attrs={'class':'_30jeq3 _1_WHN1'})
    flipname.append(names) # Add product name to list
    fprices.append(price.text[1:])
    respo= dict(zip(flipname,fprices))
#print(respo)
#print(len(products))
#print(len(prices))
fdf=pd.DataFrame({"Productname":flipname,"Product Prices":fprices})
print(fdf)
fdf.to_csv("Flipkart.csv")
res = dict(zip(flipname,fprices))
print(res)
#inp1=input()
#price1=res.get(inp1)
##################################### CROMA #############################################
products=[] #List to store the name of the product
prices=[]

url="https://www.croma.com/campaign/deals/c/6444?q=%3Arelevance%3Alower_categories%3A95%3Alower_categories%3A97%3Adelivery_mode%3AHome+Delivery"
response = requests.get(url)
htmlcontent = response.content
soup = BeautifulSoup(htmlcontent,"html.parser")
print(soup.prettify)
for data in soup.findAll('div',class_='cp-product typ-plp plp-srp-typ'):
    names=data.find('a',attrs={'rel':'noopener noreferrer'})
    print(names)
    price=data.find('span', attrs={'class':'amount plp-srp-new-amount'})
    products.append(names.text) # Add product name to list
    prices.append(price.text[1:])
    respo= dict(zip(products,prices))
#print(respo)
#print(len(products))
#print(len(prices))
df=pd.DataFrame({"Productname":products,"Product Prices":prices})
print(df)
df.to_csv("croma.csv")
res = dict(zip(products,prices))
print(res)