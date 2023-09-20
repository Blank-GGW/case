   
链接数据库方法：
   导入pymysql之前需要先安装pymysql模块
   		方法一:直接在pycharm编译器里面输入	pip install pymysql
   		
   		方法二:win+r --> 输入cmd -->在里面输入pip install pymysql
   		
   	ps:在cmd中输入pip list后回车 可以找到安装的pymysql就表示安装成功了

coon = pymysql.connect(host='127.0.0.1', user='root', password='123456', database='pymysql_test')
使用 cursor() 方法创建一个游标对象:cursor
cursor = coon.cursor()

host:也可以为localhost
user:是你的数据库用户名
password:数据库密码
database:你已经创建好的数据库

数据库建表操作：
cursor.execute(
'''create table if not exists pets(id int primary key  auto_increment,
   src varchar(50),
   skill varchar(100)''')

添加数据：
sql = '''insert into test_mysql(id,src,skill) values(%d,%s,%s)'''
	ps: test_mysql 是你连接到的数据库中的一张表
		id,src,skill 这个是你创建表时所定义的字段关键字
		%d,%s,%s 这个要根据你创建的字段关键字的类型而定,记住要一一对应

