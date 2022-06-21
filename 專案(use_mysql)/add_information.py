import pymysql
db_settings = {
    "host": "180.218.7.38",
    "port": 3306,
    "user": "root",
    "password": "5698741",
    "db": "video_imformation",
    "charset": "utf8"
}

db = pymysql.connect(**db_settings)
cursor = db.cursor()# 使用 cursor() 方法創造操作游標 cursor
sql=""
#
ID=0
name="NULL"
web="NULL"


def add_new_video(ID , name , web , Author):
    #新增資料用SQL指令
    if(ID!=0 and name!="NULL" and web!="NULL"):
        sql = "INSERT INTO data \
          ( id , name , web , Author) \
          VALUES ( %s , %s , %s , %s)"

        cursor.execute(sql,(ID , name , web , Author))
    else:
        pass
    db.commit()

def search_video(names):
    global video_name , web_name , Author_name
    video_name = []
    web_name = []
    Author_name = []
    #搜尋所有資料用的SQL指令
    sql = "SELECT * FROM data  \
           WHERE name = '%s' "%(names)
    cursor.execute(sql)
    commodity = cursor.fetchall()
    if commodity != () :
        for row in commodity:
            video_name.append(row[1])
            web_name.append(row[2])
            Author_name.append(row[3])
        return video_name , web_name , Author_name
    else:
        return "NULL"
    db.commit()

def count():
    number_of_rows = cursor.execute("SELECT * FROM data")
    db.commit()
    return number_of_rows

def search_IP(IP):
    #搜尋所有資料用的SQL指令
    sql = "SELECT * FROM Loading_ip  \
           WHERE IP = '%s' "%(IP)
    cursor.execute(sql)
    commodity = cursor.fetchall()
    if commodity != () :
        return 1
    else:
        return 0
    db.commit()

def add_new_ip(IP):
    #新增資料用SQL指令
    x = search_IP(IP)
    if(ID!="NULL" and x!=1):
        sql = "INSERT INTO Loading_ip \
          ( ip) \
          VALUES ( %s )"

        cursor.execute(sql,(IP))
        print("已新增 IP: %s " %(IP))
    else:print("NO NO NO~~~")
    db.commit()

def Delete_IP(IP):
    sql= "DELETE FROM loading_ip \
          WHERE IP = '%s'"  %(IP)
    
    cursor.execute(sql)
    print("已刪除 IP: %s " %(IP))
    db.commit()


