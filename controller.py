import json
import yaml
from kubernetes import client, config, watch
import os

DOMAIN = "fluentd.mylabs.local"
indexexist = ['project1', 'project3', 'project5']

def check_index(crds, obj):
    metadata = obj.get("metadata")
    if not metadata:
        print("No metadata in object, skipping: %s" % json.dumps(obj, indent=1))
        return
    name = metadata.get("name")
    namespace = metadata.get("namespace")
    obj["spec"]["isexist"] = True
    brand = obj["spec"]["projectname"]
    if brand in indexexist:
        obj["spec"]["comment"] = "Index exist for this project"
    else:
        obj["spec"]["comment"] = "Index does not exists for this project"

    print("Updating: %s" % name)
    crds.replace_namespaced_custom_object(DOMAIN, "v1", namespace, "splunkindexes", name, obj)


if __name__ == "__main__":
    if 'KUBERNETES_PORT' in os.environ:
        config.load_incluster_config()
        definition = '/tmp/splunkindex.yml'
    else:
        config.load_kube_config()
        definition = 'splunkindex.yml'
    configuration = client.Configuration()
    configuration.assert_hostname = False
    api_client = client.api_client.ApiClient(configuration=configuration)
    v1 = client.ApiextensionsV1beta1Api(api_client)
    current_crds = [x['spec']['names']['kind'].lower() for x in v1.list_custom_resource_definition().to_dict()['items']]
    if 'guitar' not in current_crds:
        print("Creating SplunkIndex definition")
        with open(definition) as data:
            body = yaml.load(data)
        v1.create_custom_resource_definition(body)
    crds = client.CustomObjectsApi(api_client)

    print("Waiting for SplunkIndexes to come up...")
    resource_version = ''
    while True:
        stream = watch.Watch().stream(crds.list_cluster_custom_object, DOMAIN, "v1", "splunkindexes", resource_version=resource_version)
        for event in stream:
            obj = event["object"]
            operation = event['type']
            spec = obj.get("spec")
            if not spec:
                continue
            metadata = obj.get("metadata")
            resource_version = metadata['resourceVersion']
            name = metadata['name']
            print("Handling %s on %s" % (operation, name))
            done = spec.get("isexist", False)
            if done:
                continue
            check_index(crds, obj)
