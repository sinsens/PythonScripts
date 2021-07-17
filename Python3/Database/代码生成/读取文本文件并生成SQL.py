# -*- coding: utf-8 -*-
'''
读取文本文件并生成 sql
python 版本:3.9.1
'''

# 表名
tablename = 'T_Table'
# 源数据文件名
inputFileName = 'filename.txt'

# 分列标识，一般为 tab 符(\t)
col_split_by = '\t'
# 指定每个输出文件最多多少行 SQL 语句，超过会自动生成新文件
max_sql_row_per_file = 10000

def get_key(index):
    return 'AutoKey{0:05d}'.format(index) # 主键

def get_insert_sql(dct, tbname):
    sql = 'insert into {0} ({1})'.format(tbname, ','.join(i for i in dct)) + ' values (\'' + '\',\''.join(dct[i] for i in dct) + '\')'
    return sql

def get_update_sql(tbname, dctkey, dct):
    sql = 'update {0} set {1} where {2}'.format(tbname, ','.join(i + '=\'' + dct[i] + '\'' for i in dct), ' and '.join(i + '=\'' + dctkey[i] + '\'' for i in dctkey))
    return sql

# 字段名，为第一行的数据
dct = []
index = 0
dctlen = 0
fIndex = 0

# 输出文件名
fd = open('out{0}.txt'.format(fIndex), 'w')
with open(inputFileName, 'r') as f:
    print('读取文件： {0}'.format(inputFileName))
    lines = f.readlines()
    for line in lines:
        line = line.replace('\n','').replace('\r','')
        line = line.split(col_split_by)
        if index == 0:
            for c in line:
                dct.append(c)
            dctlen = len(dct)
            print(dct)
            index += 1
            continue

        index += 1
        if(len(line) != len(dct)):
            continue
        
        dataItem = {}
        for i in range(0,dctlen):
            dataItem[dct[i]] = line[i]

        # 附加字段
        dataItem['CreateTime'] = '2021-04-21 10:50'

        sql = get_insert_sql(dataItem, tablename)
        fd.write(sql + '\r\n')

        if (index % max_sql_row_per_file == 0):
            fd.close()
            fIndex += 1
            fd = open('out{0}.txt'.format(fIndex), 'w')

fd.close()