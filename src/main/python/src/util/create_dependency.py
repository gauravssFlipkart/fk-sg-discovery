from clients.mysql_client import connection


known_ports = {'27300': 'mongos', '9300': 'Elastic Search', '3306': 'mysql', '26379': 'Redis'}

class Dependency(object):

    @staticmethod
    def fetch_cur_row(sql, data):
        (_, cur) = connection()
        cur.execute(sql, data)
        for row in cur:
             return row

    @staticmethod
    def update_service_type(instance_ip, port,cur):

        print "port: ", port.replace(' ','')
        if port.replace(' ','') in known_ports.keys():
            print "FOUND"
            service_type = known_ports[port.replace(' ','')]
            sql1 = "UPDATE instance SET service_type=%s WHERE ip=%s"
            data = (service_type, instance_ip)
            cur.execute(sql1, data)
        else:
            print "NOT FOUND"
            pass


    @staticmethod
    def persist_dependency(dependency, source_inst, dest_inst):
        (_, cur) = connection()
        cur.execute("""INSERT INTO dependency (source_ip, dest_ip, source_port, dest_port, source_app_id, dest_app_id, dependency_type, source_group, dest_group) 
            VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s",  "%s")"""
                    % (str(source_inst[1]), str(dest_inst[1]), str(dependency[2]), str(dependency[3]), str(source_inst[3]),
                       str(dest_inst[3]), None, str(source_inst[8]), str(dest_inst[8])))

        Dependency.update_service_type(dest_inst[1], dependency[3], cur)

    @staticmethod
    def form_dependencies():
        (_, curr) = connection()
        sql1 = "Select id from dependency where source_ip = %s and dest_ip = %s"
        sql2 = "Select * from instance where ip = %s"
        sql3 = "Select * from instance where elb_ip = %s"
        file = open('../web/dependency.txt','r')
        for line in file.read().split('\n'):
            #split into SOURCE_IP, DEST_IP, SOURCE_PORT, DEST_PORT
            dependency = line.split(',')

            # find if dependency already exists

            data1 = ((dependency[0]).replace(' ',''), (dependency[1]).replace(' ',''))
            if curr.execute(sql1, data1):
                print "exists"
            else:
                if(dependency[0].split('.')[0].__eq__('172')):
                    pass
                else:
                    if(dependency[0].split('.')[1] == '47'):
                        data3 = (dependency[0]).strip()
                        source_inst = Dependency.fetch_cur_row(sql3, data3)
                        data2 = (dependency[1])
                        dest_inst = Dependency.fetch_cur_row(sql2, data2)
                        if(dest_inst and source_inst):
                            Dependency.persist_dependency(dependency, source_inst, dest_inst)
                        else:
                            print "Does Not exist"

                        print ("Dependency", source_inst, dest_inst)

                    else:

                        data5 = (dependency[1]).strip()
                        dest_inst2 = Dependency.fetch_cur_row(sql2, data5)
                        data4 = (dependency[0]).strip()
                        source_inst = Dependency.fetch_cur_row(sql2, data4)
                        if(dest_inst2 and source_inst):
                            Dependency.persist_dependency(dependency, source_inst, dest_inst2)

                            #print "Dependency YO", source_inst, dest_inst2
                        else:
                            print "Does Not exist"
