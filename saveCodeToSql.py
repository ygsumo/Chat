import pymysql
import activeCode




conn = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='root',
    db='code'
)

cur = conn.cursor()

code_list = activeCode.gene_activation_code(5, 16)
code = code_list.keys()
print code;

for item in code:
    sql = 'INSERT INTO code(code) VALUES (\'%s\');' % item
    cur.execute(sql)

conn.commit()
cur.close()
conn.close()
