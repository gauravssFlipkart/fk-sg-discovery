import requests
import json


class IAASClient(object):

    @staticmethod
    def parse_response_ch(response):
        """
              fetch list of instances from a dict response
              :param response: dict of instances
              :return: return list of instance values
              """
        json_response = json.loads(response.text)
        return json_response.values()[0]

    @staticmethod
    def parse_response_nm(response):
        return json.loads(response.text)

    @staticmethod
    def fetch_intances_for_app_id(app_id):
        front_end_url_ch = 'http://10.32.105.112:4100/appdata?path=/apps/' + app_id + '/instances&version=beta'
        front_end_url_nm = 'http://10.47.1.196/api/compute/in-mumbai-prod/compute/v1/apps/' + app_id + '/instances'
        # hitting CH first
        response_ch = requests.get(front_end_url_ch)
        instances = IAASClient.parse_response_ch(response_ch)
        # in case the app is in NM
        if len(instances) == 0:
            # hitting NM now
            response_nm = requests.get(front_end_url_nm)
            return IAASClient.parse_response_nm(response_nm)
        else:
            return instances

    @staticmethod
    def fetch_elbs_for_app(app_id):
        elbs=[]
        elb_host = 'http://10.47.0.100/apps/' + app_id +'/aggregated/addresses'
        response = requests.get(elb_host)
        for elb_data in json.loads(response.text):
            for user in elb_data['users']:
                if user.endswith('forwarding-rule') or 'forwarding' in user:
                    elbs.append(elb_data['address'])
                    break
        return elbs


    @staticmethod
    def fetch_elb_name(elb_ip):
        elb_name_url = 'http://10.47.0.100/vips/'+elb_ip
        response = requests.get(elb_name_url)
        elb_name = (json.loads(response.text)['Users'][0]).rsplit('/', 1)[1]
        return elb_name



    @staticmethod
    def fetch_instances_from_elb(app_id, elb_name):
        elb_health_url = 'http://10.33.145.88:8080/apps/' + app_id + '/regions/ch/addresses/' + elb_name + '/versionedConfigs/deployed'
        response = requests.get(elb_health_url)

        if response.status_code == 200:
            health = json.loads(response.text)
            return health['Config']['BackendServiceHealths'].values()[0]['health_status'].keys()
        else:
            return list()