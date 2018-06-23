# splunkindexcontroller repository

This is a simple controller to demonstrate how to interact within kubernetes using python api and custom resource definitions

## Requisites

- a running kubernetes/openshift cluster

## Running

on minikub/gce

```
kubectl run splunkindexcontroller --image=lokeshgupta/splunkindexcontroller:1.0 --restart=Always
```

- on openshift ( enough privileges needed as i m checking splunkindexes cluster wide)

```
oc new-project splunkfluentd
oc adm policy add-cluster-role-to-user cluster-admin -z default -n splunkfluentd
oc new-app lokeshgupta/splunkindexcontroller:1.0
```

Note that the splunkindex custom resource definition gets created when launching the controller

## How to use

Create some splunkindex and see if exists or not

```
oc create -f crd/project1.yml
oc create -f crd/project2.yml
oc create -f crd/project3.yml
oc get splunkindexes -o yaml
```

## Copyright

Copyright 2018 Lokesh Gupta

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Problems?

Send me a mail at [lokeshgupta13@gmail.com](mailto:lokeshgupta13@gmail.com) !

Lokesh Gupta
