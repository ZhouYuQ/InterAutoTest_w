# 导入pymysql包
import pymysql

from utils.LogUtil import my_log


# 1.创建封装类
class Mysql:
# 2.初始化数据，连接数据库，光标对象
    def __init__(self,host,user,passeord,database,charset="utf-8",port="3306"):
        # 链接database
        self.log = my_log()
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=passeord,
            database=database,
            charset=charset,
            port=port
        )
        # 3.获取执行sql的光标对象
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
# 3.创建查询、执行方法
    def fetchone(self,sql):
        """
        单个查新
        :param sql:
        :return:
        """
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def fetchall(self,sql):
        """
        多个查询
        :return:
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def exec(self,sql):
        """
        执行
        :return:
        """
        try:
            if self.conn and self.cursor:
                self.cursor.execute(sql)
                self.conn.commit()
        except Exception as ex:
            self.conn.rollback()
            self.log.error("Mysql执行失败")
            self.log.error(ex)
            return False
        return True

# 4.关闭对象
    def __del__(self):
        # 关闭游标
        if self.cursor is not None:
            self.cursor.close()
        # 关闭数据库连接对象
        if self.conn is not None:
            self.conn.close()

if __name__ == '__main__':
    mysql = Mysql("211.103.136.242",
                  "test",
                  "test123456",
                  "meiduo",
                  charset="utf8",
                  port=7090)
    res =  mysql.fetchall("select id,username,mobile,email from tb_users where username='python';")
    print(res)

    # 1.创建db_conf.yml,db1,db2
    # 2.编写数据库基本信息
    # 3.重构Conf.py
    # 4.执行


