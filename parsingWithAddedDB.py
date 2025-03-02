import vk_api
import csv
from pymongo import MongoClient
import pandas as pd
import json

client = MongoClient("localhost", 27017)

database = client["Posts"]
Post = database.postFromParser

session = vk_api.VkApi(token='698e97510f36f88ced18449a9aa25c9663b8e2eeb1f42a857c3c5c2a65be69d5d90b645e12313d090aad7')
vk = session.get_api()
global j,i
myData = [["post_number", "first_name", "second_name","comment","city","country","education","occupation" ]]
text=""
name=''
lastname=''
def get_comments (group_id):
    Wall= session.method('wall.get', {"owner_id": group_id})
    count= Wall["count"]
    print(count)
    j=0
    i=0
    print ("Сколько постов вам надо добавить?")
    k=input()
    while j <count :
        Wall= session.method('wall.get', {"owner_id": group_id, 'offset': j})
        for post in Wall['items']:
            j=j+1
           # if post['date'] <= 1633392055 :     ограничение по дате, мол, получить все посты до этого момента. Время в формате SuperTIme вроде так называется. Если не нужно, комменть эти две строки
          #      j=count+1
           #     break
            if i > k:
                j=count+1
                break

            print("Пост номер ", post['id']) #Выписывать номер текущего поста, чтобы понимать, на каком сейчас месте программа
            comments = session.method('wall.getComments', {"owner_id": group_id, "post_id": post['id'], "extended":1 })
            ident= str('group_id') + '_' + str('j')
            posts = session.method('wall.getById', {"posts": ident })
            for comment in comments["items"]:
                from_id = comment["from_id"]
                if from_id <= 0:
                    continue

                user = session.method("users.get", {"user_ids": from_id,"fields": "city,country,education,occupation"})
                name = user[0]['first_name']
                lastname = user[0]['last_name']
                try:
                    city = user[0]["city"]
                    city=city["title"]
                except:
                    city="0"
                try:
                    country = user[0]["country"]
                    country=country["title"]
                except:
                    country="0"
                try:
                    education = user[0]["education"]
                    education=education["university_name"]
                except:
                    education="0"
                try:
                    occupation = user[0]["occupation"]
                    occupation=occupation["name"]
                except:
                    occupation="0"

                for post in posts:
                    global text
                    text=post['text']
                myData.append([j, name ,lastname, comment['text'],city,country,education,occupation])
                i = i+1




print ("Введите id группы или человека. ID группы начинается с -. То есть -1231231, а не 1231231")
group_id=int(input())
get_comments(group_id)
print ('Цикл завершен')

myFile = open('DB.csv', 'w', encoding='utf-16')

with myFile:
    writer = csv.writer(myFile)
    writer.writerows(myData)

print("Запись завершена")

def csv_to_json(filename):
    data = pd.read_csv(filename, encoding='utf-16')
    print(data)
    return data.to_dict('records')

x= Post.insert_many(csv_to_json('DB.csv')).inserted_ids
print(x)
