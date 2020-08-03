import pymysql


class ConnDB(object):
    def __init__(self, db_info):
        self.host = db_info['host']
        self.port = db_info['port']
        self.user = db_info['user']
        self.password = db_info['password']
        self.db = db_info['db']

    def insert(self, table, value_dict):
        try:
            conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db)
            cur = conn.cursor()
            sql = 'insert into {} ({}) values ({})'.format('movies_info', ','.join(value_dict.keys()), ','.join(list(map(lambda x: "'" + x + "'", value_dict.values()))))
            print(sql)
            cur.execute(sql)
            cur.close()
            conn.commit()
        except Exception as e:
            print('执行脚本失败:%s' % e)
            conn.rollback
        finally:
            conn.close()
