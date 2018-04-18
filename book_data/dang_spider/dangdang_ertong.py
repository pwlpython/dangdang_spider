import requests,re
from data_from_dang import py_and_sql


'''
儿童
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

    def dangdang(self):
        s=requests.session()
        header={
            "Referer": "http://book.dangdang.com/children",
            "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Mobile Safari/537.36"
        }
        url='http://book.dangdang.com/children'
        ret=s.get(url=url,headers=header)
        info=ret.content.decode('gbk').replace('\n','').replace('\r','').replace('\t','').replace(' ','')
        # print(info)
        info_list=re.findall('<liclass="line(.*?)atitle="(.*?)"class="img"href="(.*?)"target="_blank"><imgsrc=\'(.*?)\'alt(.*?)atitle(.*?)href=(.*?)num">(.*?)</span><spanclass="tail">(.*?)</span>',info)
        if len(info_list)>0:
            self.id=0
            self.gtypeinfo_id=0
            self.isdelete=0
            self.ginventory=500
            self.gclick=0
            self.gintro=''
            self.gcontent=''
            for item in info_list:
                # global data_list
                # data_list=[]
                self.gunit = '1册'
                self.ginventory+=1
                self.id+=1
                self.gtitle=item[1]
                if len(self.gtitle)<1:
                    continue
                if len(self.gtitle)>100:
                    continue
                href=item[2]
                self.gpic=item[3]
                with open('/home/blm/Desktop/pic/儿童{}.jpg'.format(self.id),'a') as f:
                    f.write(self.gpic)
                self.gprice=item[7]+item[8]
                self.gtypeinfo_id=1
                if len(self.dispose_parenthesis(self.gtitle))>1:
                    self.gunit=self.dispose_parenthesis(self.gtitle)
                print('开始爬取:')
                print('ID:',self.id)
                print('书名:',self.gtitle)
                print('图片:',self.gpic)
                print('价格:',self.gprice)
                print('单位:',self.gunit)
                self._detail(href)
                # py_and_sql.insert_dang(self.id,self.gtitle,self.gpic,self.gprice,self.gunit,self.gclick,self.gintro,self.gcontent,self.ginventory,self.isdelete,self.gtypeinfo_id)

    def _detail(self,url):
        s = requests.session()
        ret2 = s.get(url)
        info2 = ret2.content.decode('gbk').replace('\n', '').replace('\t', '').replace('\r', '').replace(' ','')
        # print(info2)
        info2_list=re.findall('<h1title="(.*?)">(.*?)head_title_name"title="(.*?)">(.*?)comm_num_down"dd_name="评论数">(.*?)</a>',info2)
        if len(info2_list)>0:
            for demo in info2_list:
                self.gintro=demo[0]
                self.gcontent=demo[2].replace('&nbsp;',' ')
                self.gclick=demo[4]
                # print(gcontent)
                # data_list.append(self.gintro)
                # data_list.append(self.gclick)
                # data_list.append(self.gcontent)

                print('简介:',self.gintro)
                print('内容:',self.gcontent)
                print('点击量:',self.gclick)

data=data_dang()
data.dangdang()