
import requests

## import url encoding functions
from urllib.parse import urlencode

## import the python classes that implement the various schemas defined and used by the api
from .schema.cluster import *
from .schema.infra_env import *

## importing helper functions
from .tools import *


API_BASE = "https://api.openshift.com/api/assisted-install/v2/"

def __get_headers():
    return  {
        "Authorization": "Bearer {}".format(__get_access_token()),
        "Content-Type": "application/json"
    }


def __get_access_token():
    # URL for the token request
    url = "https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token"

    # Headers to be sent with the request
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Data to be sent in the request, explicitly encoding each variable
    data = urlencode({
        "grant_type": "refresh_token",
        "client_id": "cloud-services",
        "refresh_token": os.environ.get("REDHAT_OFFLINE_TOKEN")
    })

    response = requests.post(url, headers=headers, data=data)
    access_token = response.json().get("access_token")
    return access_token


def get_cluster(cluster_id: str=None) -> requests.Response:
    url = API_BASE + f"clusters/{cluster_id}"

    response = requests.get(url, headers=__get_headers())
    return response   

def get_default_config() -> requests.Response:
    url = API_BASE + f"clusters/default-config"

    response = requests.get(url, headers=__get_headers())
 
    return response

def get_clusters(with_hosts: bool=False, owner: str=None) -> requests.Response:
    url = API_BASE + "clusters"

    if with_hosts:
        if '?' not in url:
            url += '?'
        url += f'with_hosts={with_hosts}&'            

    if owner is not None:
        if '?' not in url:
            url += '?'
        url += f'owner={owner}&'
    
    response = requests.get(url, headers=__get_headers())
 
    return response

def post_cluster(cluster: Cluster) -> requests.Response:
    VALID_POST_PARAMS = [
        "additional_ntp_source","api_vips","base_dns_domain","cluster_networks","cpu_architecture","disk_encryption",
        "high_availability_mode","http_proxy","https_proxy","hyperthreading","ignition_endpoint","ingress_vips",
        "machine_networks","name","network_type","no_proxy","ocp_release_image","olm_operators","openshift_version",
        "platform","pull_secret","schedulable_masters","service_network_cidr","service_networks","ssh_public_key",
        "tags","user_managed_networking","vip_dhcp_allocation",
        ]
    
    url = API_BASE + "clusters"

    cluster_params = filter_dict_by_keys(cluster.create_params(), VALID_POST_PARAMS)

    response = requests.post(url, headers=__get_headers(), json=cluster_params)    
 
    return response

def patch_cluster(cluster: Cluster) -> requests.Response:
    VALID_PATCH_PARAMS = [
        "additional_ntp_source","api_vips","base_dns_domain","cluster_network_cidr",
        "cluster_network_host_prefix","cluster_networks","disk_encryption","http_proxy","https_proxy","hyperthreading",
        "ignition_endpoint","ingress_vips","machine_network_cidr","machine_networks","name","network_type","no_proxy",
        "olm_operators","platform","pull_secret","schedulable_masters","service_network_cidr","service_networks",
        "ssh_public_key","tags","user_managed_networking","vip_dhcp_allocation",
        ]
    
    cluster_params = cluster.create_params()

    cluster_id = cluster_params.pop("cluster_id", None)

    if cluster_id is None:
        response = requests.Response()
        response._content = b'{"message": "cluster_id is requried to preform the patch operation"}'
        response.status_code = 404
        return response
    
    cluster_params = filter_dict_by_keys(cluster_params, VALID_PATCH_PARAMS)
    
    url = API_BASE + f"clusters/{cluster_id}"

    response = requests.patch(url, headers=__get_headers(), json=cluster_params)
 
    return response

def delete_cluster(cluster_id: str) -> bool:
    url = API_BASE + f"clusters/{cluster_id}"
    response = requests.delete(url, headers=__get_headers())
    return True if (response.status_code == 204) else False

def get_infrastructure_environement(infra_env_id: str) -> requests.Response:
    url = API_BASE + f"infra-envs/{infra_env_id}"

    response = requests.get(url, headers=__get_headers())
 
    return response

# Method that will implement the /v2/infra-envs GET assisted installer endpoint
def get_infrastructure_environements() -> requests.Response:
    url = API_BASE + "infra-envs"
    
    response = requests.get(url, headers=__get_headers())
 
    return response

    
def patch_infrastructure_environment(infra_env_id: str, data: dict) -> requests.Response:
    VALID_PATCH_PARAMS =  [
        "additional_ntp_sources","additional_trust_bundle","ignition_config_override","image_type",
        "kernel_arguments","proxy","pull_secret","ssh_authorized_key","static_network_config",
        ]
    
    infra_params = filter_dict_by_keys(data, VALID_PATCH_PARAMS)
    
    url = API_BASE + f"infra-envs/{infra_env_id}"

    response = requests.patch(url, headers=__get_headers(), json=infra_params)
 
    return response

def post_infrastructure_environment(infra_env: InfraEnv) -> requests.Response:
    VALID_POST_PARAMS = [
        "additional_ntp_sources","additional_trust_bundle","cluster_id","cpu_architecture",
        "ignition_config_override","image_type","kernel_arguments","name","openshift_version",
        "proxy","pull_secret","ssh_authorized_key","static_network_config",
        ]
    
    url = API_BASE + "infra-envs"

    infra_env_params = filter_dict_by_keys(infra_env.create_params(), VALID_POST_PARAMS)

    response = requests.post(url, headers=__get_headers(), json=infra_env_params)
 
    return response

def delete_infrastructure_environment(infra_env_id: str) -> bool:
    url = API_BASE + f"infra-envs/{infra_env_id}"

    response = requests.delete(url, headers=__get_headers())
    return True if (response.status_code == 204) else False

def cluster_action_allow_add_hosts(cluster_id: str):
    url = API_BASE + f"clusters/{cluster_id}/actions/allow-add-hosts"

    response = requests.post(url, headers=__get_headers())
 
    return response

def cluster_action_allow_add_workers(cluster_id: str):
    url = API_BASE + f"clusters/{cluster_id}/actions/allow-add-workers"

    response = requests.post(url, headers=__get_headers())
 
    return response

def cluster_action_cancel(cluster_id: str):
    url = API_BASE + f"clusters/{cluster_id}/actions/cancel"

    response = requests.post(url, headers=__get_headers())
    print(f"Successfully canceled installation for cluster: {cluster_id}") 
 
    return response

def cluster_action_complete_installation(cluster_id: str):
    url = API_BASE + f"clusters/{cluster_id}/actions/complete-installation"
    
    response = requests.post(url, headers=__get_headers())
    print(f"Successfully complete installation for cluster: {cluster_id}")      
 
    return response

def cluster_action_reset(cluster_id: str):
    url = API_BASE + f"clusters/{cluster_id}/actions/reset"

    response = requests.post(url, headers=__get_headers())
 
    return response

def cluster_action_install(cluster_id: str):

    url = API_BASE + f"clusters/{cluster_id}/actions/install"
    response = requests.post(url, headers=__get_headers())
    print(f"Successfully initiated cluster install for cluster: {cluster_id}")
 
    return response
    
def cluster_get_credentials(cluster_id: str, credentials: str = None):
    endpoint = f"clusters/{cluster_id}/downloads/credentials" if credentials is not None else f"clusters/{cluster_id}/credentials"
    url = API_BASE + endpoint
    
    query_string = {"file_name": credentials}

    if credentials is not None:
        response = requests.get(url, headers=__get_headers(), params=query_string)
        return response
    else:
        response = requests.get(url, headers=__get_headers())
        return response

def cluster_get_files(cluster_id: str, file_name: str = "install-config.yaml"):
    url = API_BASE + f"clusters/{cluster_id}/downloads/files"
    
    query_string = {"file_name": file_name}

    response = requests.get(url, headers=__get_headers(), params=query_string)
    return response

def get_infrastructure_environement_hosts(infra_env_id: str) -> requests.Response:
    url = API_BASE + f"infra-envs/{infra_env_id}/hosts"

    response = requests.get(url, headers=__get_headers())
 
    return response

def get_infrastructure_environement_host(infra_env_id: str, host_id: str) -> requests.Response:
    url = API_BASE + f"infra-envs/{infra_env_id}/hosts/{host_id}"

    response = requests.get(url, headers=__get_headers())
 
    return response