# coding=UTF-8

"""Server stuff."""

from __future__ import print_function
from fcoclient import clients
from fcoclient import api
from wrapper import (get_image,
                     get_first_vdc,
                     create_vdc,
                     get_prod_offer,
                     create_server,
                     create_ssh_key,
                     attach_ssh_key,
                     wait_for_state,
                     wait_for_status,
                     create_nic,
                     get_network_uuid,
                     create_network,
                     attach_nic,
                     get_resource,
                     get_server_state,
                     start_server,
                     stop_server,
                     delete_resource)
from datetime import datetime
import socket
import errno
from cloudify import ctx
from cloudify.decorators import operation
from wrapper.helpers import with_fco_api

PROP_IMAGE = 'image_uuid'
PROP_NET_TYPE = 'net_type'
PROP_DISK_SIZE = 'disk_size'
PROP_CPU_COUNT = 'cpu_count'
PROP_RAM_AMOUNT = 'ram_amount'
PROP_PUBLIC_KEYS = 'public_keys'
PROP_SERVER_PO_NAME = 'server_type'
PROP_CLUSTER = 'cluster_uuid'
PROP_NET = 'network_uuid'

RPROP_UUID = 'uuid'
RPROP_DISKS = 'disks'
RPROP_NICS = 'nics'
RPROP_IP = 'ip'
RPROP_USER = 'username'
RPROP_PASS = 'password'

def ssh_probe(server_ip, server_port=22, time=10, step=90):
    while step:
        ctx.logger.info('SSH probing [{}]'.format(step))
        try:
            s = socket.create_connection((server_ip, server_port), time)
            s.close()
            break
        except socket.error, msg:
            if str(msg[0]) == str(errno.ECONNREFUSED):
                break
            step -= 1
    return bool(step)


@operation
@with_fco_api
def create(fco_api, *args, **kwargs):
    ctx.logger.info('starting server creation')

    image_uuid = ctx.node.properties.get(PROP_IMAGE)
    net_type = ctx.node.properties.get(PROP_NET_TYPE, 'IP')
    cpu_count = ctx.node.properties.get(PROP_CPU_COUNT)
    ram_amount = ctx.node.properties.get(PROP_RAM_AMOUNT)
    public_keys = ctx.node.properties.get(PROP_PUBLIC_KEYS, [])
    server_po_name = ctx.node.properties.get(PROP_SERVER_PO_NAME)
    net_uuid = ctx.node.properties.get(PROP_NET)

    # Get cluster and VDC UUID

    ctx.logger.info('image UUID: ' + image_uuid)
    ctx.logger.info('fco_api: ' + str(fco_api))

    image = get_image(fco_api, image_uuid)
    cluster_uuid = ctx.node.properties.get(PROP_CLUSTER) or image.clusterUUID
    vdc_uuid = get_first_vdc(fco_api, cluster_uuid).resourceUUID

    # Set up VDC
    if not vdc_uuid:
        vdc_uuid = create_vdc(fco_api, cluster_uuid, 'VDC ' + datetime.now()
                              .strftime('%Y-%m-%d %H:%M:%S')).itemUUID
    if not vdc_uuid:
        raise Exception('Could not get or create VDC!')

    ctx.logger.info('VDC UUID: ' + vdc_uuid)

    # Get Server PO
    server_po_uuid = get_prod_offer(fco_api, server_po_name).resourceUUID
    if not server_po_uuid:
        raise Exception('No product offer found! ({})'.format(
            'Standard Server'))

    ctx.logger.info('VDC UUID: ' + vdc_uuid)

    # Get disk PO
    image_disk_po_name = '{} GB Storage Disk'.format(image.size)
    boot_disk_po_uuid = get_prod_offer(fco_api, image_disk_po_name)\
        .resourceUUID
    if not boot_disk_po_uuid:
        raise Exception('No product offer found! ({})'.format(
            image_disk_po_name))

    ctx.logger.info('Boot disk PO UUID: ' + boot_disk_po_uuid)

    # Create server
    server_name = 'VM ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    create_server_job = create_server(fco_api, server_name, server_po_uuid,
                                      image_uuid, cluster_uuid, vdc_uuid,
                                      cpu_count, ram_amount,
                                      boot_disk_po_uuid)
    server_uuid = create_server_job.itemUUID

    ctx.logger.info('Server UUID: ' + vdc_uuid)

    # Add keys
    for single_key in public_keys:
        key_uuid = create_ssh_key(fco_api, single_key, '').itemUUID
        attach_ssh_key(fco_api, server_uuid, key_uuid)

    ctx.logger.info('Keys attached')

    # Wait for server to be active
    if not wait_for_state(fco_api, server_uuid, 'ACTIVE', 'SERVER'):
        raise Exception('Server failed to prepare in time!')

    ctx.logger.info('Server ACTIVE')

    # Get network
    if not net_uuid:
        net_uuid = get_network_uuid(fco_api, net_type, cluster_uuid)
    if not net_uuid:
        net_uuid = create_network(fco_api, cluster_uuid, net_type, vdc_uuid)\
            .itemUUID
    if not net_uuid:
        raise Exception('Failed to create network')

    ctx.logger.info('Network UUID: ' + net_uuid)

    # Create NIC
    nic_uuid = create_nic(fco_api, cluster_uuid, net_type, net_uuid, vdc_uuid,
                          '0').itemUUID
    if not wait_for_state(fco_api, nic_uuid, 'ACTIVE', 'NIC'):
        raise Exception('NIC failed to create in time!')

    ctx.logger.info('NIC UUID ' + nic_uuid)

    # Stop server if started
    if get_server_state(fco_api, server_uuid) != 'STOPPED':
        if not stop_server(fco_api, server_uuid):
            raise Exception('Stopping server failed to complete in time!')

    ctx.logger.info('Server STOPPED')

    # Attach NIC
    attach_nic_job = attach_nic(fco_api, server_uuid, nic_uuid, 1)
    if not wait_for_status(fco_api, attach_nic_job.resourceUUID, 'SUCCESSFUL',
                           'JOB'):
        raise Exception('Attaching NIC failed to complete in time!')

    server = get_resource(fco_api, server_uuid, 'SERVER')
    server_uuid = server.resourceUUID  # does it change?

    ctx.logger.info('NICs attached')

    # attach any disks now

    ctx.logger.info('Disks attached')

    # Start server if not started
    if get_server_state(fco_api, server_uuid) == 'STOPPED':
        if not start_server(fco_api, server_uuid):
            raise Exception('Running server failed to complete in time!')

    ctx.logger.info('Server RUNNING')

    server = get_resource(fco_api, server_uuid, 'SERVER')
    server_ip = server.nics[0].ipAddresses[0].ipAddress
    server_port = 22

    if not ssh_probe(server_ip, server_port, step=-1):
        raise Exception('Starting server failed to complete in time!')

    ctx.logger.info('Server READY')

    ctx.instance.runtime_properties[RPROP_UUID] = server.resourceUUID
    ctx.instance.runtime_properties[RPROP_DISKS] = [d.resourceUUID for d in server.disks]
    ctx.instance.runtime_properties[RPROP_NICS] = [n.resourceUUID for n in server.nics]
    ctx.instance.runtime_properties[RPROP_IP] = server_ip
    ctx.instance.runtime_properties[RPROP_USER] = server.initialUser
    ctx.instance.runtime_properties[RPROP_PASS] = server.initialPassword

    ctx.logger.info('Server IP: ' + server_ip)
    ctx.logger.info('Server User: ' + server.initialUser)
    ctx.logger.info('Server Password: ' + server.initialPassword)

    return server.resourceUUID, server_ip, server.initialUser, server.initialPassword


@operation
@with_fco_api
def delete(fco_api, *args, **kwargs):
    server_uuid = ctx.instance.runtime_properties.get(RPROP_UUID)
    for d in ctx.instance.runtime_properties[RPROP_DISKS]:
        job_uuid = delete_resource(fco_api, d, 'DISK').resourceUUID
        if not wait_for_status(fco_api, job_uuid, 'SUCCESSFUL', 'JOB'):
            raise Exception('Failed to delete disk from server')
    for n in ctx.instance.runtime_properties[RPROP_NICS]:
        job_uuid = delete_resource(fco_api, n, 'NIC').resourceUUID
        if not wait_for_status(fco_api, job_uuid, 'SUCCESSFUL', 'JOB'):
            raise Exception('Failed to delete NIC from server')
    job_uuid = delete_resource(fco_api, server_uuid, 'SERVER').resourceUUID
    if not wait_for_status(fco_api, job_uuid, 'SUCCESSFUL', 'JOB'):
        raise Exception('Failed to delete server')


@operation
@with_fco_api
def start(fco_api, *args, **kwargs):
    server_uuid = ctx.instance.runtime_properties.get(RPROP_UUID)
    if get_server_state(fco_api, server_uuid) != 'RUNNING':
        if not start_server(fco_api, server_uuid):
            raise Exception('Could not start server!')


@operation
@with_fco_api
def stop(fco_api, *args, **kwargs):
    server_uuid = ctx.instance.runtime_properties.get(RPROP_UUID)
    if get_server_state(fco_api, server_uuid) != 'STOPPED':
        if not stop_server(fco_api, server_uuid):
            raise Exception('Could not stop server!')


@operation
@with_fco_api
def creation_validation(fco_api, *args, **kwargs):
    server_uuid = ctx.instance.runtime_properties.get(RPROP_UUID)
    try:
        get_resource(fco_api, server_uuid, 'SERVER')
    except Exception:
        return False
    return True
