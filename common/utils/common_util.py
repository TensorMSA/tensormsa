import psycopg2
import os
import shutil, errno
import logging
import math
from common.utils import *
import datetime
import operator
import logging

gLogFloag = "Y"
gUserId = "-1"
# gUrl = "{0}:{1}".format(os.environ['HOSTNAME'], "8000")
gConpg = "dbname='tensormsa' user='tfmsauser' host='localhost' password='1234'"


def println(printStr):
    if gLogFloag == "Y":
        conn = psycopg2.connect(gConpg)
        cur = conn.cursor()
        if printStr == "S" or printStr == "s":
            sql = "delete from common_log_info where created_by = '" + gUserId + "'"
            cur.execute(sql)
            conn.commit()
        elif printStr == "E" or printStr == "e":
            sql = "select * from common_log_info where created_by = '" + gUserId + "' order by log_id"
            cur.execute(sql)
            rows = cur.fetchall()

            logging.debug("Trace.............................................................................")
            for i in range(0, len(rows)):
                for j in range(0, len(rows[i])):
                    if rows[i][j] is not None and cur.description[j][0] not in (
                            "id", "log_id", "creation_date", "last_update_date", "created_by", "last_updated_by"):
                        print(rows[i][j])
            logging.debug("..................................................................................")
        else:
            logging.debug(printStr)
            cur.execute(
                "select COALESCE(max(log_id)::int,0)+10 seq from common_log_info where created_by = '" + gUserId + "'")
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
                sql += "VALUES (" + valueStr + ",now(),now(),'" + gUserId + "','" + gUserId + "','" + str(
                    rows[0][0]) + "')"

                cur.execute(sql)
                conn.commit()
            except Exception as e:
                # 객체 형태일 경우 출력을 해준다.
                sql += "attr1,creation_date,last_update_date, created_by, last_updated_by,log_id) "
                sql += "VALUES ('" + str(printStr).replace("'",
                                                           "") + "',now(),now(),'" + gUserId + "','" + gUserId + "','" + str(
                    rows[0][0]) + "')"
                cur.execute(sql)
                conn.commit()
        # 연결을 종료한다
        cur.close()
        conn.close()

        log_savefile(printStr)

def log_savefile(printStr):
    # file Save
    logame = 'log'
    log_path = '/hoya_log'

    filesavecnt = 3
    filesizeMax = 100000

    try:
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        filelist = os.listdir(log_path)

        now_time = str(datetime.datetime.now())
        fullname = log_path + '/' + logame + '_' + now_time
        fullname = fullname.replace(" ", ".")

        filelist.sort(reverse=True)

        i = 1
        for filename in filelist:
            step1 = filename.split("_")

            # file create
            if i == 1:
                fullname = log_path + '/' + filename
                fullname = fullname.replace(" ", ".")
                filesize = os.path.getsize(fullname)
                if filesize > filesizeMax:
                    fullname = log_path + '/' + step1[0] + '_' + now_time
                    fullname = fullname.replace(" ", ".")

            if i > filesavecnt:
                os.remove(log_path + '/' + filename)

            i += 1
        with open(fullname, "a") as myfile:
            myfile.write(str(printStr)+ '\n')
    except:
        None

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
    try:
        _origin_list = list(origin_list)
        _compare_list = list(compare_list)

        _union_values = set(_origin_list).union(set(_compare_list))
        _diff_values = sorted(list(_union_values - set(_origin_list)))
        _origin_list.extend(_diff_values)
    except Exception as e:
        logging.error("get_combine_label_list {0}".format(e))

    return _origin_list


def copy_all(src, dst):
    """ 디렉토리 안에 파일을 전부 복사 하는 유틸
         The util that anything(file, directories...) in directory to destination dirctory

    Args:
      params:
        * src : source directory
        * dst: distination directory

    Returns:
        None

    Raises:

    Example
        src = /hoya_model_root/nn00001/1/netconf_node/nn00001_1_19
        dst =/hoya_model_root/nn00001/1/netconf_node/nn00001_1_20
    """

    try:
        shutil.copytree(src, dst)
        logging.info("copytree source({0}) to dest ({1})".format(src, dst))
    except OSError as exc:  # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
            logging.info("copy source({0}) to dest ({1})".format(src, dst))
        else:
            logging.error("copy error source({0}) to dest ({1})".format(src, dst))
            #raise exc


def isnan(value):
    """ Pandas에서 Nan 검사하는 유틸
         The function is Nan Check in pandas

    Args:
      params:
        * value : anything

    Returns:
        True / False

    Raises:

    Example
        isnan('hello') == False
        isnan('NaN') == True
        isnan(100) == False
        isnan(float('nan')) = True
    """
    try:
        return math.isnan(float(value))
    except:
        return False

def make_and_exist_directory(directory):
    """ 디렉토리 만들기(없으면 만들고 있으면 현재 디렉토리 값 반환)
         Make Directory and Exist Directory

    Args:
      params:
        * directory : directory path

    Returns:
        directory path

    Raises:

    Example

    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory
    except Exception as e:
        logging.error("Make Celery Logging Directory {0} : {1}".format(directory, e))
        raise Exception(e)
        return False
