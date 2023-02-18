from pyrogram import Client, filters
import mysql.connector
import os
from pyrogram.types import Message

STRING_SESSION = ""

BOT_TOKEN = ""
API_ID = 
API_HASH = ""


mydb =  mysql.connector.connect(
    user="root",
    host="containers-us-west-158.railway.app",
    password="BWOJOjg91LL9sFhvi4sR",
    port="7781",
    database="railway"
)
mycursor = mydb.cursor()


m = Client(
    "m",
    session_string=STRING_SESSION,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

chats = []
db = {}

x = mycursor.execute("SELECT * FROM db")
for x in mycursor:
    key = x[1]
    val = x[2]
    if db.get(x[1]) is not None:
        db[key].append(val)
    else:
        db[key] = [val]

chats = list(db.keys())
print("db:", db)
print("chats: ",chats)



@m.on_message(filters.regex(".ok"))
async def my_handler(client, message):
    if message.reply_to_message:
        key = message.chat.id
        value= message.reply_to_message.from_user.id
        await message.delete() 
        if db.get(key) is not None:
            db[key].append(value)
        else:
            db[key] = [value]
            chats.append(key)



        sql = "INSERT INTO db (chat_id, user_id) VALUES (%s, %s)"
        val = (key, value)
        mycursor.execute(sql, val)        
        mydb.commit()
        


@m.on_message(filters.chat(chats))
async def from_pyrogramchat(hey: Client, message: Message):
    if message.from_user.id in db[message.chat.id]:
        a = message.from_user.first_name
        b = message.from_user.last_name
        u = message.from_user.username
        k = message.text

        if k == None:
            k = "not a text"
        elif u == None:
            await message.forward(-1001813754246, k)
            print(a + b + ":" + " " + k)
        else:
            await message.forward(-1001813754246, k)
            print(u + ":" + " " + k)


m.run()
