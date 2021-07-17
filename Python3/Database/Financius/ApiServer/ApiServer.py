# -*-coding:utf8;-*-
# @desc:用于读取financius.db的数据并提供简单的查询修改接口
# @author:sinsen
# @date:2019年8月26日
import time
import json
import uuid
import sqlite3
from flask import Flask
from flask import url_for
from flask import request
from flask import jsonify

SHOW_SQL = True
IS_DEBUG = True
HOST = "localhost"
PORT = 8080


def log(msg):
    print(time.strftime("%Y-%m-%d %H:%M:%S"), msg)


def sql_log(sql, params=[]):
    if SHOW_SQL:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), sql, 'params:', params)


class ApiServer():
    class Msg:
        def __init__(self, msg, data=None, code=0):
            self.code = code
            self.msg = msg
            self.data = data

        def __str__(self):
            return str({"code": self.code, "msg": self.msg, "data": self.data, "time": time.strftime("%Y-%m-%d %H:%M:%S")})

    def __init__(self):
        self.db = sqlite3.connect("data/finance.db", check_same_thread=False)
        self.cursor = self.db.cursor()
        self.flaskServer = Flask(__name__)
        self.flaskServer.config["JSON_AS_ASCII"] = False
        self.flaskServer.add_url_rule("/", view_func=self.index)
        self.flaskServer.add_url_rule("/queryOne/<table_name>/<key_name>/<key_value>", view_func=self.query, endpoint="queryOne")
        self.flaskServer.add_url_rule("/queryMany/<table_name>/<key_name>/<key_values>", view_func=self.queryMany)
        self.flaskServer.add_url_rule("/insert/<table_name>", view_func=self.insert, methods=["POST", "GET"])
        self.flaskServer.add_url_rule("/insert/<table_name>/<key_name>", view_func=self.insert, methods=["POST", "GET"])
        self.flaskServer.add_url_rule("/update/<table_name>", view_func=self.update, methods=["POST", "GET"])
        self.flaskServer.add_url_rule("/update/<table_name>/<key_name>", view_func=self.update, methods=["POST", "GET"])
        self.flaskServer.add_url_rule("/queryTran/<tran_id>", view_func=self.query_tran)
        self.flaskServer.add_url_rule("/queryTranList", view_func=self.query_tran_list)
        self.flaskServer.add_url_rule("/queryTranList/<page>/<page_size>", view_func=self.query_tran_list)
        self.flaskServer.add_url_rule("/queryList/<table_name>", view_func=self.query_list)
        self.flaskServer.add_url_rule("/queryList/<table_name>/<page>/<page_size>", view_func=self.query_list)
        self.flaskServer.add_url_rule("/searchList/<table_name>/<key_names>/<key_values>", view_func=self.search_list)
        self.flaskServer.add_url_rule("/searchList/<table_name>/<key_names>/<key_values>/<page>/<page_size>", view_func=self.search_list)
        self.flaskServer.add_url_rule("/searchTranList/<key_names>/<key_values>", view_func=self.search_tran_list)
        self.flaskServer.add_url_rule("/searchTranList/<key_names>/<key_values>/<page>/<page_size>", view_func=self.search_tran_list)

    def index(self):
        routes = []
        for rule in self.flaskServer.url_map.iter_rules():
            routes.append({
                "url": str(rule),
                "endpoint": rule.endpoint,
                "methos": ','.join(rule.methods)
            })
        return jsonify(routes)

    def row_tojson(self, cursor_description, row):
        if row is None:
            return row
        json_data = {}
        i = 0
        for desc in cursor_description:
            json_data[desc[0]] = row[i]
            i += 1
        return json_data

    def query_to_json(self, table_name, key_name, key_value):
        sql = "select * from %s where %s='%s'" % (
            table_name, key_name, key_value)
        if SHOW_SQL:
            sql_log(sql, key_value)
        self.cursor.execute(sql)
        return self.row_tojson(self.cursor.description, self.cursor.fetchone())

    def query(self, table_name, key_name, key_value):
        return jsonify(self.query_to_json(table_name, key_name, key_value))

    def queryMany(self, table_name, key_name, key_values):
        params = key_values.split(",")
        params_str = ""
        i = len(params)
        for p in params:
            if(i != 1):
                params_str += p + "','"
            else:
                params_str += p
            i -= 1
        sql = "select * from %s where %s in ('%s')" % (
            table_name, key_name, params_str)
        if SHOW_SQL:
            sql_log(sql, params)
        self.cursor.execute(sql)
        rows = []
        for row in self.cursor.fetchall():
            rows.append(self.row_tojson(self.cursor.description, row))
        return jsonify(rows)

    def insert(self, table_name, key_name=None):
        if key_name is None:
            key_name = table_name + "_id"  # 这个是针对 finance.db 数据库的
        json_data = request.get_json()
        if json_data is None:
            return jsonify(-1)
        if json_data.has_key(key_name) == False or json_data[key_name] is None or len(json_data[key_name]) < 16:
            json_data[key_name] = str(uuid.uuid1())
        sql = "insert into %s(" % table_name
        i = len(json_data)
        for key in json_data:
            if(i != 1):
                sql += key + ","
            else:
                sql += key
            i -= 1
        sql += ")values('"
        i = len(json_data)
        for key in json_data:
            if(i != 1):
                sql += json_data[key] + "','"
            else:
                sql += json_data[key]
            i -= 1
        sql += "')"
        if SHOW_SQL:
            sql_log(sql, json_data)
        self.cursor.execute(sql, json_data)
        self.db.commit()
        return jsonify(self.cursor.lastrowid)

    def update(self, table_name, key_name=None):
        if key_name is None:
            return(-1)
        json_data = request.get_json()
        if json_data is None or json_data.has_key(key_name) == False or json_data[key_name] is None:
            return(-1)
        sql = "update %s set " % table_name
        i = len(json_data)
        for key in json_data:
            if(i != 1):
                sql += key + ("='%s', " % json_data[key])
            else:
                sql += key + ("='%s' " % json_data[key])
            i -= 1
        sql += " where 1=1 and %s='%s' " % (key_name, json_data[key_name])
        if SHOW_SQL:
            sql_log(sql, json_data)
        self.cursor.execute(sql)
        self.db.commit()
        return jsonify(self.cursor.rowcount)

    def start(self):
        self.flaskServer.run(host=HOST, port=PORT, debug=IS_DEBUG)

    def stop(self):
        self.db.close()

    ''' 一下方法是针对 Finance 数据库编写的 '''

    def query_tran(self, tran_id):
        tags = []
        account = []
        tran = self.query_to_json("transactions", "transactions_id", tran_id)
        if tran is None:
            return jsonify(tran)
        tran["transactions_account_from"] = self.query_to_json(
            "accounts", "accounts_id", tran["transactions_account_from_id"])
        tran["transactions_account_to"] = self.query_to_json(
            "accounts", "accounts_id", tran["transactions_account_to_id"])

        # tags
        tran["tags"] = tags
        sql = (
            "select * from transaction_tags where transaction_tags_transaction_id='%s'" % tran_id)
        if SHOW_SQL:
            sql_log(sql, None)
        self.cursor.execute(sql)
        for tags_id in self.cursor.fetchall():
            tag = self.query_to_json("tags", "tags_id", tags_id[1])
            tran["tags"].append(tag)

        return tran

    def query_tran_list(self, page=0, page_size=10):
        sql_count = "select count(1) from transactions where transactions_model_state=1"
        if SHOW_SQL:
            sql_log(sql_count)
        count = self.cursor.execute(sql_count).fetchone()[0]
        sql = "select DISTINCT transactions_id from transactions where transactions_model_state=1 order by transactions_date desc limit %d,%d" % (
            page, page_size)
        self.cursor.execute(sql)
        trans = []
        for trans_id in self.cursor.fetchall():
            trans.append(self.query_tran(trans_id[0]))
        return jsonify({"count": count, "data": trans, "maxpage": count/page_size+1})

    def search_tran_list(self, key_names, key_values, page=0, page_size=10):
        sql_as_view = '''
            (
            SELECT
                transactions._id,
                transactions.transactions_id,
                transactions.transactions_model_state,
                transactions.transactions_sync_state,
                transactions.transactions_account_from_id,
                transactions.transactions_account_to_id,
                transactions.transactions_category_id,
                transactions.transactions_date,
                transactions.transactions_amount,
                transactions.transactions_exchange_rate,
                transactions.transactions_note,
                transactions.transactions_state,
                transactions.transactions_type,
                transactions.transactions_include_in_reports,
                accounts.accounts_title,
                accounts.accounts_note,
                tags.tags_title,
                categories.categories_title
            FROM
                transactions
            LEFT JOIN categories ON categories_id = transactions_category_id
            LEFT JOIN accounts ON transactions_account_from_id = accounts_id
            OR transactions_account_to_id = accounts_id
            LEFT JOIN transaction_tags ON transactions_id = transaction_tags_transaction_id
            LEFT JOIN tags ON transaction_tags_tag_id = tags_id
        ) t
        '''
        '''
        sql_count = ("select count(1) from %s where transactions_model_state=1 and %s like '%%%s%%'" % (sql_as_view, key_name, key_value)).replace("\n","").replace("\t","").replace("     ","")
        if SHOW_SQL:sql_log(sql_count, (key_name, key_value))
        count = self.cursor.execute(sql_count).fetchone()[0]
        '''
        sql_where = ""
        key_names = key_names.split(",")
        key_values = key_values.split(",")
        i = len(key_names)
        kvalue = 0
        for keyname in key_names:
            if(i != 1):
                sql_where += keyname + \
                    " like '%%%s%%' and " % key_values[kvalue]
            else:
                sql_where += keyname + " like '%%%s%%'" % key_values[kvalue]
            i -= 1
            kvalue += 1
        sql = ("select DISTINCT transactions_id from %s where transactions_model_state=1 and (%s) order by transactions_date desc limit %d,%d" % (
            sql_as_view, sql_where, page, page_size)).replace("\n", "").replace("\t", "").replace("     ", "")
        if SHOW_SQL:
            sql_log(sql, (key_names, key_values))
        self.cursor.execute(sql)
        trans = []
        for trans_id in self.cursor.fetchall():
            trans.append(self.query_tran(trans_id[0]))
        return jsonify(trans)

    def query_list(self, table_name, page=0, page_size=10):
        sql_count = "select count(1) from %s where %s_model_state=1" % (
            table_name, table_name)
        if SHOW_SQL:
            sql_log(sql_count, (table_name, table_name))
        count = self.cursor.execute(sql_count).fetchone()[0]
        sql = "select DISTINCT _id from %s where %s_model_state=1 limit %d,%d" % (
            table_name, table_name, page, page_size)
        if SHOW_SQL:
            sql_log(sql, (table_name, page, page_size))
        self.cursor.execute(sql)
        datas = []
        for trans_id in self.cursor.fetchall():
            datas.append(self.query_to_json(table_name, "_id", trans_id[0]))
        return {"count": count, "data": datas, "maxpage": count/page_size+1}

    ''' 这个方法略作改过就可以做成通用的 '''

    def search_list(self, table_name, key_names, key_values, page=0, page_size=10):
        sql_where = ""
        key_names = key_names.split(",")
        key_values = key_values.split(",")
        i = len(key_names)
        kvalue = 0
        for keyname in key_names:
            if(i != 1):
                sql_where += keyname + \
                    " like '%%%s%%' and " % key_values[kvalue]
            else:
                sql_where += keyname + " like '%%%s%%'" % key_values[kvalue]
            i -= 1
            kvalue += 1
        if len(sql_where) > 0:
            sql_count = "select count(1) from %s where %s_model_state=1 and (%s)" % (
                table_name, table_name, sql_where)
            sql = "select * from %s where _id in (select DISTINCT _id from %s where %s_model_state=1 and (%s) limit %d,%d)" % (
                table_name, table_name, table_name, sql_where, page, page_size)
        else:
            sql_count = "select count(1) from %s where %s_model_state=1 " % (
                table_name, table_name)
            sql = "select * from %s where _id in (select DISTINCT _id from %s where %s_model_state=1 limit %d,%d）" % (
                table_name, table_name, table_name, sql_where, page, page_size)

        if SHOW_SQL:
            sql_log(sql_count, (table_name, key_names, key_values))
        count = self.cursor.execute(sql_count).fetchone()[0]

        if SHOW_SQL:
            sql_log(sql, (table_name, key_names, key_values, page, page_size))

        self.cursor.execute(sql)
        datas = []
        for row in self.cursor.fetchall():
            datas.append(self.row_tojson(self.cursor.description, row))
        return {"count": count, "data": datas, "maxpage": count/page_size+1}


if __name__ == "__main__":
    server = ApiServer()
    try:
        server.start()
    except Exception as identifier:
        log(str(identifier))
        server.stop()
