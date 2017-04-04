import psycopg2
import os

gLogFloag = "Y"
gUserId = "-1"
gUrl = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")
gConpg = "dbname='tensormsa' user='tfmsauser' host='localhost' password='1234'"

def println(printStr):
    if gLogFloag == "Y":
        conn = psycopg2.connect(gConpg)
        cur = conn.cursor()
        if printStr == "S" or printStr == "s":
            sql = "delete from common_log_info where created_by = '"+gUserId+"'"
            cur.execute(sql)
            conn.commit()
        elif printStr == "E" or printStr == "e":
            sql = "select * from common_log_info where created_by = '"+gUserId+"' order by log_id"
            cur.execute(sql)
            rows = cur.fetchall()

            print("Trace.............................................................................")
            for i in range(0, len(rows)):
                for j in range(0, len(rows[i])):
                    if rows[i][j] is not None and cur.description[j][0] not in (
                    "id", "log_id", "creation_date", "last_update_date", "created_by", "last_updated_by"):
                        print(rows[i][j])
            print("..................................................................................")
        else:
            print(printStr)
            cur.execute("select COALESCE(max(log_id)::int,0)+10 seq from common_log_info where created_by = '"+gUserId+"'")
            rows = cur.fetchall()

            sql = "INSERT INTO common_log_info( "
            valueStr = ""

            # 일반적인 String 형태일 경우 출력을 해준다.
            try:
                valS = printStr.split("+")

                cnt = 1
                for i in valS:
                    if cnt != 1 and cnt < 31:
                        sql += ","
                        valueStr += ","
                    if cnt < 31:
                        sql += str("attr") + str(cnt)
                        valueStr += "'" + str(i) + "'"
                    cnt += 1

                sql += ",creation_date,last_update_date, created_by, last_updated_by,log_id) "
                sql += "VALUES (" + valueStr + ",now(),now(),'"+gUserId+"','"+gUserId+"','" + str(rows[0][0]) + "')"

                cur.execute(sql)
                conn.commit()
            except Exception as e:
                # 객체 형태일 경우 출력을 해준다.
                sql += "attr1,creation_date,last_update_date, created_by, last_updated_by,log_id) "
                sql += "VALUES ('" + str(printStr).replace("'","")+"',now(),now(),'" + gUserId + "','" + gUserId + "','" + str(rows[0][0]) + "')"
                cur.execute(sql)
                conn.commit()
        # 연결을 종료한다
        cur.close()
        conn.close()

def get_combine_label_list(origin_list, compare_list):

    """ 리스트 두개를 비교하여 차이나는 값만 마지막에 순서대로 넣는 함수
        The function that compare two list and insert distingush values

    Args:
      params:
        * origin_list : A original list
        * compare_list: An compare lists

    Returns:
      list
      두 리스트를 비교하여 구별된 값을 새 원래 리스트에 추가하여 반환
    Raises:
    Example
        origin_list = ['A','B','C','D']
        compare_list = ['50>=', '50=','C','D','E']
        result => ['A', 'B', 'C', 'D', '50=', '50>=', 'E']
    """

    _origin_list = list(origin_list)
    _compare_list = list(compare_list)

    _union_values = set(_origin_list).union(set(_compare_list))
    _diff_values = sorted(list(_union_values - set(_origin_list)))
    _origin_list.extend(_diff_values)

    return _origin_list