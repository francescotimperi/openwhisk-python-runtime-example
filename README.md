# openwhisk-python-runtime-example

Simple project showing how to customize an `Openwhisk` python runtimes with additional dependencies. Dependecies can be added via the `requirements.txt` or adding specifric pip install commands inside the provided `Dockerfile`

The project provides a simple `Taskfile` with the required command to build and deploy the required custom runtime.

## Note
- Do not include the python action code inside the custom runtime

## How to deploy an Openwishk action using the custom runtime
Assuming the built image has been deployed under the URL ghcr.io/francescotimperi/action-python-v10:0.3.0-morpheus.23012416 you can deploy a python action using the runtime
with a command similar to

```
wsk action create <action_name> <action_code.py> --docker ghcr.io/francescotimperi/action-python-v10:0.3.0-morpheus.23012416
```

