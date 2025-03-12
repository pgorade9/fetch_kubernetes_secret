import asyncio
import base64
import json

from kubernetes_asyncio import client, config
from configuration import keyvault


async def listpods_kubernetes_async_api(context, namespace):
    # Load Kubernetes config (supports ~/.kube/config)
    await config.load_kube_config(context=context)

    # Create API instance
    v1 = client.CoreV1Api()

    # List pods in the default namespace
    pods = await v1.list_namespaced_pod(namespace=namespace)

    for pod in pods.items:
        print(f"Pod Name: {pod.metadata.name}, Status: {pod.status.phase}")

    await v1.api_client.close()


async def fetch_secret_kubernetes_async_api(context, namespace, secret_name):
    # Load Kubernetes config (supports ~/.kube/config)
    await config.load_kube_config(context=context)

    # Create API instance
    v1 = client.CoreV1Api()

    # Read Secret in the default namespace
    result = await v1.read_namespaced_secret(name=secret_name, namespace=namespace)

    secret_value = base64.b64decode(result.data.get('attribute.default_primary_connection_string')).decode()
    print(f"Secret Name: {secret_name}, \n Value: {secret_value}")

    await v1.api_client.close()
    return secret_value


def update_service_bus_configuration(update_conn_string:bool):
    if update_conn_string:
        for env in keyvault["envs-ltops"]:
            secret_key = f"{keyvault[env]["data_partition_id"]}-servicebus-{keyvault[env]["namespace"]}-message-broker"
            keyvault[env]["CONNECTION_STRING"] = asyncio.run(fetch_secret_kubernetes_async_api(keyvault[env]["cluster"],
                                                          keyvault[env]["namespace"],
                                                          secret_key))
    FILE = "C:\\Users\\pgorade\\Desktop\\configuration.py"
    with open(FILE,"w") as fp:
        fp.write(f"keyvault = {json.dumps(keyvault,indent=4)}")



if __name__ == "__main__":
    update_service_bus_configuration(update_conn_string=False)
