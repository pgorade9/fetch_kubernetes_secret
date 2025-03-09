import asyncio
import base64

from kubernetes_asyncio import client, config

from config_local import context, namespace, secret_key


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

    print(f"Secret Name: {secret_name}, Value: {result.api_version}")
    print(f"Secret Name: {secret_name}, Value: {base64.b64decode(result.data.get('attribute.default_primary_connection_string')).decode()}")

    await v1.api_client.close()


if __name__ == "__main__":
    # asyncio.run(listpods_kubernetes_async_api(context,namespace))
    asyncio.run(fetch_secret_kubernetes_async_api(context, namespace, secret_key))
