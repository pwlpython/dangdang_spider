import requests,re
from data_from_dang import py_and_sql

'''
网络
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
    def get_id(self):
        retid = py_and_sql.select_id()
        yang_id = retid[len(retid) - 1][0]
        return yang_id

    def dangdang(self):
        s=requests.session()
        header={
            "Referer": "http://e.dangdang.com/new_original_index_page.html",
            "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Mobile Safari/537.36"
        }
        url='http://e.dangdang.com/new_original_index_page.html'
        ret = s.get(url=url, headers=header)
        info = ret.content.decode('utf-8').replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
        # print(info)
        info_list1=re.findall('<divclass="bookinfo"(.*?)href="(.*?)"title="(.*?)">(.*?)des">(.*?)</div>',info)
        self.id = self.get_id()
        self.gtypeinfo_id=6
        if len(info_list1)>0:
            for item in info_list1:
                self.gunit = '1千字'
                self.gtitle = item[2]
                if self.gtitle=='嫡女重生：溺宠残王妃':
                    continue
                if len(self.gtitle) < 1:
                    continue
                if len(self.gtitle) > 100:
                    continue
                href = item[1]
                self.gintro=item[2]
                self.gprice = '5铃铛'
                if len(self.dispose_parenthesis(self.gtitle)) > 1:
                    self.gunit = self.dispose_parenthesis(self.gtitle)
                print('开始爬取:')
                print('ID:', self.id)
                print('书名:', self.gtitle)
                print('简介:', self.gintro)
                print('价格:', self.gprice)
                print('单位:', self.gunit)

                self._detail(href)
                self.id += 1
                py_and_sql.insert_dang(self.id, self.gtitle, self.gpic, self.gprice, self.gunit, self.gclick,self.gintro, self.gcontent, self.ginventory, self.isdelete, self.gtypeinfo_id)

        info_list2=re.findall('<divclass="info"(.*?)href="(.*?)"title="(.*?)">(.*?)orange">(.*?)</span>',info)
        if len(info_list2)>0:
            for item in info_list1:
                self.gunit = '1千字'
                self.id += 1
                self.gtitle = item[2]
                if len(self.gtitle) < 1:
                    continue
                if len(self.gtitle) > 100:
                    continue
                href = item[1]
                self.gintro=item[2]
                self.gprice = '5铃铛'
                if len(self.dispose_parenthesis(self.gtitle)) > 1:
                    self.gunit = self.dispose_parenthesis(self.gtitle)
                print('开始爬取:')
                print('ID:', self.id)
                print('书名:', self.gtitle)
                print('简介:', self.gintro)
                print('价格:', self.gprice)
                print('单位:', self.gunit)

                self._detail(href)

                py_and_sql.insert_dang(self.id, self.gtitle, self.gpic, self.gprice, self.gunit, self.gclick,self.gintro, self.gcontent, self.ginventory, self.isdelete, self.gtypeinfo_id)
    def _detail(self,href):
        s = requests.session()
        header = {
            "Referer": "http://e.dangdang.com/{}".format(href.replace('./','')),
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Mobile Safari/537.36"
        }
        try:
            url='http://e.dangdang.com/'+href.replace('./','')
            ret2 = s.get(url=url,headers=header)
            info2 = ret2.content.decode('utf-8').replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
            # print(info2)
            info2_list=re.findall('<divid="content">(.*?)imgsrc="(.*?)">(.*?)clickRateNum">(.*?)</span>(.*?)字数：(.*?)万(.*?)desc"title="(.*?)">',info2)
            if len(info2_list)>0:
                for item in info2_list:
                    self.ginventory=str(float(item[5])*10000)+'字'
                    self.gpic=item[1]
                    self.gcontent=item[7]
                    self.gclick=item[3]
                    print('点击量:',self.gclick)
                    print('图片路径:',self.gpic)
                    print('库存:',self.ginventory)
                    print('内容:',self.gcontent)
        except Exception as e:
            print(e)

data=data_dang()
data.dangdang()