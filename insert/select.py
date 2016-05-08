import MySQLdb


conn = MySQLdb.connect("davidykan.mysql.pythonanywhere-services.com", "davidykan", "qwerqwer", "davidykan$default", charset='utf8')
c = conn.cursor()
c.execute("select name_id from newapp_entry where source='youtube'")
conn.commit()
b=[]
for a in c:
    b.append(a[0])


print(b)

