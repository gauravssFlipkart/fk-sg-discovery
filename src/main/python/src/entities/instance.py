# from sqlalchemy.testing import db


class Instance(object):

    def __init__(self, ip, instance_id, app_id, host_name, zone, state, elb_ip, group_id, instance_group, group_tag):
        self.ip = ip
        self.instance_id = instance_id
        self.app_id = app_id
        self.host_name = host_name,
        self.zone = zone
        self.state = state
        self.elb_ip = elb_ip
        self.group_id = group_id,
        self.instance_group = instance_group
        self.group_tag = group_tag


# class User(db.Model):
#
#     id = db.Column('student_id', db.Integer, primary_key=True)
#     fname = db.Column(db.String(100))
#     lname = db.Column(db.String(50))
#
#     def __init__(self, fname, lname):
#         self.id = 1
#         self.fname = fname
#         self.lname = lname

