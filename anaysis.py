import json
from collections import defaultdict
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

#connect MongoDB
from pymongo import MongoClient
conn = MongoClient('mongodb://localhost:27017/')
db = conn.mobileSalesDB
collection = db.colloections

# load ptt posts
path = 'mobileSales.json'
with open(path) as f:
    posts = json.load(f)

def store_data_to_database(posts):
	for post in posts:
		collection.insert({"modelName":"iphone"+post['modelName'],
			'storage_size':post['storageSize'],'price':str(post['price']).ljust(5,"0")
			,'date':post['date'],'status':post['status']})

def show_results():
	#get iphoneX 256G average price from 12/05 to 12/30
	priceNew = []
	priceOld = []
	date = ['12-05','12-10','12-15','12-20','12-25','12-30']
	
	#new price
	priceTmp = 0
	count = 0
	for i in collection.find({'modelName': 'iphoneX','status':'new','storage_size': '256','date':{"$gt":"2017-11-30","$lt":"2017-12-06"}}): 
		priceTmp += int(i.get('price'))
		count +=1
	priceNew.append(priceTmp/count)
	priceTmp = 0
	count = 0
	for i in collection.find({'modelName': 'iphoneX','status':'new','storage_size': '256','date':{"$gt":"2017-12-05","$lt":"2017-12-11"}}): 
		priceTmp += int(i.get('price'))
		count +=1
	priceNew.append(priceTmp/count)	
	priceTmp = 0
	count = 0
	for i in collection.find({'modelName': 'iphoneX','status':'new','storage_size': '256','date':{"$gt":"2017-12-10","$lt":"2017-12-16"}}): 
		priceTmp += int(i.get('price'))
		count +=1
	priceNew.append(priceTmp/count)
	priceTmp = 0
	count = 0
	for i in collection.find({'modelName': 'iphoneX','status':'new','storage_size': '256','date':{"$gt":"2017-12-15","$lt":"2017-12-21"}}): 
		priceTmp += int(i.get('price'))
		count +=1
	priceNew.append(priceTmp/count)
	priceTmp = 0
	count = 0
	for i in collection.find({'modelName': 'iphoneX','status':'new','storage_size': '256','date':{"$gt":"2017-12-20","$lt":"2017-12-26"}}): 
		priceTmp += int(i.get('price'))
		count +=1
	priceNew.append(priceTmp/count)
	priceTmp = 0
	count = 0
	for i in collection.find({'modelName': 'iphoneX','status':'new','storage_size': '256','date':{"$gt":"2017-12-25","$lt":"2017-12-31"}}): 
		priceTmp += int(i.get('price'))
		count +=1
	priceNew.append(priceTmp/count)
	priceTmp = 0	
	count = 0
	
	#old price
	for i in collection.find({'modelName': 'iphoneX','status':'old','storage_size': '256','date':{"$gt":"2017-11-30","$lt":"2017-12-06"}}): 
		priceTmp += int(i.get('price'))
		count +=1
	priceOld.append(priceTmp/count)
	priceTmp = 0
	count = 0
	for i in collection.find({'modelName': 'iphoneX','status':'old','storage_size': '256','date':{"$gt":"2017-12-05","$lt":"2017-12-11"}}): 
		priceTmp += int(i.get('price'))
		count +=1
	priceOld.append(priceTmp/count)	
	priceTmp = 0
	count = 0
	for i in collection.find({'modelName': 'iphoneX','status':'old','storage_size': '256','date':{"$gt":"2017-12-10","$lt":"2017-12-16"}}): 
		priceTmp += int(i.get('price'))
		count +=1
	priceOld.append(priceTmp/count)
	priceTmp = 0
	count = 0
	for i in collection.find({'modelName': 'iphoneX','status':'old','storage_size': '256','date':{"$gt":"2017-12-15","$lt":"2017-12-21"}}): 
		priceTmp += int(i.get('price'))
		count +=1
	priceOld.append(priceTmp/count)
	priceTmp = 0
	count = 0
	for i in collection.find({'modelName': 'iphoneX','status':'old','storage_size': '256','date':{"$gt":"2017-12-20","$lt":"2017-12-26"}}): 
		priceTmp += int(i.get('price'))
		count +=1
	priceOld.append(priceTmp/count)
	priceTmp = 0
	count = 0
	for i in collection.find({'modelName': 'iphoneX','status':'old','storage_size': '256','date':{"$gt":"2017-12-25","$lt":"2017-12-31"}}): 
		priceTmp += int(i.get('price'))
		count +=1
	priceOld.append(priceTmp/count)	
	
	#plot
	f, ax = plt.subplots(figsize=(10, 6))
	plt.ylabel('price')
	plt.xlabel('date')

	plt.plot(date,priceNew,label='new',color='blue')
	plt.plot(date,priceOld,label='old',color='red')
	ax.legend(ncol=2, loc='upper right', frameon=True)
	plt.show()

#store_data_to_database(posts)
show_results()
