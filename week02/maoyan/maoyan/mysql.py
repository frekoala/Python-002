import pymysql


class ConnDB(object):
    def __init__(self, db_info):
        self.host = db_info['host']
        self.port = db_info['port']
        self.user = db_info['user']
        self.password = db_info['password']
        self.db = db_info['db']
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db)

    def getcur(self):
        self.cur = self.conn.cursor()
        return self.cur

    def insert(self, table, value_dict):
        try:
            sql = 'insert into {} ({}) values ({})'.format('movies_info', ','.join(value_dict.keys()), ','.join(list(map(lambda x: "'" + x + "'", value_dict.values()))))
            print(sql)
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print('执行脚本失败:%s' % e)
            self.conn.rollback

    def close(self):
        self.cur.close()
        self.conn.close()
