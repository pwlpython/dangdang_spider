import pymysql

db=pymysql.connect(host='localhost',user='root',passwd='root',db='pythontest',port=3306,charset='utf8',use_unicode=True)
cur=db.cursor()

#查询所有
def select_dang():
    sql='select * from dangdang'

    try:
        cur.execute(sql)
        result=cur.fetchall()
        for i in result:
            id=i[0]
            gtitle=i[1]
            gpic=i[2]
            gprice=i[3]
            gunit=i[4]
            gclick=i[5]
            ginventory=i[8]
            gtypeinfo_id=i[10]
            print('id=%s,gtitle=%s,gpic=%s,gprice=%s,gunit=%s,gclick=%s,ginventory=%s,gtypeinfo_id=%s'%(id,gtitle,gpic,gprice,gunit,gclick,ginventory,gtypeinfo_id))
    except Exception as e:
        raise e
#查询id值
def select_id():
    sql='select id from dangdang'
    try:
        cur.execute(sql)
        result=cur.fetchall()

    except Exception as e:
        print(e)
    finally:
        return result
#插入
def insert_dang(id,gtitle,gpic,gprice,gunit,gclick,gintro,gcontent,ginventory,isdelete,gtypeinfo_id):

    sql_insert="INSERT INTO dangdang(id,gtitle,gpic,gprice,gunit,gclick,gintro,gcontent,ginventory,isdelete,gtypeinfo_id) VALUES ({},'{}','{}','{}','{}','{}','{}','{}',{},'{}',{})".format(id,gtitle,gpic,gprice,gunit,gclick,gintro,gcontent,ginventory,isdelete,gtypeinfo_id)
    try:
        cur.execute(sql_insert)
        db.commit()
    except:
        db.rollback()