import logging
from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy

from clients.iaas_frontend import IAASClient
from clients.mysql_client import connection, store_instance
from entities.instance import Instance
from util.create_dependency import Dependency
from util.group_instances import GroupOperation

app = Flask(__name__)


def persist_instances(instances):
    for instance in instances:
        if instance.has_key('instance_group') :
            store_instance(Instance(instance['primary_ip'], instance['id'], instance['app'], instance['hostname'], instance['zone'], instance['state'], None, None, instance['instance_group'], None))
        else:
            store_instance(Instance(instance['primary_ip'], instance['id'], instance['app'], instance['hostname'], instance['zone'], instance['state'], None, None, None, None))


@app.route("/apps", methods=["GET"])
def app_func():
    logging.basicConfig(level=logging.INFO, filename="log.txt")
    app_id = request.args.get("appId")

    if not app_id:
        logging.error("No appId in request")
        return Response("AppId must be there", 400)
    else:
        instances = IAASClient.fetch_intances_for_app_id(app_id)
        persist_instances(instances)
        elbs = IAASClient.fetch_elbs_for_app(app_id)
        print 'number of instances:', len(instances)
        instance_groups_per_elb = GroupOperation.group_on_elb(app_id, elbs, instances)
        instance_groups_per_hostname = GroupOperation.group_instances_on_host_name(instances)
        merged_group = GroupOperation.merge_groups(instance_groups_per_hostname.copy(), instance_groups_per_elb)

        return jsonify((instance_groups_per_elb, instance_groups_per_hostname, merged_group))


@app.route("/apps/dependency", methods=["GET"])
def find_dependeny():
    logging.basicConfig(level=logging.INFO, filename="log.txt")
    Dependency.form_dependencies()
    return "Go it"




app.run('0.0.0.0', 9900)
