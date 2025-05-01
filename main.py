import asyncio
import base64
import json

from kubernetes_asyncio import client, config
from configuration import keyvault

DESKTOP_CONFIGURATION_PY = "C:\\Users\\pgorade\\Desktop\\configuration.py"


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


async def fetch_secret_kubernetes_async_api(context, namespace, secret_name, fp):
    # Load Kubernetes config (supports ~/.kube/config)
    await config.load_kube_config(context=context)

    # Create API instance
    v1 = client.CoreV1Api()

    # Read Secret in the default namespace
    result = await v1.read_namespaced_secret(name=secret_name, namespace=namespace)

    secret_key = "attribute.connection_strings.0" if secret_name.endswith(
        "document-storage") else "attribute.default_primary_connection_string"
    secret_value = base64.b64decode(result.data.get(secret_key)).decode()
    fp.write(f"Secret Name: {secret_name},\nValue: {secret_value}\n\n")

    await v1.api_client.close()
    return secret_value


def update_service_bus_configuration(update_conn_string: bool):
    if update_conn_string:
        for env in keyvault["envs-ltops"]:
            for key in keyvault[env]["CONNECTION_STRING"].keys():

                secret_key = f"{key}-servicebus-{keyvault[env]["namespace"]}-message-broker"
                try:
                    keyvault[env]["CONNECTION_STRING"][key] = asyncio.run(
                        fetch_secret_kubernetes_async_api(keyvault[env]["cluster"],
                                                          keyvault[env][
                                                              "namespace"],
                                                          secret_key))
                except Exception as e:
                    print(f"Could not find connection string for {key}")
    with open(DESKTOP_CONFIGURATION_PY, "w") as fp:
        fp.write(f"keyvault = {json.dumps(keyvault, indent=4)}")


def populate_document_store_configuration():
    FILE = "C:\\Users\\pgorade\\PycharmProjects\\fetch_kubernetes_secret\\document-store-connection-strings.txt"
    with open(FILE, "w") as fp:
        for env in keyvault["envs-ltops"]:
            for key in keyvault[env]["data_partitions"]:
                secret_key = f"{key}-documentstore-{keyvault[env]["namespace"]}-document-storage"
                try:
                    asyncio.run(fetch_secret_kubernetes_async_api(keyvault[env]["cluster"], keyvault[env]["namespace"],
                                                                  secret_key, fp))
                except Exception as e:
                    print(f"Could not find connection string for {key}")


def add_new_entry():
    env_list = [env for env in keyvault.keys() if
                isinstance(keyvault.get(env), dict) and keyvault.get(env).get("data_partition_id") not in [None, ""]]
    print(f"{env_list=}")
    with open(DESKTOP_CONFIGURATION_PY, "w") as fp:
        for env in env_list:
            # dw_dn_host was added
            if env.endswith("ltops"):
                dw_dns_host = {"dw_dns_host":"https://evt-dw.app.evt-1.lightops.slb.com"}
                keyvault.get(env).update(dw_dns_host)
        fp.write(f"keyvault = {json.dumps(keyvault, indent=4)}")

    # pass


if __name__ == "__main__":
    # update_service_bus_configuration(update_conn_string=True)
    # populate_document_store_configuration()
    add_new_entry()
