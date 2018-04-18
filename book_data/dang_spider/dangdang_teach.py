import requests,re
from data_from_dang import py_and_sql



'''
教育,人文,励志,科技
'''

class data_dang(object):
    def __init__(self,id=0,gtitle='',gpic='',gprice='',gunit='',gclick='',gintro='',gcontent='',ginventory=0,gtypeinfo_id=0,isdelete=0):
        self.id=id
        self.gtitle=gtitle
        self.gpic=gpic
        self.gprice=gprice
        self.gunit=gunit
        self.gclick=gclick
        self.gintro=gintro
        self.gcontent=gcontent
        self.ginventory=ginventory
        self.isdelete=isdelete
        self.gtypeinfo_id=gtypeinfo_id
    def hasNumbers(self,inputString):
        #是否含有数字
        return any(char.isdigit() for char in inputString)

    def get_id(self):
        retid = py_and_sql.select_id()
        yang_id = retid[len(retid) - 1][0]
        return yang_id
    def dispose_parenthesis(self,s2):
        #处理小括号(全角)
        a=0
        b=0
        for item in range(len(s2)):
            if s2[item] == '（':
                a=item
            if s2[item] == '）':
                b=item
                break
        s=s2[a+1:b]
        if self.hasNumbers(s)==False:
            s=''
        return s

    def dangdang(self):
        s=requests.session()
        header = {
            # "Referer": "http://book.dangdang.com/children",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Mobile Safari/537.36"
        }
        teach_list=[
            {'type_id':2,'type_pgs':['43','47','49','50']},
            {'type_id':3,'type_pgs':['28','32','34','36']},
            {'type_id':4,'type_pgs':['21']},
            {'type_id':5,'type_pgs':['62','54','56','52']}
                    ]
        self.id = self.get_id()
        self.ginventory = 500
        for item in teach_list:
            self.gtypeinfo_id=item['type_id']
            for demo in item['type_pgs']:
                print(demo)
                for pg in range(1,10):
                    url='http://category.dangdang.com/pg{}-cp01.{}.00.00.00.00.html'.format(pg,demo)
                    ret=s.get(url=url,headers=header)
                    info=ret.content.decode('gbk').replace('\n','').replace('\r','').replace('\t','').replace(' ','')
                    # print(info)
                    info_list=re.findall('<liddt-pit(.*?)atitle="(.*?)"(.*?)imgdata-original=\'(.*?)\'(.*?)atitle="(.*?)"(.*?)detail">(.*?)</p>(.*?)yen;(.*?)</span>(.*?)click_review_count(.*?)>(.*?)条评论</a>',info)
                    if len(info_list)>0:
                        for item in info_list:
                            self.id +=1
                            self.gtitle = item[1]
                            if len(self.gtitle) < 1:
                                continue
                            if len(self.gtitle) > 100:
                                continue
                            self.gpic = item[3]
                            self.gprice = item[9]
                            self.gunit = '1册'
                            self.gclick = item[12]
                            self.gintro = item[1]
                            self.gcontent = item[5]
                            self.ginventory +=1
                            self.isdelete = 0

                            print('开始爬取:')
                            print('ID:', self.id)
                            print('书名:', self.gtitle)
                            print('图片:', self.gpic)
                            print('价格:', self.gprice)
                            print('单位:', self.gunit)
                            print('简介:', self.gintro)
                            print('内容:', self.gcontent)
                            print('点击量:', self.gclick)
                            print('图书种类',self.gtypeinfo_id)
                            py_and_sql.insert_dang(self.id, self.gtitle, self.gpic, self.gprice, self.gunit, self.gclick,self.gintro, self.gcontent, self.ginventory, self.isdelete,self.gtypeinfo_id)

data=data_dang()
data.dangdang()