from ast import Str, keyword
from pickletools import read_decimalnl_short
from unicodedata import category
from yelpapi import YelpAPI
import csv
import time
import pickle
import datetime
from keeptrack import keeptrack_f


#TODO multiple city per keyword

api_key='insert key'
yelp_api = YelpAPI(api_key)
counter_api=0

def get_50_businesses_total(term_csv: str,location_csv: str,skipp: int): 
    "Gets 50 biz , total results "
    term=f'{term_csv}'
    location=f'{location_csv}'
    time.sleep(2)
    counter_api_req=keeptrack_f()
    if counter_api_req < 4900:
        search_results = yelp_api.search_query(categories=term,location=location,limit=50,offset=skipp)
        print(location,term)
        print("Till now",counter_api_req,"Requests to Yelp for today")
    # print(search_results)
    # print("======")
    print(search_results['total'])
    return search_results['total'],search_results['businesses']

# get_total('electrician','austin tx')
line_count=0
def read_csv_to_list(filename):
    """Returns listofdicts, colum names"""
    with open(f'{filename}') as csvfile:
        csv_reader = csv.DictReader(csvfile,delimiter=';')
        list_of_dict_csv=list(csv_reader)
        columns=csv_reader.fieldnames
        return list_of_dict_csv,columns

def write_to_csv(filename,columns,rows):
    """
    parameters filename, column names, rows(list of dict)
    """
    with open(f'{filename}','a') as f:
        csv_writer = csv.DictWriter(f, columns,delimiter=';')
        csv_writer.writeheader()
        csv_writer.writerows(rows)       
def update_10_rows(list_of_dict_csv, columns,column_pointer):
    counter=1
    for index,row in enumerate(list_of_dict_csv):
        if index != 10000:
            row['city']
            search_term=columns[column_pointer]
            columns[1].strip()
            if row[search_term] is None or row[search_term]=='':
                total=get_total(term_csv=columns[column_pointer].strip(),location_csv=row['city'])
                row[search_term]=total
                counter+=1
            if counter == 10:
                return (list_of_dict_csv,counter)
    return (list_of_dict_csv,counter)

def write_10_results(column_pointer):
    
    list_of_dict_csv,columns=read_csv_to_list('yelp.csv')
    rows,counter=update_10_rows(list_of_dict_csv, columns,column_pointer=column_pointer)           
    write_to_csv('yelp.csv',columns,rows)
    return counter




#start main 
#get no of columns 
list_of_dict_csv,columns=read_csv_to_list('yelp.csv')
#iterate columns
# for column_pointer in range(1,len(columns)):
#     # iterate every 10 saves
#     counter =2
#     while counter > 1:
#         counter=write_10_results(column_pointer)  
#         print("Counter",counter)
    # end iterate every 10 saves

def get_all_results_per_city(city,keyword):
    skippint=0
    total_businesses_start=100000000
    total_biz_fetched=[]
    biz_batch_of50_dict=[]
    keylock=1
    biz_listing={}
    while total_businesses_start >50:
        print("skip",skippint)
        total_businesses,biz_batch_of50=get_50_businesses_total(keyword,city,skipp=skippint)
        if keylock==1:
            total_businesses_start=total_businesses
        
        print("tot biz start",total_businesses_start)
        if keylock==0:
            total_businesses_start-=50
        keylock=0 # for total biz start and for missing a turn    
        skippint+=50
    
    
        for el in biz_batch_of50:
            biz_listing["id"]=el["id"]
            biz_listing["city"]=el["location"]['city']
            biz_listing["state"]=el["location"]['state']
            biz_listing["zipcode"]=el["location"]['zip_code']
            categories_list=str(el['categories'][0])
            categories_list=categories_list.strip("{").strip('}').strip("]").strip('[')
        # if len(el['categories'])>1:
        #     for i in range(0,len(el['categories'])):
        #         categories_list.append(el['categories'][i]['alias'])
        # else:
        #     categories_list.append(el['categories'][i]['alias'])
        
            biz_listing["categories"]=str(categories_list)
            biz_listing["rating"]=el["rating"]
            biz_listing["review_count"]=el["review_count"]
            biz_listing["url"]=el["url"]
            biz_listing["is_closed"]=el["is_closed"]
            biz_listing["name"]=el["name"]
            if biz_listing["city"].lower()==city.split(",")[0].lower():
                biz_batch_of50_dict.append(biz_listing.copy())
# total_biz_fetched.append(biz_batch_of50_dict
    write_to_csv('yelpbizlist.csv',columns=["id","name","is_closed",'url','review_count','rating','categories','city','state','zipcode'],rows=biz_batch_of50_dict)
def get_city_list_keyword():
    f,columns=read_csv_to_list('citylist.txt')
    
    line=0 
    citylist=[]
    for row in f:
        if line==0:
            keyword=row
            line=2
        else:
            citylist.append(row)
    return citylist,keyword


citylist,keyword=get_city_list_keyword()

for city in citylist:
    get_all_results_per_city(city['items'],keyword['items'])