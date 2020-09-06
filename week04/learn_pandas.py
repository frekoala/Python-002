import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine


db_info = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '111111',
    'db': 'test',
    'charset': 'utf8'
}


group = ['x','y','z']
data = pd.DataFrame({
    "id": np.random.randint(1,2000,20),
    "group":[group[x] for x in np.random.randint(0,len(group),20)] ,
    "age":np.random.randint(15,50,20)
    })

# 多对一替换
data.replace([24,25,26,27,28], np.NaN,inplace=True)
# data.replace(regex=r'.*',value=111)
data.loc[[2,5,6],['id']] = np.NaN

table1 = pd.DataFrame({
    "id" : np.random.randint(1,20,20),
    "order_id" : np.random.randint(100,130,20),
    "group":[group[x] for x in np.random.randint(0,len(group),20)] ,
    "age":np.random.randint(15,50,20)
})

# 多对一替换
table1.replace([109,111,105], np.NaN,inplace=True)
# data.replace(regex=r'.*',value=111)
table1.loc[[3,15,9],['id']] = np.NaN

table2 = pd.DataFrame({
    "id": np.random.randint(1,20,20),
    "order_id": np.random.randint(100,500,20),
    "group": [group[x] for x in np.random.randint(0,len(group),20)] ,
    "age": np.random.randint(15,50,20)
})

# 多对一替换
table2.replace([i for i in range(200,300)], np.NaN,inplace=True)
# data.replace(regex=r'.*',value=111)
table2.loc[[3,15,9],['id']] = np.NaN

#在数据库创建与pandas对应的表及数据
engine = create_engine('mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(db)s?charset=%(charset)s'%db_info, encoding='utf-8')
data.to_sql('data', con=engine, if_exists='replace')
table1.to_sql('table1', con=engine, if_exists='replace')
table2.to_sql('table2', con=engine, if_exists='replace')

def query_from_mysql(sql, num):
    try:
        db_conn = pymysql.connect(**db_info)
        db_cur = db_conn.cursor()
        db_cur.execute(sql)       
        print('-'*10 + 'case%s query_from_mysql'%num + '-'*10)
        for i in db_cur.fetchall():
            print('\t'.join('%s'%id for id in i))
    except Exception as e:
        print("执行脚本失败:%s" % e) 
    finally:
        db_cur.close()
        db_conn.close()

def excute_from_mysql(sql, num):
    try:
        db_conn = pymysql.connect(**db_info)
        db_cur = db_conn.cursor()
        print('-'*10 + 'case%s excute_from_mysql successful'%num + '-'*10)
        db_cur.execute(sql)  
        db_conn.commit()     
    except Exception as e:
        print("执行脚本失败:%s" % e) 
        db_conn.rollback
    finally:
        db_cur.close()
        db_conn.close()
    


def case1():
    sql = """SELECT * FROM data"""
    query_from_mysql(sql,1)
    print('-'*10 + 'case1 query_from_pandas' + '-'*10)
    print(data)

def case2():
    sql = """SELECT * FROM data LIMIT 10"""
    query_from_mysql(sql,2)
    print('-'*10 + 'case2 query_from_pandas' + '-'*10)
    print(data[0:10])

def case3():
    sql = """SELECT id FROM data"""
    query_from_mysql(sql,3)
    print('-'*10 + 'case3 query_from_pandas' + '-'*10)
    print(data['id'])

def case4():
    sql = """SELECT COUNT(id) FROM data"""
    query_from_mysql(sql,4)
    print('-'*10 + 'case4 query_from_pandas' + '-'*10)
    print(data['id'].count())

def case5():
    sql = """SELECT * FROM data WHERE id<1000 AND age>30"""
    query_from_mysql(sql,5)
    print('-'*10 + 'case5 query_from_pandas' + '-'*10)
    print(data[(data['id']<1000) & (data['age']>30)])

def case6():
    sql = """SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id"""
    query_from_mysql(sql,6)
    print('-'*10 + 'case6 query_from_pandas' + '-'*10)
    print(table1.groupby('id').aggregate({'order_id':'count'}))

#因mysql查询与pandas打印顺序不一致，为方便比较，在第7行语句的基础上增加排序
def case7():
    sql = """SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id order by t1.id"""
    query_from_mysql(sql,7)
    print('-'*10 + 'case7 query_from_pandas' + '-'*10)
    print(pd.merge(table1, table2, on='id',how='inner').sort_values(by='id', ascending=True))

def case8():
    sql = """SELECT * FROM table1 UNION SELECT * FROM table2"""
    query_from_mysql(sql,8)
    print('-'*10 + 'case8 query_from_pandas' + '-'*10)
    print(pd.concat([table1,table2]))

# 为方便数据比较，删除后增加sql查询
def case9():
    sql = """DELETE FROM table1 WHERE id=10"""
    excute_from_mysql(sql,9)
    sql = """select * from table1 order by id,order_id"""
    query_from_mysql(sql,9)
    print('-'*10 + 'case9 query_from_pandas' + '-'*10)
    print(table1[table1['id'] != 10].sort_values(by=['id','order_id'],ascending=True))

# 为方便数据比较，删除字段后增加sql查询
def case10():
    sql = """ALTER TABLE table1 DROP COLUMN id"""
    excute_from_mysql(sql,10)
    sql = """select * from table1"""
    query_from_mysql(sql,10)
    print('-'*10 + 'case10 query_from_pandas' + '-'*10)
    print(table1.drop('id', axis=1))




if __name__ == "__main__":
    case1()
    case2()
    case3()
    case4()
    case5()
    case6()
    case7()
    case8()
    case9()
    case10()