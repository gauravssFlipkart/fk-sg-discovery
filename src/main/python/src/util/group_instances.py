from clients.iaas_frontend import IAASClient
from clients.mysql_client import connection, update_groups_for_inst
from entities import service

class GroupOperation(object):
    """
    Grouping of instances
    """

    @staticmethod
    def group_instances_on_host_name(instances):
        group = {}
        (_, cur) = connection()
        for instance in instances:
            group_tag = instance['hostname'][:instance['hostname'].rindex('-')].rstrip('-0123456789')
            group.setdefault(group_tag, []).append(service.Service(instance['hostname'],
                                                                  instance['app'],
                                                                  instance['primary_ip'],
                                                                  instance['zone'],
                                                                  instance['reservation_id'],
                                                                  instance['id']).serialize())
            sql1 = "UPDATE instance SET group_tag=%s WHERE ip=%s"
            data = (group_tag, instance['primary_ip'])
            cur.execute(sql1, data)
        return group

    @staticmethod
    def group_on_elb(app_id, elb_ips, instances):

         (_, cur) = connection()
         elb_instance_ips = {}
         for elb_ip in elb_ips:
             elb_name = IAASClient.fetch_elb_name(elb_ip)
             print (elb_ip, elb_name)
             instance_ips = IAASClient.fetch_instances_from_elb(app_id, elb_name)
             if not instance_ips:
                 pass
             else:
                elb_instance_ips[elb_name] = instance_ips
                for instance_ip in instance_ips:
                    sql1 = "UPDATE instance SET elb_ip=%s WHERE ip=%s"
                    data = (elb_ip, instance_ip)
                    cur.execute(sql1, data)
         return elb_instance_ips


    @staticmethod
    def merge_groups(host_grp, elb_grp):
        print ("host-grp size:  elb-grp size ", len(host_grp), len(elb_grp))

        for elb_name, elb_ips in elb_grp.items():
            for host_name, host_ips in host_grp.items():
                set_host_ips = set(host_ips)
                set_elb_ips = set(elb_ips)
                if set_host_ips.issubset(set_elb_ips):
                    del host_grp[host_name]
                    # break if there is exact match
                    if len(host_ips) == len(elb_ips):
                        break
                elif set_elb_ips.issubset(set_host_ips):
                    res = list(set_elb_ips ^ set_host_ips)
                    host_grp[host_name] = res
                elif set_elb_ips.intersection(set_host_ips) > 0:
                    host_grp[host_name] = list(set_host_ips.difference(set_elb_ips))

                else:
                    print(set(elb_ips).difference(set(host_ips)))

        merged_groups = host_grp.copy()
        merged_groups.update(elb_grp)
        # print ("host-grp size:  elb-grp size ", len(host_grp), len(elb_grp))
        for group_name, inst_list in merged_groups.items():
            print group_name, inst_list
            for instance_ip in inst_list:
                update_groups_for_inst(instance_ip.strip(), group_name)

        return merged_groups