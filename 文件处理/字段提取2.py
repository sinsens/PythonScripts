# -*- coding=utf-8 -*-
import chardet
import re
from sys import argv
'''
@author: sinsen
@date: 2020.08.16
@desc: ascx 模板文件代码清理工具
@changelog:
    2020.09.11 加了导出字段用的代码
'''
ver = '0.2'

class CodeCleaner:
    @classmethod
    def read_all_lines(cls, filename):
        try:
            lines = []
            line_states = 0
            print('读取文件：{0}'.format(filename))
            with open(filename, 'rb') as f:
                content = f.read()
                encoding = chardet.detect(content)['encoding']  # 获取编码格式
                print('文件编码：{0}'.format(encoding))
                temp_lines = content.decode(encoding)

            line_split = '\n'
            if temp_lines.find(line_split) < 0:
                line_split = '\r'
            for line in temp_lines.split(line_split):
                line_state = CodeCleaner.count_line_weight(line)
                if line_state == 0:
                    continue
                '''
                类似代码花括号 '(<{}>)' 包含关系的计算，这里是计算注释包含关系
                '''
                if type(line_state) == type(0) and line_state != 0:
                    line_states += line_state
                elif type(line_state) == type('str') and line_states == 0:
                    lines.append(line_state)
            #print('清理完成::0}'.format(filename))
            return lines
        except Exception as identifier:
            print('读取发生错误::0},:1}'.format(filename, identifier))

    '''
    类似代码花括号 '(<{}>)' 包含关系的计算，这里是计算注释包含关系
    '''
    @classmethod
    def count_line_weight(cls, line):
        if line is None or len(line) == 0:
            return 0
        temp_line = line.replace(' ', '').replace(
            '\n', '').replace('\r', '').replace('\t', '')
        if len(temp_line) == 0:
            return 0
        if temp_line.startswith('//'):
            return 0

        prefix1 = line.find('<%--')
        if prefix1 > -1:
            prefix11 = line.find('--%>')
            if prefix11 > -1:
                str_to_remove = line[prefix1: prefix11+4]
                line = line.replace(str_to_remove, '')

        prefix1 = line.find('<!--')
        if prefix1 > -1:
            prefix11 = line.find('-->')
            if prefix11 > -1:
                str_to_remove = line[prefix1: prefix11+3]
                line = line.replace(str_to_remove, '')

        prefix1 = line.find('/*')
        if prefix1 > -1:
            prefix11 = line.find('*/')
            if prefix11 > -1:
                str_to_remove = line[prefix1: prefix11+2]
                line = line.replace(str_to_remove, '')

        if line.startswith('<%--'):
            return 2
        if line.endswith('--%>'):
            return -2
        if line.startswith('/*'):
            return 3
        if line.endswith('*/'):
            return -3
        return line

    @classmethod
    def clean(cls, filename, newfilename=None):
        from os import path
        from os import walk
        from os import makedirs
        if path.exists(filename) == False:
            print('文件（夹）不存在或无不可访问：{0}'.format(filename))
            exit(0)
        ''' 文件处理 '''
        if path.isfile(filename):
            newfilename = newfilename or filename + '.output.txt'
            lines = CodeCleaner.read_all_lines(filename)
            with open(newfilename, 'w', encoding='utf8') as f:
                print('写出文件：{0}'.format(newfilename))
                f.writelines(lines)
                print('----------------------------------------')

        else:
            ''' 文件夹处理 '''
            output_dir = newfilename or path.dirname(filename) + './output/'
            
            if path.exists(output_dir) == False:
                try:
                    makedirs(output_dir)
                except Exception as identifier:
                    print('创建文件夹发生错误::0},:1}'.format(
                        output_dir, identifier))
                    exit(1)
            dir_info = list(walk(filename))[0]
            for f in dir_info[2]:
                filename = dir_info[0] + '/' + f
                if path.isfile(filename):
                    output_filename = output_dir + path.basename(f)
                    lines = CodeCleaner.read_all_lines(filename)
                    with open(output_filename, 'w', encoding='utf8') as f:
                        print('写出文件：{0}'.format(output_filename))
                        f.writelines(lines)
                        print('----------------------------------------')



class ElementData:
    def __init__(self):
        self.RowIndex = 0
        self.TableName = ""
        self.ColumnName = ""
        self.ColumnValue = ""
        self.ControlName = ""
        self.DataNeedRead = False
        self.DataNeedGet = False
        self.DataNeedSave = False

class ElementAgent:
    
    def __init__(self):
        self.elemList = []


    def Add(self, elemName, elemValue, aIndex = 0):
        array = elemName.split('#')
        text = ""
        if (len(array) > 1):
            text = array[1]
        
        array2 = array[0].split('$')
        elementData = ElementData()
        elementData.ControlName = elemName
        elementData.RowIndex = aIndex
        elementData.ColumnName = self.GetColumnName(elemName)
        elementData.ColumnValue = elemValue
        num = len(array2)
        if (num == 2):
            elementData.TableName = array2[0]
        
        elementData.DataNeedGet = text.find("$G") > -1
        elementData.DataNeedRead = text.find("$R") > -1
        elementData.DataNeedSave = text.find("$S") > -1
        self.elemList.append(elementData)
    
    def Get(self, elemName, elemValue, aIndex = 0):
        array = elemName.split('#')
        text = ""
        if (len(array) > 1):
            text = array[1].upper()
        
        array2 = array[0].split('$')
        elementData = ElementAgent()
        elementData.ControlName = elemName
        elementData.RowIndex = aIndex
        elementData.ColumnName = self.GetColumnName(elemName)
        elementData.ColumnValue = elemValue
        num = len(array2)
        if (num == 2):
            elementData.TableName = array2[0]
        
        elementData.DataNeedGet = text.find("$G") > -1
        elementData.DataNeedRead = text.find("$R") > -1
        elementData.DataNeedSave = text.find("$S") > -1
        return elementData
    
    def GetColumnName(self, aName):
        array = aName.split('#')[0].split('$')
        if (len(array) > 1):
            aName = array[1]
        
        if (aName.index("") > -1):
            aName = aName.split('⊙')[0]
        
        return aName

class FormControl:
    def __init__(self, paras):
        self.eIndex = 0
        self.IsGet = False
        if(len(paras)>0):
            self.ControlName = paras[0] or ''
        if(len(paras)>1):
            self.showTitle = paras[1] or ''
        if(len(paras)>2):
            self.showVal = paras[2] or '&nbsp;'
        if(len(paras)>3):
            self.ctrlType = paras[3] or 'inputText'
        if(len(paras)>4):
            self.ctrlPara = paras[4] or ''
        if(len(paras)>5):
            self.showTips = paras[5] or ''
        if(len(paras)>6):
            self.Verify = paras[6] or ''
        self.columnValue = self.showVal

class CForm:
    def __init__(self):
        self.eleAgent = ElementAgent()
        self.cols = []

    def Add(self, paras):
        num = 0
        formControl = FormControl(paras)
        for el in self.eleAgent.elemList:
            if (el.ControlName == formControl.ControlName):
                num +=1
        formControl.eIndex = num
        self.eleAgent.Add(formControl.ControlName, formControl.columnValue, formControl.eIndex)
        self.cols.append(formControl)
    
    def Cols(self):
        tb = {}
        for col in self.cols:
            el = self.eleAgent.Get(col.ControlName, '')
            tbname = el.TableName
            colname = el.ColumnName
            if(len(tbname) > 0 and len(colname)>0):
                if tb.keys().__contains__(tbname):
                    tbinfo = tb[tbname]
                else:
                    tbinfo = {}
                    tb[tbname] = tbinfo
                if tbinfo.keys().__contains__(colname):
                    continue
                else:
                    tbinfo[colname] = col.showTitle.replace(' ','')
        print(tb)
        return tb
class CtlExport:
    reCFormSetter = re.compile(r'cForm.Add\(\"(.*?)\"\)|cform.Add\(\"(.*?)\"\)|cfa.Add\((.*?);')
    reParam =  re.compile('\"(.*?)\"')      

    @classmethod
    def getCols(cls, lines):
        cform = CForm()
        for line in lines:
            cfsetter = cls.reCFormSetter.search(line)
            if(cfsetter):
                params = []
                for p in cfsetter.groups():
                    if(p):
                        pvs = p.split(",")
                        for ps in pvs:
                            params.append(ps.replace('"',''))
                cform.Add(params)
        
        # 转成文本行
        '''
        tbname,
        中文描述,字段名称
        '''
        tbs = cform.Cols()
        lines = []
        for tb in tbs.keys():
            lines.append('表名称,{0}\n'.format(tb))
            tbinfo = tbs[tb]
            for c in tbinfo.keys():
                lines.append('{0},{1}\n'.format(tbinfo[c], c))
            lines.append('\n')
        return lines

    @classmethod
    def export(cls, filename, newfilename=None):
        from os import path
        from os import walk
        from os import makedirs
        if path.exists(filename) == False:
            print('文件（夹）不存在或无不可访问：{0}'.format(filename))
            exit(0)
        ''' 文件处理 '''
        if path.isfile(filename):
            newfilename = newfilename or filename + '.output.txt'
            lines = CodeCleaner.read_all_lines(filename)
            out_lines = cls.getCols(lines)
            with open(newfilename, 'w', encoding='utf8') as f:
                print('写出文件：{0}'.format(newfilename))
                f.writelines(out_lines)
                print('----------------------------------------')

        else:
            ''' 文件夹处理 '''
            print('文件夹：{0}'.format(filename))
            output_dir = newfilename or path.dirname(filename) + './output/'

            if path.exists(output_dir) == False:
                try:
                    makedirs(output_dir)
                except Exception as identifier:
                    print('创建文件夹发生错误:{0},{1}'.format(
                        output_dir, identifier))
                    exit(1)
            dir_info = list(walk(filename))[0]
            
            for f in dir_info[2]:
                filename = dir_info[0] + '/' + f
                print(filename)
                if path.isfile(filename):
                    print('读取文件{0}'.format(filename))
                    output_filename = output_dir + path.basename(f) + '.output.txt'
                    lines = CodeCleaner.read_all_lines(filename)
                    out_lines = cls.getCols(lines)
                    with open(output_filename, 'w', encoding='utf8') as f:
                        print('写出文件：{0}'.format(output_filename))
                        f.writelines(out_lines)
                        print('----------------------------------------')


'''
# 测试
CtlExport.export('Temp_NdbgMf2019_Zichan.ascx')
exit(0)
'''

if __name__ == '__main__':
    print('=====================================')
    print('代码清理(字段导出)工具 ver:{0}'.format(ver))
    if len(argv) < 2:
        print(
            '''
        用法：
            python codcleaner.py [clean|export] 文件名（夹） [输出文件名（夹）]
                
        示例：
            python codcleaner.py [clean|export] f:temp/temp_NdbgSt2019_Zichan.ascx
        ''')
        exit(0)
    
    if (argv[1] == 'clean'):
        if len(argv) == 3:
            CodeCleaner.clean(argv[2])
        else :
            CodeCleaner.clean(argv[2], argv[3])
    elif (argv[1] == 'export'):
        if len(argv) == 3:
            CtlExport.export(argv[2])
        else :
            CtlExport.export(argv[2], argv[3])