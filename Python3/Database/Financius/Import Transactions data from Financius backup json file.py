# 从Financius的json备份中导入数据到mysql
# import financius transactions from json
# sinsen at 2018-08-29
import json
import time
import datetime
import pymysql


db = {
	'host' : 'localhost',
	'user' : 'root',
	'password': 'root',
	'database': 'financius'
}

t1 = time.time()

con = pymysql.connect(**db)

try:
	with con.cursor() as cursor:
		# Read a single record
		sql = "SELECT database()"
		cursor.execute(sql)
		result = cursor.fetchone()
		print("Use database:", result)
finally:
	con.close()

# read data from file
with open('transactions.json') as f:
	data = json.load(f)
if data == None:
	exit("Data was none")

i = 0
try:
	con = pymysql.connect(**db)
	with con.cursor() as cursor:
		# 导入 transactions
		for item in data['transactions']:
			type(item['model_state'])
			sql = '''INSERT INTO transactions (transactions_id, transactions_model_state, transactions_sync_state, transactions_account_from_id, transactions_account_to_id, transactions_category_id, transactions_date, transactions_amount, transactions_exchange_rate, transactions_note, transactions_state, transactions_type, transactions_include_in_reports) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
			'''
			id = item['id']
			model_state = int(item['model_state'])
			sync_state = int(item['sync_state'])
			account_from_id = item['account_from_id']
			account_to_id = item['account_to_id']
			category_id = item['category_id']
			date = datetime.datetime.utcfromtimestamp(item['date']/1000)
			#date = (item['date'])
			amount = item['amount']
			exchange_rate = float(item['exchange_rate'])
			note = item['note']
			transaction_state = int(item['transaction_state'])
			transaction_type = int(item['transaction_type'])
			include_in_reports = int(item['include_in_reports'])
			#print (sql % (id, model_state, sync_state,account_from_id, account_to_id, category_id, date, amount,exchange_rate, note, transaction_state, transaction_type, include_in_reports))
			
			cursor.execute(sql,(id, model_state, sync_state,account_from_id, account_to_id, category_id, date, amount,exchange_rate, note, transaction_state, transaction_type, include_in_reports))
			# 插入标签
			for tag in item['tag_ids']:
				cursor.execute(''' insert into transaction_tags(transaction_tags_transaction_id, transaction_tags_tag_id) values(%s, %s) ''', (item['id'], tag))
			i += 1
		
		con.commit()
finally:
	con.close()
	t2 = time.time()
	print('插入数据完成\n共插入', i , '条数据，耗时', t2 - t1)

