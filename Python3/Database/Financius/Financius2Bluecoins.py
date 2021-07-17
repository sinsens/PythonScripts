#-*-coding:utf8;-*-
#file:Financius2Bluecoins.py
#author:Sinsen
#desc:Financius Json 数据转为 Bluecoins App数据
#script ver:0.1
#bluecoins ver:208.27.02
#date:2019.08.10

import json
import time
import sqlite3
from os import path

SHOW_SQL = True # Set this value equals True for show SQL has executed.
output_dir = path.realpath('./data/out/')
financius_backup_filename = path.realpath('data/financius.json')
bluecoins_backup_filename = path.realpath('data/bluecoins.fydb')

def log(msg):
    print(time.strftime("%Y-%m-%d %H:%M:%S"), msg)
def sql_log(sql, params=[]):
    if SHOW_SQL: print(time.strftime("%Y-%m-%d %H:%M:%S"), sql, 'params:', params)

class Converter():

    def __init__(self):
        self.jdata = {}
        self.coins_data = {}

        self.init_json_data()
        self.init_blueconins_data()

    def init_json_data(self):
        try:
            log('Initiating json data...')
            log('Working directory is:'+path.realpath("./"))

            if path.exists(financius_backup_filename) == False:
                log('Could not found Financius json backup file:'+financius_backup_filename)
                exit(0)
            if path.exists(bluecoins_backup_filename) == False:
                log('Could not found Bluecoins backup file:'+bluecoins_backup_filename)
                exit(0)
            
            with open(financius_backup_filename, encoding='utf8') as f:
                self.jdata = json.loads(f.read())

                log('Initialization json data done')
                print('========Json data preview========')
                print('tags count:', len(self.jdata['tags']))
                print('accounts count:', len(self.jdata['accounts']))
                print('categories count:', len(self.jdata['categories']))
                print('transactions count:', len(self.jdata['transactions']))
            
        except Exception as e:
            log('Something wrong:'+str(e))
            if self.cursor is not None:self.cursor.close()
    
    def get_alldata(self, table_name):
        try:
            if self.cursor is sqlite3.Cursor and len(table_name) >= 1:
                sql = 'select * from %s'.format(table_name)
                sql_log(sql)
                return self.cursor.execute(sql).fetchall()
            return None
        except Exception as e:
            log('Something wrong:'+str(e))
    
    def get_blueconis_key(self, table_name, keyname, colname, search_value):
        try:
            if self.coins_data[table_name] is None: return -1
            for i in self.coins_data[table_name]:
                if(i[colname] == search_value):
                    return i[keyname]
            return -1
        except Exception as e:
            log('Something wrong:'+str(e))
    
    def get_account_title_from_json(self, account_id):
        try:
            if self.jdata['accounts'] is None: return None
            for i in self.jdata['accounts']:
                if(i['id'] == account_id):
                    return i['title']
            return None
        except Exception as e:
            log('Something wrong:'+str(e))

    def get_tag_title_from_json(self, tag_id):
        try:
            for i in self.jdata['tags']:
                if(i['id'] == tag_id):
                    return i['title']
            return None
        except Exception as e:
            log('Something wrong:'+str(e))
    
    def get_title_from_json(self, obj_name, obj_id):
        try:
            for i in self.jdata[obj_name]:
                if(i['id'] == obj_id):
                    return i['title']
            return None
        except Exception as e:
            log('Something wrong:'+str(e)) 

    def insertone(self, sql, params):
        if self.cursor is not None:
            try:
                sql_log(sql, params)
                self.cursor.execute(sql, params)
                self.db.commit()
                return self.cursor.lastrowid
            except Exception as e:
                log('Something wrong:'+str(e))
                return -1
        else:
            return -1
    
    def init_blueconins_data(self):
        try:
            # open Bluecoins backup file as sqlite3 database file
            self.db = sqlite3.connect(bluecoins_backup_filename)
            self.cursor = self.db.cursor()
            # accounts
            self.coins_data['ACCOUNTTYPETABLE'] = self.get_alldata('ACCOUNTTYPETABLE')
            self.coins_data['ACCOUNTSTABLE'] = self.get_alldata('ACCOUNTSTABLE')
            self.coins_data['ACCOUNTINGGROUPTABLE'] = self.get_alldata('ACCOUNTINGGROUPTABLE')
            # categories
            self.coins_data['CATEGORYGROUPTABLE'] = self.get_alldata('CATEGORYGROUPTABLE')
            self.coins_data['CHILDCATEGORYTABLE'] = self.get_alldata('CHILDCATEGORYTABLE')
            # tags
            self.coins_data['LABELSTABLE'] = self.get_alldata('LABELSTABLE')
            # transactions
            self.coins_data['TRANSACTIONTYPETABLE'] = self.get_alldata('TRANSACTIONTYPETABLE')
            self.coins_data['TRANSACTIONSTABLE'] = self.get_alldata('TRANSACTIONSTABLE')

        except sqlite3.DatabaseError as e:
            log('Something wrong:'+str(e))
            if self.cursor is not None:self.db.close()
    
    def sync_accounts(self):
        for i in self.jdata['accounts']:
            keyid = self.get_blueconis_key('ACCOUNTSTABLE', 'accountsTableID', 'accountName', (i['title']))
            if keyid == -1:
                keyid = self.insertone('insert into ACCOUNTSTABLE(accountName) values(?)', (i['title']))
            if keyid == -1:
                log('Error: could not be able to sync account on title:'+i['title'])
                exit(1)

    def sync_categories(self):
        for i in self.jdata['categories']:
            keyid = self.get_blueconis_key('CHILDCATEGORYTABLE', 'categoryTableID', 'childCategoryName', i['title'])
            if keyid == -1:
                keyid = self.insertone('insert into CHILDCATEGORYTABLE(childCategoryName,parentCategoryID) values(?,0)', (i['title']))
            if keyid == -1:
                log('Error: could not be able to sync category on title:'+i['title'])
                exit(1)
    
    def sync_transactions(self):
        for i in self.jdata['transactions']:
            # accounts
            from_account_title = self.get_account_title_from_json(i['account_from_id'])
            to_account_title = self.get_account_title_from_json(i['account_from_id'])
            from_account_id = self.get_blueconis_key('ACCOUNTSTABLE', 'accountsTableID', 'accountName', from_account_title)
            to_account_id = self.get_blueconis_key('ACCOUNTSTABLE', 'accountsTableID', 'accountName', to_account_title)
            # tags
            tags = []
            for tag in i['tag_ids']:
                tags.append(self.get_tag_title_from_json(tag))
            # categories
            cate_tilte = self.get_title_from_json('categories', i['category_id'])
            cate_id = self.get_blueconis_key('CHILDCATEGORYTABLE', 'categoryTableID', 'childCategoryName', cate_tilte)
            # itemID,transactionTypeID
            transactionTypeID = 3
            itemID = 0
            if i['transaction_type'] == 1:
                itemID = 2
                transactionTypeID = 3
            elif i['transaction_type'] == 2:
                itemID = 3
                transactionTypeID = 4
            elif i['transaction_type'] == 3:
                itemID = 1
                transactionTypeID = 5
            # amount
            amount = i['amount'] * 1000

            # insert transaction
            sql = '''insert into TRANSACTIONSTABLE(itemID, amount, notes, accountID, transactionCurrency,
                     conversionRateNew, transactionTypeID, categoryID, accountReference, accountPairID,
                      uidPairID, deletedTransaction, hasPhoto, labelCount, date) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
            sql_log(sql, (itemID, amount, i['note'], from_account_id, 'CNY', 1, transactionTypeID, cate_id,
                3, to_account_id, -1, 6, 0, len(tags), i['date']))
            self.cursor.execute(sql, (itemID, amount, i['note'], from_account_id, 'CNY', 1, transactionTypeID, cate_id,
                3, to_account_id, -1, 6, 0, len(tags), i['date']))
            
            transaction_id = self.cursor.lastrowid
            # insert tags
            for tag in tags:
                sql =  'insert into LABELSTABLE(labelName,transactionIDLabels) values(?)'
                sql_log(sql, (tag, transaction_id))
            # commit transaction
            self.db.commit()
            log('update transaction id:%s done'%i['id'])
    
    def sync_all(self):
        self.sync_accounts()
        self.sync_categories()
        self.sync_transactions()
        pass

    def update_accounts(self):
        for tag in self.self.jdata['accounts']:
            self.cursor.execute('INSERT into ACCOUNTSTABLE(accountName,accountCurrency,accountHidden) Values("%s","%s",%d,)'%(tag['title'],'CNY', 1, tag['transaction_type']))

converter = Converter()
converter.sync_all()