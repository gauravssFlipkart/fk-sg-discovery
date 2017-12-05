
class Service(object):

    def __init__(self, host_name, app_id, ip, zone, reservation_id, instance_id):
        self.host_name = host_name
        self.app_id = app_id
        self.ip = ip
        self.zone = zone
        self.reservation_id = reservation_id
        self.instance_id = instance_id

    @property
    def instance_info(self):
        return {
            'ip': self.ip,
            'instance_id': self.instance_id,
            'app_id' : self.app_id
        }

    def serialize(self):
        return self.ip

