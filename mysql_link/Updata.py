# 添加数据
import pymysql

db = pymysql.connect(host='localhost',
                     user='root',
                     password='root',
                     database='Crawler',
                     charset='utf8')
 
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
 
# # 使用 execute()  方法执行 SQL 查询 
# cursor.execute("SELECT VERSION()")

print ("数据库连接成功！")
 
# 关闭数据库连接
# db.close() 
# # 使用 fetchone() 方法获取单条数据.
# data = cursor.fetchone()
 