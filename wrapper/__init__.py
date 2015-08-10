# coding=UTF-8

"""Provides a wrapper that functions as the Cloudify interface."""

from __future__ import print_function
from resttypes import cobjects
from time import sleep

__author__ = 'alen'


###############################################################################
# "Utility functions"
###############################################################################

def get_token(fco_api):
    return fco_api.getAuthenticationToken(automaticallyRenew=True).publicToken


# TODO: time delta and parallel job
def wait_for_state(fco_api, res_uuid, state, res_type, time=10, step=10):
    fc1 = cobjects.FilterCondition(field='resourceUUID',
                                   condition='IS_EQUAL_TO',
                                   value=[res_uuid])
    fc2 = cobjects.FilterCondition(field='resourceState',
                                   condition='IS_EQUAL_TO',
                                   value=[state])
    sf = cobjects.SearchFilter(filterConditions=[fc1, fc2])
    result_set = fco_api.listResources(resourceType=res_type, searchFilter=sf)

    while step and not result_set.totalCount:
        result_set = fco_api.listResources(resourceType=res_type,
                                           searchFilter=sf)
        sleep(time)
        step -= 1

    return bool(result_set.totalCount)


def wait_for_status(fco_api, res_uuid, status, res_type, time=5, step=24):
    fc1 = cobjects.FilterCondition(field='resourceUUID',
                                   condition='IS_EQUAL_TO',
                                   value=[res_uuid])
    fc2 = cobjects.FilterCondition(field='status',
                                   condition='IS_EQUAL_TO',
                                   value=[status])
    sf = cobjects.SearchFilter(filterConditions=[fc1, fc2])
    result_set = fco_api.listResources(resourceType=res_type, searchFilter=sf)

    while step and not result_set.totalCount:
        result_set = fco_api.listResources(resourceType=res_type,
                                           searchFilter=sf)
        sleep(time)
        step -= 1

    return bool(result_set.totalCount)


def wait_for_job(fco_api, job_uuid, time=5, step=24):
    while step:
        job = get_resource(fco_api, job_uuid, 'JOB')
        if job.status in ['IN_PROGRESS', 'WAITING', 'NOT_STARTED', 'SUSPENDED']:
            continue
        return job.status == 'SUCCESSFUL'
    return False


def get_resource(fco_api, res_uuid, res_type):
    fc = cobjects.FilterCondition(field='resourceUUID',
                                  condition='IS_EQUAL_TO',
                                  value=[res_uuid])
    sf = cobjects.SearchFilter(filterConditions=[fc])
    try:
        return fco_api.listResources(searchFilter=sf, resourceType=res_type)\
            .list[0]
    except KeyError:
        return 'NOT_FOUND'


def first_resource(fco_api, res_type):
    return fco_api.resourceType(resourceType=res_type).list[0]


def get_resource_type(fco_api, res_type, limit=False, number=200, page=0):
    if limit:
        ql = cobjects.QueryLimit(from_=page*number, to=(page+1)*number,
                                 maxRecords=number, loadChildren=True)
        return fco_api.listResources(resourceType=res_type, queryLimit=ql)
    return fco_api.listResources(resourceType=res_type).list


def delete_resource(fco_api, res_uuid, res_type, cascade=False):
    return fco_api.deleteResource(resourceUUID=res_uuid, resourceType=res_type, cascade=cascade)


def get_prod_offer(fco_api, prod_offer_name):
    fc1 = cobjects.FilterCondition(field='resourceName',
                                   condition='IS_EQUAL_TO',
                                   value=[prod_offer_name])
    fc2 = cobjects.FilterCondition(field='resourceState',
                                   condition='IS_EQUAL_TO',
                                   value=['ACTIVE'])
    sf = cobjects.SearchFilter(filterConditions=[fc1, fc2])
    return fco_api.listResources(resourceType='PRODUCTOFFER',
                                 searchFilter=sf).list[0]


###############################################################################
# Cluster stuff
###############################################################################

def get_cluster_uuid(fco_api):
    return fco_api.listResources(resourceType='CLUSTER').list[0].resourceUUID


###############################################################################
# VDC stuff
###############################################################################

def create_vdc(fco_api, cluster_uuid, vdc_name):
    vdc = cobjects.VDC(resourceType='VDC', resourceName=vdc_name,
                       clusterUUID=cluster_uuid, sortOrder=None,
                       vdcUUID=None)
    return fco_api.createVDC(skeletonVDC=vdc)


def get_first_vdc(fco_api, cluster_uuid):
    for v in get_resource_type(fco_api, 'VDC'):
        if v.clusterUUID == cluster_uuid:
            return v
    return None


def get_vdc_uuid(fco_api):
    return fco_api.listResources(resourceType='VDC').list[0].resourceUUID


###############################################################################
# Network stuff
###############################################################################

def create_network(fco_api, cluster_uuid, net_type, vdc_uuid):
    net_data = cobjects.Network(clusterUUID=cluster_uuid,
                                resourceType='NETWORK', vdcUUID=vdc_uuid,
                                sortOrder=None, networkType=net_type,
                                resourceName='xxx')
    return fco_api.createNetwork(skeletonNetwork=net_data)


def get_network_uuid(fco_api, net_type, cluster_uuid):
    fc = cobjects.FilterCondition(field='resourceState',
                                  condition='IS_EQUAL_TO',
                                  value=['ACTIVE'])
    sf = cobjects.SearchFilter(filterConditions=[fc])
    ql = cobjects.QueryLimit(loadChildren=False, maxRecords=200)
    result_set = fco_api.listResources(searchFilter=sf, queryLimit=ql,
                                       resourceType='NETWORK')
    for v in result_set.list:
        if v.clusterUUID == cluster_uuid and v.networkType == net_type:
            return v.resourceUUID
    return None


###############################################################################
# Image stuff
###############################################################################

def get_image(fco_api, uuid):
    fc = cobjects.FilterCondition(field='resourceUUID',
                                  condition='IS_EQUAL_TO',
                                  value=[uuid])
    sf = cobjects.SearchFilter(filterConditions=[fc])
    result_set = fco_api.listResources(searchFilter=sf, resourceType='IMAGE')

    if not result_set.totalCount:
        raise RuntimeError('Image {} not found or no permissions to use.'
                           .format(uuid))

    return result_set.list[0]


###############################################################################
# Server stuff
###############################################################################

def get_server_state(fco_api, server_uuid):
    try:
        return get_resource(fco_api, server_uuid, 'SERVER').status
    except AttributeError:
        return 'NOT_FOUND'


def change_server_status(fco_api, server_uuid, state):
    fco_api.changeServerStatus(serverUUID=server_uuid, newStatus=state,
                               safe=True)
    return wait_for_status(fco_api, server_uuid, state, 'SERVER')


def start_server(fco_api, server_uuid):
    return change_server_status(fco_api, server_uuid, 'RUNNING')


def stop_server(fco_api, server_uuid):
    return change_server_status(fco_api, server_uuid, 'STOPPED')


def create_server(fco_api, server_name, server_po_uuid, image_uuid,
                  cluster_uuid, vdc_uuid, cpu_count, ram_amount,
                  boot_disk_po_uuid):
    disk_size = get_image(fco_api, image_uuid).size
    disk = cobjects.Disk(storageCapabilities=None, clusterUUID=None,
                         resourceType='DISK', iso=False, sortOrder=None,
                         vdcUUID=vdc_uuid, resourceName=None, size=disk_size,
                         resourceUUID=boot_disk_po_uuid)
    server = cobjects.Server(serverCapabilities=None, clusterUUID=cluster_uuid,
                             virtualizationType=None, resourceType='SERVER',
                             disks=[disk], vmId=None, sortOrder=None,
                             vdcUUID=vdc_uuid, resourceName=server_name,
                             productOfferUUID=server_po_uuid,
                             imageUUID=image_uuid, cpu=cpu_count,
                             ram=ram_amount)
    return fco_api.createServer(skeletonServer=server)


###############################################################################
# Disk stuff
###############################################################################

def create_disk(fco_api, vdc_uuid, disk_po_uuid, disk_name, disk_size):
    sc = ['CLONE', 'CHILDREN_PERSIST_ON_DELETE', 'CHILDREN_PERSIST_ON_REVERT']
    disk = cobjects.Disk(storageCapabilities=sc, clusterUUID=None,
                         resourceType='DISK', iso=False, sortOrder=None,
                         vdcUUID=vdc_uuid, resourceName=disk_name,
                         size=disk_size, resourceUUID=disk_po_uuid)
    return fco_api.createDisk(skeletonDisk=disk)


def attach_disk(fco_api, server_uuid, disk_uuid, index):
    return fco_api.attachDisk(serverUUID=server_uuid, diskUUID=disk_uuid,
                              index=index)


def detach_disk(fco_api, server_uuid, disk_uuid):
    return fco_api.detachDisk(serverUUID=server_uuid, diskUUID=disk_uuid)


###############################################################################
# NIC stuff
###############################################################################

def create_nic(fco_api, cluster_uuid, net_type, net_uuid,  vdc_uuid,
               nic_count):
    nic_data = cobjects.Nic(clusterUUID=cluster_uuid, networkUUID=net_uuid,
                            vdcUUID=vdc_uuid, resourceType='NIC',
                            serverUUID=None, sortOrder=None,
                            networkType=net_type,
                            resourceName=str(net_type)+'-'+nic_count)
    return fco_api.createNetworkInterface(skeletonNIC=nic_data)


def attach_nic(fco_api, server_uuid, nic_uuid, index):
    return fco_api.attachNetworkInterface(serverUUID=server_uuid,
                                          networkInterfaceUUID=nic_uuid,
                                          index=index)


def detach_nic(fco_api, server_uuid, nic_uuid):
    return fco_api.detachNic(serverUUID=server_uuid,
                             networkInterfaceUUID=nic_uuid)


###############################################################################
# SSH Key stuff
###############################################################################

def get_customer_keys(fco_api, customer_uuid):
    fc = cobjects.FilterCondition(field='customerUUID',
                                  condition='IS_EQUAL_TO',
                                  value=[customer_uuid])
    sf = cobjects.SearchFilter(filterConditions=[fc])
    return fco_api.listResources(resourceType='SSHKEY', searchFilter=sf)


def create_ssh_key(fco_api, public_key, key_name):
    key = cobjects.SSHKey(clusterUUID=None, resourceType='SSHKEY',
                          publicKey=public_key, public_key=False,
                          sortOder=None, vdcUUID=None, resourceName=key_name)
    return fco_api.createSSHKey(skeletonSSHKey=key)


def attach_ssh_key(fco_api, server_uuid, key_uuid):
    return fco_api.attachSSHKey(serverUUID=server_uuid, SSHKeyUUID=key_uuid)


def detach_ssh_key(fco_api, server_uuid, key_uuid):
    return fco_api.detachSSHKey(serverUUID=server_uuid, SSHKeyUUID=key_uuid)
