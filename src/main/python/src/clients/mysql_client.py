from __future__ import print_function
import pymysql


def connection():

    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='service_graph', autocommit=True)
    cur = conn.cursor()
    #cur.execute("SELECT fname, lname FROM user")
    #print(cur.description)
    # print()
    # cur.close()
    # conn.close()

    return(conn, cur)


def store_instance(instance):
    (conn, cur) = connection()
    cur.execute("""INSERT INTO instance (ip, instance_id, app_id, host_name, zone, state, elb_ip, group_id, instance_group, group_tag) 
    VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s",  "%s", "%s")"""
% (instance.ip, instance.instance_id, instance.app_id, instance.host_name, instance.zone, instance.state, instance.elb_ip, instance.group_id, instance.instance_group, instance.group_tag))


def update_groups_for_inst(instance_ip, group_name):
    (_,cur)  = connection()
    sql1 = "UPDATE instance SET group_id=%s WHERE ip=%s"
    data = (group_name, instance_ip)
    cur.execute(sql1, data)