import cx_Oracle
import os

class dbConnection():
    def conn(self, param):
        # os.putenv('NLS_LANG', 'UTF8')
        # print(os.environ['LD_LIBRARY_PATH'])

        conn = cx_Oracle.connect(param['conninfo'])
        cur = conn.cursor()

        sql = "select "
        sql += "inventory_item_id, segment1, 'leaf_node' as leaf, description "
        sql += "from table "
        sql += "where item_code like 'Q43250%' "

        cur.execute(sql)

        for row in cur:
            param['list'].append({'item_code': row[1], 'item_leaf': row[2], 'item_desc': row[3]})
        cur.close()
        conn = None
        # conn.close()
        return param['list']