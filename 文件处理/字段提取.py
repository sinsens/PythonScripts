# -*- coding: utf-8 -*-
'''
@filename: 字段提取.py
@author: sinsen
@date: 2020.08.03
@desc: 从模板文件提取字段并生成添加字段的 sql 语句
@tested by: python 2.7.13
@usage:
    dir_name = 要遍历的目录
    reg_part = 提取字段的正则表达式
    length = 默认增加字段的长度

    cmd & bash: python 字段提取.py
'''
import re
import os

length = 100
reg_part = '\w+\$\w+'
dir_name = 'input/'

fl = os.listdir(dir_name)

class Table:
    def __init__(self, tbname, colnames = []):
        self.tbname = tbname
        self.colnames = colnames

    def addcol(self, colname):
        if colname not in self.colnames:
            self.colnames.append(colname)

    def tosql(self):
        
        #sql = 'alter table {0} add {1} nvarchar({2})\nGO\n'.format(self.tbname, str.join(' nvarchar({0}), '.format(length),self.colnames), length)
        sql = ''
        sql_fmt = 'alter table {0} add {1} nvarchar({2})\nGO\n'
        for col in self.colnames:
            sql += sql_fmt.format(self.tbname, col, length)
        return sql

class Tables:
    def __init__(self):
        self.tables = []
        self.sqls = []
        
    def addnew(self, ctl):
        tbinfo = ctl.split('$')
        self.add(tbinfo[0], tbinfo[1])
        
    def add(self, tbname, colname):
        flag = False
        for tb in self.tables:
            if tb.tbname == tbname:
                tb.addcol(colname)
                flag = True
        if flag == False:
            tb = Table(tbname, [colname])
            self.tables.append(tb)

    def output(self):
        print('tables count:{0}'.format(len(self.tables)))
        for tb in self.tables:
            sql = tb.tosql()
            self.sqls.append(sql)
        return self.sqls


ls = []
words = []
mytables = Tables()

for i in fl:
    print('reading file: {0}'.format(i))
    with open(dir_name+i) as f:
        content = f.read()
        res = re.findall(reg_part, content)
        if res:
            for word in res:
                mytables.addnew(word)
                words.append(word + '\n')

print('file count:{0}'.format(len(fl)))
# 写出所有字段
with open('result.txt', 'w') as f:
    newwords = set(words)
    f.writelines(newwords)

# 写出 sql
sqls = mytables.output()
with open('sql.txt', 'w') as f:
    newwords = set(sqls)
    f.writelines(newwords)

print('mission complate')
