import requests
import pymysql
from lxml import etree
from time import sleep

'''
    完整的、简单的例子：创建表、链接数据库、添加数据，查找数据
'''

# 数据库链接
conn = pymysql.connect(host='127.0.0.1', user='root',
                       password='root', database='Crawler')
cursor = conn.cursor()
# 执行一条创建表的操作
cursor.execute(
    '''CREATE TABLE
IF
	NOT EXISTS petsValue (
		NAME VARCHAR ( 50 ) NOT NULL PRIMARY KEY,
		LEVEL VARCHAR ( 100 ),
		property VARCHAR ( 100 ),
		type VARCHAR ( 100 ),
		target VARCHAR ( 100 ),
		power VARCHAR ( 100 ),
		pp VARCHAR ( 100 ),
		result text 
	)''');(
    '''CREATE TABLE
IF
	NOT EXISTS pets (
		NAME VARCHAR ( 50 ),
		src VARCHAR ( 100 ),
		petsValuename VARCHAR ( 100 ),
		PRIMARY KEY (`Name`),
		UNIQUE KEY `Name` ( `Name` ),
		CONSTRAINT `FK_petsValue` FOREIGN KEY ( `petsValuename` ) REFERENCES `petsValue` ( `name` ) 
	)''')

url = 'http://news.4399.com/luoke/luokechongwu/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
}

response = requests.get(url=url, headers=headers)
response.encoding = 'gbk'

html = response.text
# print(html)

# 宠物名称
# 宠物图片(图片在 lz_src)
# 宠物技能(跳转详细页)

# tree = etree.HTML(html)
tree = etree.HTML(html)  # type: ignore
li_list = tree.xpath('//ul[@id="cwdz_list"]/li')  # 所有的宠物
for li in li_list:
    name = li.xpath('./@name')[0]  # 每一个宠物的名称
    src = 'http:' + li.xpath('./a/img/@lz_src')[0]  # 图片链接
    link = 'http://news.4399.com' + li.xpath('./a/@href')[0]  # 宠物的详细链接
    industry = []  # 数组里面存放每一个对象,每一个对象就是一个技能
    # 对详细链接发起请求,获取技能
    try:
        detail_resp = requests.get(url=link, headers=headers)
        sleep(0.5)
        detail_resp.encoding = 'gbk'
        detail_tree = etree.HTML(detail_resp.text)  # type: ignore

        # 技能
        skills = detail_tree.xpath(
            '/html/body/div[5]/div[2]/div[2]/div[1]/div[1]/table[4]/tbody/tr')
        del skills[0]
        del skills[0]
        item = {}
        for skill in skills:
            item['name'] = skill.xpath('./td[1]/text()')[0]  # 技能
            item['level'] = skill.xpath('./td[2]/text()')[0]  # 等级
            item['property'] = skill.xpath('./td[3]/text()')[0]  # 属性
            item['type'] = skill.xpath('./td[4]/text()')[0]  # 类型
            item['target'] = skill.xpath('./td[5]/text()')[0]  # 目标
            item['power'] = skill.xpath('./td[6]/text()')[0]  # 威力
            item['pp'] = skill.xpath('./td[7]/text()')[0]  # pp
            item['result'] = skill.xpath('./td[8]/text()')[0]  # 效果
            industry.append(item)
        sql_select = '''	SELECT name FROM crawler.petsvalue WHERE name = '{0}'
        '''.format(item['name'])
        result = cursor.execute(sql_select)
        rows = cursor.fetchall()
        if len(rows) > 0:
            print("已存在")
            continue
        # 数据保存 (mysql)
        sql_1 = '''insert into petsValue(name,level,property,type,target,power,pp,result) values (%s,%s,%s,%s,%s,%s,%s,%s)'''
        cursor.execute(sql_1, [item['name'], item['level'], item['property'],
                       item['type'], item['target'], item['power'], item['pp'], item['result']])
        # conn.commit()
        print(item['name'])
        sql = '''insert into pets(name,src,petsValuename) values (%s,%s,%s);'''
        cursor.execute(sql, [name, src, item['name']])
        conn.commit()
        print(f'{name}--保存成功!')
    except Exception as e:
        print(e)
        pass
cursor.close()
conn.close()
