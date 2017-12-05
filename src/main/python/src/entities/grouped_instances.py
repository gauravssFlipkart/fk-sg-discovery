
class InstanceGroups(object):

    def __init__(self, hostname_group, elb_group):
        self.hostname_group = hostname_group
        self.elb_group = elb_group

    @property
    def elb_group(self):
        return self.elb_group

    @property
    def hostname_group(self):
        return self.hostname_group