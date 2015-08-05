# coding=UTF-8

"""Provides abstraction of the FCO REST API endpoints."""

import rest_types.enums as enums
import rest_types.cobjects as cobjects
from rest_types import (to_string, rat_check)
from rest_types import is_acceptable as c_is_acceptable
from rest_types import construct_data as c_construct_data
from typed import Typed
from typed.builtins import (List, Dict)

from enum import Enum
from datetime import datetime

Verbs = Enum('Verbs', 'GET POST PUT DELETE')


class Endpoint(Typed):

    """Generic class for FCO REST API endpoints."""

    ENDPOINTS = []

    ALL_PARAMS = set()
    REQUIRED_PARAMS = set()
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {}

    ALL_DATA = set()
    REQUIRED_DATA = set()
    OPTIONAL_DATA = set()
    DATA_TYPES = {}

    RETURNS = {}

    def __init__(self, parameters=None, data=None, **kwargs):
        super(Endpoint, self).__init__(self)

        # We can append underscores to avoid keyword conflicts
        kwargs = {k.rstrip('_'): to_string(v) for k, v in kwargs.items()}

        parameters, data = self.prepare_input(parameters, data, **kwargs)

        merged = parameters.copy()
        merged.update(data)

        if not self.is_acceptable(merged):
            raise Exception('Invalid data to create class {}'
                            .format(type(self).__name__))

        self.parameters = {}
        for k, v in parameters:
            self.parameters[k] = c_construct_data(v, self.PARAMS_TYPES,
                                                  self._noneable)
        self._data = {}
        for k, v in data:
            self._data[k] = c_construct_data(v, self.DATA_TYPES[k],
                                             self._noneable)
        self.endpoint = self.get_endpoint(parameters, data)

    @classmethod
    def prepare_input(cls, parameters=None, data=None, *args, **kwargs):
        if parameters is None:
            parameters = {}
        if data is None:
            data = {}
        parameters.update({k: v for k, v in kwargs.items() if k in
                           cls.ALL_PARAMS})
        data.update({k: v for k, v in kwargs.items() if k in cls.ALL_DATA})

        for param in cls.ALL_PARAMS:
            try:
                k, idx = param.split('.')
                if (param in parameters and data[k][idx] !=
                        parameters[param]):
                    raise ValueError('inconsistent type between data and'
                                     'parameters')
                parameters[param] = data[k][idx]
            except (KeyError, ValueError):
                pass

        rat_check(parameters, cls.ALL_PARAMS, cls.REQUIRED_PARAMS,
                  cls.PARAMS_TYPES, cls._noneable)
        rat_check(data, cls.ALL_DATA, cls.REQUIRED_DATA, cls.DATA_TYPES,
                  cls._noneable)

        return parameters, data

    @classmethod
    def get_endpoint(cls, parameters=None, data=None):
        valid_endpoints = []
        for endpoint in cls.ENDPOINTS:
            try:
                url = endpoint[1].format(**parameters)
                if '{' not in url:
                    valid_endpoints.append((endpoint[0], url))
            except (KeyError, TypeError):
                pass
        if not valid_endpoints:
            raise Exception('no valid endpoints found for given data')
        if len(valid_endpoints) > 1:
            # TODO: choosing endpoints intelligently
            # prefer post or put if we have a payload, or vice versa
            if data:
                post_endpoints = [e for e in valid_endpoints if e[0] is
                                  Verbs.POST]
                if len(post_endpoints):
                    return post_endpoints[0]
                put_endpoints = [e for e in valid_endpoints if e[0] is
                                 Verbs.PUT]
                if len(put_endpoints):
                    return put_endpoints[0]
            else:
                get_endpoints = [e for e in valid_endpoints if e[0] is
                                 Verbs.GET]
                if len(get_endpoints):
                    return get_endpoints[0]
                del_endpoints = [e for e in valid_endpoints if e[0] is
                                 Verbs.DELETE]
                if len(del_endpoints):
                    return del_endpoints[0]
        return valid_endpoints[0]

    @classmethod
    def validate_return(cls, return_value):
        return c_is_acceptable(return_value, cls.RETURNS.values()[0],
                               cls._noneable)

    # TODO: not merge but iterate separately
    # TODO: catch exceptions upstairs
    @classmethod
    def is_acceptable(cls, inst):
        req = cls.REQUIRED_PARAMS | cls.REQUIRED_DATA
        opt = cls.OPTIONAL_PARAMS | cls.OPTIONAL_DATA

        # TODO: merge smarter
        # TODO: proper exceptions
        types = cls.PARAMS_TYPES.copy()
        types.update(cls.DATA_TYPES)
        try:
            for k, v in inst.items():
                if k in req:
                    req.remove(k)
                else:
                    opt.remove(k)
                if not c_is_acceptable(v, types[k], cls._noneable):
                    return False
        except:
            raise
        return not req or cls._noneable

    def __str__(self):
        return str(self.endpoint[0]) + ' ' + self.endpoint[1] + ': ' + \
                str(self._data)


class UpdateUser(Endpoint):

    """FCO REST API updateUser endpoint.

    This function will update a user's details and returns the updated
    user.

    Remarks:
    See createUser for comments on plaintext and hashed passwords.

    Parameters (type name (required): description):
        str userDetails.resourceUUID (T):
            The resourceUUID field of the referenced userDetails object

    Data (type name (required): description):
        str passwordHash (F):
            The new hashed password
        str password (F):
            The new plaintext password
        cobjects.UserDetails userDetails (T):
            The UserDetail object to update

    Returns (type name: description):
        cobjects.UserDetails user:
            The updated UserDetail object
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/user/{userDetails.resourceUUID}')]

    ALL_PARAMS = {'userDetails.resourceUUID'}
    REQUIRED_PARAMS = {'userDetails.resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'userDetails.resourceUUID': str}

    ALL_DATA = {'password', 'passwordHash', 'userDetails'}
    REQUIRED_DATA = {'userDetails'}
    OPTIONAL_DATA = {'passwordHash', 'password'}
    DATA_TYPES = {'passwordHash': str, 'password': str, 'userDetails':
                  cobjects.UserDetails}

    RETURNS = {'user': cobjects.UserDetails}


class GetResource(Endpoint):

    """FCO REST API getResource endpoint.

    Gets a resource of the given type with the specified UUID.

    Parameters (type name (required): description):
        enums.ResourceType resourceType (F):
            The type of the required resource.
        str resourceUUID (T):
            The UUID of the required resource.

    Data (type name (required): description):
        bool loadChildren (F):
            State if the child objects should be loaded.

    Returns (type name: description):
        cobjects.PseudoResource resource:
            The retrieved resource object.
    """

    ENDPOINTS = [(Verbs.GET, 'resources/{resourceType}/{resourceUUID}'),
                 (Verbs.GET, 'resources/{resourceUUID}')]

    ALL_PARAMS = {'resourceType', 'resourceUUID'}
    REQUIRED_PARAMS = {'resourceUUID'}
    OPTIONAL_PARAMS = {'resourceType'}
    PARAMS_TYPES = {'resourceType': enums.ResourceType, 'resourceUUID': str}

    ALL_DATA = {'loadChildren'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'loadChildren'}
    DATA_TYPES = {'loadChildren': bool}

    RETURNS = {'resource': cobjects.PseudoResource}


class GetCompiledTranslation(Endpoint):

    """FCO REST API getCompiledTranslation endpoint.

    Gets the compiled value of a Translation object.

    Parameters (type name (required): description):
        str translationUUID (T):
            The UUID of the translation object.

    Returns (type name: description):
        Dict(str, str) translationMap:
            A map holder containing the translation values.
    """

    ENDPOINTS = [(Verbs.GET,
                 'resources/translation/{translationUUID}/compile')]

    ALL_PARAMS = {'translationUUID'}
    REQUIRED_PARAMS = {'translationUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'translationUUID': str}

    RETURNS = {'translationMap': Dict(str, str)}


class ListStatementDetail(Endpoint):

    """FCO REST API listStatementDetail endpoint.

    This function will list the statement details matching a given
    filter.

    Remarks:
    On successful execution, a list of statement details will be
    returned. On an exception, an empty list is returned.

    Data (type name (required): description):
        cobjects.SearchFilter searchFilter (F):
            The filter to apply
        cobjects.QueryLimit queryLimit (F):
            The query limit for the filter

    Returns (type name: description):
        cobjects.ListResult listStatementDetail:
            The list of statement details
    """

    ENDPOINTS = [(Verbs.GET, 'resources/statement_detail/list'), (Verbs.POST,
                 'resources/statement_detail/list')]

    ALL_DATA = {'searchFilter', 'queryLimit'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'searchFilter', 'queryLimit'}
    DATA_TYPES = {'searchFilter': cobjects.SearchFilter, 'queryLimit':
                  cobjects.QueryLimit}

    RETURNS = {'listStatementDetail': cobjects.ListResult}


class GetMeasuredValues(Endpoint):

    """FCO REST API getMeasuredValues endpoint.

    This function will return a list of measured values close to a given
    time stamp.

    Remarks:
    One measured value is returned per measure key specified in
    measureKeys, or if an empty array is passed one measured values of
    each type available is returned. Each measured value will be the
    latest measured value with a measurement timestamp at or before the
    timestamp passed, i.e. the timestamp of the measured value returned
    is guaranteed to have the largest timestamp available which is less
    than or equal to the timestamp passed. If the timestamp is not
    specified (timestamp <= 0), the current time will be used as the
    timestamp. Note that as measured values are measured asynchronously,
    the timestamp of each measured value returned is likely to differ.
    To return a series of more than one measured value with the same
    measure key, use doQuery. On successful execution, a list of
    measured values which matches the requested list or if no list is
    passed a list of all measured values will be returned; in each case,
    there will only be one measured value with each measure key. On
    error, an exception will be thrown and no MeasuredValues will be
    returned.

    Parameters (type name (required): description):
        int timestamp (T):
            Unix timestamp

    Data (type name (required): description):
        List(str) resourceUUID (F):
            List of resource UUIDs
        List(str) measureKeys (F):
            List of keys of the measured values sought

    Returns (type name: description):
        List(cobjects.MeasuredValue) measuredValues:
            The list of measured values
    """

    ENDPOINTS = [(Verbs.GET, 'resources/measurement/timestamp/{timestamp}')]

    ALL_PARAMS = {'timestamp'}
    REQUIRED_PARAMS = {'timestamp'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'timestamp': int}

    ALL_DATA = {'resourceUUID', 'measureKeys'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'resourceUUID', 'measureKeys'}
    DATA_TYPES = {'resourceUUID': List(str), 'measureKeys': List(str)}

    RETURNS = {'measuredValues': List(cobjects.MeasuredValue)}


class AddIP(Endpoint):

    """FCO REST API addIP endpoint.

    This function will add an IP address to a network interface.

    Remarks:
    Please note that you will only be able to have one IPv4 address set
    as 'auto' in a network interface. An automatic IPv6 address is set
    on the network interface at creation time and can not be altered.
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not modified.

    Parameters (type name (required): description):
        str networkInterfaceUUID (T):
            The UUID of the network interface
        str ipAddress (T):
            The IP address to be added

    Data (type name (required): description):
        bool auto (T):
            Set if the IPv4 address needs to be set on the NIC via dhcp
        datetime when (F):
            A date object specifying when the job is to be scheduled

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/nic/{networkInterfaceUUID}/ip_address/{ipAddress}/'
                  'add')]

    ALL_PARAMS = {'networkInterfaceUUID', 'ipAddress'}
    REQUIRED_PARAMS = {'networkInterfaceUUID', 'ipAddress'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'networkInterfaceUUID': str, 'ipAddress': str}

    ALL_DATA = {'auto', 'when'}
    REQUIRED_DATA = {'auto'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'auto': bool, 'when': datetime}

    RETURNS = {'job': cobjects.Job}


class PayInvoice(Endpoint):

    """FCO REST API payInvoice endpoint.

    This function marks an existing invoice status either
    pending,paid,unpaid or void.

    Remarks:
    On an exception, the invoice is not updated.

    Parameters (type name (required): description):
        str invoiceUUID (T):
            The UUID of the invoice to update

    Data (type name (required): description):
        str paymentMethodInstanceUUID (T):
            The UUID of the payment method instance used to pay the
            invoice.
        datetime when (F):
            A date object specifying when the job is to be scheduled
        str interactiveInputReturnURL (F):
            The URL for interactive input return
        bool allowInteractive (T):
            Indicates whether callbacks may be used by this payment
            method instance for 3DS transactions

    Returns (type name: description):
        cobjects.Job job:
            The job associated with the payment
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/invoice/{invoiceUUID}/pay')]

    ALL_PARAMS = {'invoiceUUID'}
    REQUIRED_PARAMS = {'invoiceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'invoiceUUID': str}

    ALL_DATA = {'paymentMethodInstanceUUID', 'interactiveInputReturnURL',
                'when', 'allowInteractive'}
    REQUIRED_DATA = {'paymentMethodInstanceUUID', 'allowInteractive'}
    OPTIONAL_DATA = {'when', 'interactiveInputReturnURL'}
    DATA_TYPES = {'paymentMethodInstanceUUID': str, 'when': datetime,
                  'interactiveInputReturnURL': str, 'allowInteractive': bool}

    RETURNS = {'job': cobjects.Job}


class CreateImage(Endpoint):

    """FCO REST API createImage endpoint.

    This function will create an image from a server or disk.

    Remarks:
    Whether a server or disk can be used depends on the capabilities of
    the cluster concerned. The call may be scheduled for a future date
    by setting the 'when' parameter. On successful execution, a Job
    object will be returned. On an exception, the resource is not
    created.

    Data (type name (required): description):
        cobjects.Image skeletonImage (T):
            A skeleton of the image to be created
        cobjects.FetchParameters fetchParameters (F):
            The parameters holding the url details
        datetime when (F):
            A date object specifying when the job is to be scheduled

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.POST, 'resources/image')]

    ALL_DATA = {'skeletonImage', 'fetchParameters', 'when'}
    REQUIRED_DATA = {'skeletonImage'}
    OPTIONAL_DATA = {'fetchParameters', 'when'}
    DATA_TYPES = {'skeletonImage': cobjects.Image, 'fetchParameters':
                  cobjects.FetchParameters, 'when': datetime}

    RETURNS = {'job': cobjects.Job}


class AttachDisk(Endpoint):

    """FCO REST API attachDisk endpoint.

    This function will attach a disk to an existing server.

    Remarks:
    The server must not be running when the call is made. The index
    parameter is an integer specifying the position in the list of disks
    that the disk in question should take, When index is 0 disk is added
    to the first position, only if no disks are attached to the given
    server, otherwise is added in the last position. Other disks will be
    shuffled around appropriately. The call may be scheduled for a
    future date by setting the 'when' parameter. On successful
    execution, a Job object will be returned. On an exception, the
    resource is not attached.

    Parameters (type name (required): description):
        str serverUUID (T):
            The UUID of the server to which disk is to be attached
        str diskUUID (T):
            The UUID of the disk to be attached

    Data (type name (required): description):
        int index (T):
            The position in the list of disks that the attached disk
            should take
        datetime when (F):
            A date object specifying when the job is to be scheduled

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/server/{serverUUID}/disk/{diskUUID}/attach')]

    ALL_PARAMS = {'serverUUID', 'diskUUID'}
    REQUIRED_PARAMS = {'serverUUID', 'diskUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'serverUUID': str, 'diskUUID': str}

    ALL_DATA = {'index', 'when'}
    REQUIRED_DATA = {'index'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'index': int, 'when': datetime}

    RETURNS = {'job': cobjects.Job}


class PublishImage(Endpoint):

    """FCO REST API publishImage endpoint.

    This function will publish an image to a Customer or a Billing
    Entity.

    Parameters (type name (required): description):
        str imageUUID (T):
            The UUID of the image to publish

    Data (type name (required): description):
        bool exclude (F):
            To exclude/include the publishTo
        str publishTo (T):
            The UUID of the customer or billing entity to publish to

    Returns (type name: description):
        bool success:
            Returns true on success; otherwise, false.
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/image/{imageUUID}/publish')]

    ALL_PARAMS = {'imageUUID'}
    REQUIRED_PARAMS = {'imageUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'imageUUID': str}

    ALL_DATA = {'exclude', 'publishTo'}
    REQUIRED_DATA = {'publishTo'}
    OPTIONAL_DATA = {'exclude'}
    DATA_TYPES = {'exclude': bool, 'publishTo': str}

    RETURNS = {'success': bool}


class AddUserToGroup(Endpoint):

    """FCO REST API addUserToGroup endpoint.

    This function adds a user to the specified group.

    Parameters (type name (required): description):
        str userUUID (T):
            The UUID of the user to add
        str groupUUID (T):
            The UUID of the group to which the user is to be added

    Returns (type name: description):
        bool success:
            Returns true on success; otherwise, false.
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/group/{groupUUID}/user/{userUUID}/add')]

    ALL_PARAMS = {'userUUID', 'groupUUID'}
    REQUIRED_PARAMS = {'userUUID', 'groupUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'userUUID': str, 'groupUUID': str}

    RETURNS = {'success': bool}


class UpdateMetadata(Endpoint):

    """FCO REST API updateMetadata endpoint.

    This function will update the metadata attached to a resource.

    Remarks:
    On successful execution, true is returned. On an exception, the
    resource is not modified.

    Parameters (type name (required): description):
        str resourceUUID (T):
            The UUID of the resource to which the metadata to update
            belongs

    Data (type name (required): description):
        cobjects.ResourceMetadata resourceMetadata (T):
            The updated metadata to apply to the resource

    Returns (type name: description):
        bool success:
            Returns true on success; otherwise, false.
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/{resourceUUID}/metadata')]

    ALL_PARAMS = {'resourceUUID'}
    REQUIRED_PARAMS = {'resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'resourceUUID': str}

    ALL_DATA = {'resourceMetadata'}
    REQUIRED_DATA = {'resourceMetadata'}
    OPTIONAL_DATA = set()
    DATA_TYPES = {'resourceMetadata': cobjects.ResourceMetadata}

    RETURNS = {'success': bool}


class ModifyDisk(Endpoint):

    """FCO REST API modifyDisk endpoint.

    This function will modify a disk object.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not modified.

    Parameters (type name (required): description):
        str updatedResource.resourceUUID (T):
            The resourceUUID field of the referenced updatedResource
            object

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.Disk updatedResource (T):
            The disk object to be updated

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/disk/{updatedResource.resourceUUID}')]

    ALL_PARAMS = {'updatedResource.resourceUUID'}
    REQUIRED_PARAMS = {'updatedResource.resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'updatedResource.resourceUUID': str}

    ALL_DATA = {'when', 'updatedResource'}
    REQUIRED_DATA = {'updatedResource'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'updatedResource': cobjects.Disk}

    RETURNS = {'job': cobjects.Job}


class GetHypervisorConfig(Endpoint):

    """FCO REST API getHypervisorConfig endpoint.

    This function returns the hypervisor specific settings for a
    cluster.

    Parameters (type name (required): description):
        str clusterUUID (T):
            List of keys of the measured values sought

    Returns (type name: description):
        cobjects.MapHolder hypervisorConfig:
            A map of config keys to valid settings
    """

    ENDPOINTS = [(Verbs.GET,
                 'resources/cluster/{clusterUUID}/hypervisorconfig')]

    ALL_PARAMS = {'clusterUUID'}
    REQUIRED_PARAMS = {'clusterUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'clusterUUID': str}

    RETURNS = {'hypervisorConfig': cobjects.MapHolder}


class AddKey(Endpoint):

    """FCO REST API addKey endpoint.

    This function will add keys to the given resource object.

    Remarks:
    On successful execution, the resource object will be returned with
    the added key in it. On an exception, the key will not be added.

    Parameters (type name (required): description):
        str resourceUUID (T):
            The UUID of the resource object

    Data (type name (required): description):
        cobjects.ResourceKey resourceKey (T):
            The key object to be added to resource

    Returns (type name: description):
        cobjects.Resource resource:
            The resource object after adding the key
    """

    ENDPOINTS = [(Verbs.POST, 'resources/{resourceUUID}/key')]

    ALL_PARAMS = {'resourceUUID'}
    REQUIRED_PARAMS = {'resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'resourceUUID': str}

    ALL_DATA = {'resourceKey'}
    REQUIRED_DATA = {'resourceKey'}
    OPTIONAL_DATA = set()
    DATA_TYPES = {'resourceKey': cobjects.ResourceKey}

    RETURNS = {'resource': cobjects.Resource}


class CreateDisk(Endpoint):

    """FCO REST API createDisk endpoint.

    This function will create a disk, and optionally attach it to a
    server.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not created or attached.

    Data (type name (required): description):
        cobjects.FetchParameters fetchParameters (F):
            The parameters holding the url details
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.Disk skeletonDisk (T):
            The disk object to be created

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.POST, 'resources/disk')]

    ALL_DATA = {'fetchParameters', 'when', 'skeletonDisk'}
    REQUIRED_DATA = {'skeletonDisk'}
    OPTIONAL_DATA = {'fetchParameters', 'when'}
    DATA_TYPES = {'fetchParameters': cobjects.FetchParameters, 'when':
                  datetime, 'skeletonDisk': cobjects.Disk}

    RETURNS = {'job': cobjects.Job}


class ModifyKey(Endpoint):

    """FCO REST API modifyKey endpoint.

    This function will modify an existing resource key for a given
    resource object.

    Remarks:
    On successful execution, the resource object will be returned with
    the modified key object. On an exception, the key will not be
    modified

    Parameters (type name (required): description):
        str resourceUUID (T):
            The UUID of the resource which contains the key

    Data (type name (required): description):
        cobjects.ResourceKey resourceKey (T):
            The new value of the resource key object which needs to be
            modified

    Returns (type name: description):
        cobjects.VirtualResource resource:
            The resource object after modifying the key
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/{resourceUUID}/key')]

    ALL_PARAMS = {'resourceUUID'}
    REQUIRED_PARAMS = {'resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'resourceUUID': str}

    ALL_DATA = {'resourceKey'}
    REQUIRED_DATA = {'resourceKey'}
    OPTIONAL_DATA = set()
    DATA_TYPES = {'resourceKey': cobjects.ResourceKey}

    RETURNS = {'resource': cobjects.VirtualResource}


class RemoveFromFavourites(Endpoint):

    """FCO REST API removeFromFavourites endpoint.

    This function removes a resource on to the favourites list.

    Parameters (type name (required): description):
        enums.ResourceType resourceType (F):
            The resource type of the favorited resource
        str resourceUUID (T):
            The UUID of the resource

    Returns (type name: description):
        bool success:
            true if the specified resource is removed from the favorites
            list
    """

    ENDPOINTS = [(Verbs.DELETE,
                 'resources/{resourceType}/favourites/{resourceUUID}'),
                 (Verbs.DELETE, 'resources/favourites/{resourceUUID}')]

    ALL_PARAMS = {'resourceType', 'resourceUUID'}
    REQUIRED_PARAMS = {'resourceUUID'}
    OPTIONAL_PARAMS = {'resourceType'}
    PARAMS_TYPES = {'resourceType': enums.ResourceType, 'resourceUUID': str}

    RETURNS = {'success': bool}


class ModifyPluggableResource(Endpoint):

    """FCO REST API modifyPluggableResource endpoint.

    This function will start a job that will modify a Pluggable Resource
    and return the job reference.

    Remarks:
    If you do not specify a date for the when parameter the job will be
    started as soon as possible.

    Parameters (type name (required): description):
        str updatedResource.resourceUUID (T):
            The resourceUUID field of the referenced updatedResource
            object

    Data (type name (required): description):
        datetime when (F):
            The date/time in the future when the job will be started.
        cobjects.PluggableResource updatedResource (T):
            The modified pluggable resource

    Returns (type name: description):
        cobjects.Job job:
            The delete pluggable resource job.
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/pluggable_resource/{updatedResource.resourceUUID}')
                 ]

    ALL_PARAMS = {'updatedResource.resourceUUID'}
    REQUIRED_PARAMS = {'updatedResource.resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'updatedResource.resourceUUID': str}

    ALL_DATA = {'when', 'updatedResource'}
    REQUIRED_DATA = {'updatedResource'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'updatedResource':
                  cobjects.PluggableResource}

    RETURNS = {'job': cobjects.Job}


class DryRunTemplate(Endpoint):

    """FCO REST API dryRunTemplate endpoint.

    This function will do a dry run on the deployment instance to check
    if template can be deployed.

    Remarks:
    This function will return list of suggested references which can be
    used when optional references are not found.

    Data (type name (required): description):
        cobjects.DeploymentInstance skeletonDeploymentInstance (T):
            The instance of the template to be deployed
        datetime when (F):
            A date object specifying when the job is to be scheduled

    Returns (type name: description):
        cobjects.DryRunResult dryRunResult:
            Returns true on success and list of resolvable references
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/deployment_instance/dryrun')]

    ALL_DATA = {'skeletonDeploymentInstance', 'when'}
    REQUIRED_DATA = {'skeletonDeploymentInstance'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'skeletonDeploymentInstance': cobjects.DeploymentInstance,
                  'when': datetime}

    RETURNS = {'dryRunResult': cobjects.DryRunResult}


class LockUser(Endpoint):

    """FCO REST API lockUser endpoint.

    This function will move a user into the Locked group.

    Parameters (type name (required): description):
        str userUUID (T):
            The UUID of the user to lock

    Returns (type name: description):
        bool success:
            Returns true on success; otherwise, false.
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/user/{userUUID}/lock')]

    ALL_PARAMS = {'userUUID'}
    REQUIRED_PARAMS = {'userUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'userUUID': str}

    RETURNS = {'success': bool}


class IsPermitted(Endpoint):

    """FCO REST API isPermitted endpoint.

    This function will determine whether a specified action on a
    resource would be permitted.

    Parameters (type name (required): description):
        str resourceUUID (T):
            The UUID of the resource

    Data (type name (required): description):
        cobjects.Permission permission (T):
            The permission to test

    Returns (type name: description):
        bool permitted:
            Returns true if the action would be permitted, otherwise
            false
    """

    ENDPOINTS = [(Verbs.GET, 'resources/{resourceUUID}/permission/permitted')]

    ALL_PARAMS = {'resourceUUID'}
    REQUIRED_PARAMS = {'resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'resourceUUID': str}

    ALL_DATA = {'permission'}
    REQUIRED_DATA = {'permission'}
    OPTIONAL_DATA = set()
    DATA_TYPES = {'permission': cobjects.Permission}

    RETURNS = {'permitted': bool}


class DetachDisk(Endpoint):

    """FCO REST API detachDisk endpoint.

    This function will detach a disk from an existing server.

    Remarks:
    The server must not be running when the call is made. The call may
    be scheduled for a future date by setting the 'when' parameter. On
    successful execution, a Job object will be returned. On an
    exception, the resource is not detached.

    Parameters (type name (required): description):
        str serverUUID (T):
            The UUID of the server from which the disk to be detached
        str diskUUID (T):
            The UUID of the disk to be detached

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/server/{serverUUID}/disk/{diskUUID}/detach')]

    ALL_PARAMS = {'serverUUID', 'diskUUID'}
    REQUIRED_PARAMS = {'serverUUID', 'diskUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'serverUUID': str, 'diskUUID': str}

    ALL_DATA = {'when'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime}

    RETURNS = {'job': cobjects.Job}


class ModifyImage(Endpoint):

    """FCO REST API modifyImage endpoint.

    This function will modify an image.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not modified.

    Parameters (type name (required): description):
        str updatedResource.resourceUUID (T):
            The resourceUUID field of the referenced updatedResource
            object

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.Image updatedResource (T):
            The modified image

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/image/{updatedResource.resourceUUID}')]

    ALL_PARAMS = {'updatedResource.resourceUUID'}
    REQUIRED_PARAMS = {'updatedResource.resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'updatedResource.resourceUUID': str}

    ALL_DATA = {'when', 'updatedResource'}
    REQUIRED_DATA = {'updatedResource'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'updatedResource': cobjects.Image}

    RETURNS = {'job': cobjects.Job}


class CancelProductPurchase(Endpoint):

    """FCO REST API cancelProductPurchase endpoint.

    This function cancels an active purchase. This will only be
    applicable for UNIT purchaes.

    Remarks:
    On an exception, the product purchase is not updated.

    Parameters (type name (required): description):
        str purchaseUUID (T):
            The UUID of purchase

    Returns (type name: description):
        bool success:
            Returns true on success
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/product_purchase/{purchaseUUID}/cancel')]

    ALL_PARAMS = {'purchaseUUID'}
    REQUIRED_PARAMS = {'purchaseUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'purchaseUUID': str}

    RETURNS = {'success': bool}


class TestPaymentMethod(Endpoint):

    """FCO REST API testPaymentMethod endpoint.

    Tests a payment method.

    Parameters (type name (required): description):
        str paymentMethodUUID (T):
            The payment method to be tested

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled

    Returns (type name: description):
        cobjects.Job job:
            The job used to test the payment method.
    """

    ENDPOINTS = [(Verbs.GET,
                 'resource/payment_method/{paymentMethodUUID}/test')]

    ALL_PARAMS = {'paymentMethodUUID'}
    REQUIRED_PARAMS = {'paymentMethodUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'paymentMethodUUID': str}

    ALL_DATA = {'when'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime}

    RETURNS = {'job': cobjects.Job}


class ModifyDeploymentTemplate(Endpoint):

    """FCO REST API modifyDeploymentTemplate endpoint.

    This function will modify deployment template.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not modified.

    Parameters (type name (required): description):
        str updatedResource.resourceUUID (T):
            The resourceUUID field of the referenced updatedResource
            object

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.DeploymentTemplate updatedResource (T):
            The VDC object to be modified

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/deployment_template/{updatedResource.resourceUUID}'
                  )]

    ALL_PARAMS = {'updatedResource.resourceUUID'}
    REQUIRED_PARAMS = {'updatedResource.resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'updatedResource.resourceUUID': str}

    ALL_DATA = {'when', 'updatedResource'}
    REQUIRED_DATA = {'updatedResource'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'updatedResource':
                  cobjects.DeploymentTemplate}

    RETURNS = {'job': cobjects.Job}


class ListResources(Endpoint):

    """FCO REST API listResources endpoint.

    This function will return list of resources after satisfying a
    filter.

    Remarks:
    The resource types can be chosen from the ResourceType enum, the
    possible values of which are returned by the getResourceTypes call.
    Where no resource type is given, the resource type defaults to
    RESOURCE and all resource objects satisfying the filter; the
    resource objects are returned as simple resource objects in this
    case. If a specific resource type other than RESOURCE is specified,
    the objects returned are fully populated. On successful execution, a
    list of resource objects will be returned. On an exception, an empty
    list is returned.

    Parameters (type name (required): description):
        enums.ResourceType resourceType (F):
            The type of resources sought

    Data (type name (required): description):
        cobjects.SearchFilter searchFilter (F):
            A filter containing the conditions for search criteria
        cobjects.QueryLimit queryLimit (F):
            The limit on search

    Returns (type name: description):
        cobjects.ListResult resourcesList:
            The list of resources
    """

    ENDPOINTS = [(Verbs.GET, 'resources/{resourceType}/list'), (Verbs.POST,
                 'resources/{resourceType}/list'), (Verbs.GET,
                 'resources/list'), (Verbs.POST, 'resources/list')]

    ALL_PARAMS = {'resourceType'}
    REQUIRED_PARAMS = set()
    OPTIONAL_PARAMS = {'resourceType'}
    PARAMS_TYPES = {'resourceType': enums.ResourceType}

    ALL_DATA = {'searchFilter', 'queryLimit'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'searchFilter', 'queryLimit'}
    DATA_TYPES = {'searchFilter': cobjects.SearchFilter, 'queryLimit':
                  cobjects.QueryLimit}

    RETURNS = {'resourcesList': cobjects.ListResult}


class CreateNetwork(Endpoint):

    """FCO REST API createNetwork endpoint.

    This function will create a network.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not created.

    Data (type name (required): description):
        cobjects.Network skeletonNetwork (T):
            The network object to be created
        datetime when (F):
            A date object specifying when the job is to be scheduled

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.POST, 'resources/network')]

    ALL_DATA = {'skeletonNetwork', 'when'}
    REQUIRED_DATA = {'skeletonNetwork'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'skeletonNetwork': cobjects.Network, 'when': datetime}

    RETURNS = {'job': cobjects.Job}


class DetachNetworkInterface(Endpoint):

    """FCO REST API detachNetworkInterface endpoint.

    This function will detach a network interface from a given server.

    Remarks:
    The server must not be running when the call is made. The call may
    be scheduled for a future date by setting the 'when' parameter. On
    successful execution, a Job object will be returned. On an
    exception, the resource is not detached.

    Parameters (type name (required): description):
        str serverUUID (T):
            The UUID of the server from which the network interface is
            to be detached
        str nicUUID (T):
            The UUID of the network interface to be detached

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/server/{serverUUID}/nic/{nicUUID}/detach')]

    ALL_PARAMS = {'serverUUID', 'nicUUID'}
    REQUIRED_PARAMS = {'serverUUID', 'nicUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'serverUUID': str, 'nicUUID': str}

    ALL_DATA = {'when'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime}

    RETURNS = {'job': cobjects.Job}


class RenewAuthenticationToken(Endpoint):

    """FCO REST API renewAuthenticationToken endpoint.

    Manully renew an authentication trigger for the specified number of
    seconds.

    Remarks:
    If you do not specifiy the amount of time to renew the token for,
    the default timeout value will be used. You cannot renew an
    authentication token if the current session was authenticated with
    an authentication token. Any attempt to renew a token, including
    auto-renewal, which will result in it expiring earlier than the
    current expirey time will be ignored.

    Parameters (type name (required): description):
        str authToken (T):
            The authentication token to renew.

    Data (type name (required): description):
        int renew (F):
            The number of seconds from the current time to renew the
            token until.

    Returns (type name: description):
        bool success:
            True if the authentication token was renewed; otherwise,
            false.
    """

    ENDPOINTS = [(Verbs.PUT, 'authentication/{authToken}'), (Verbs.PUT,
                 'authentication')]

    ALL_PARAMS = {'authToken'}
    REQUIRED_PARAMS = {'authToken'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'authToken': str}

    ALL_DATA = {'renew'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'renew'}
    DATA_TYPES = {'renew': int}

    RETURNS = {'success': bool}


class DeleteAuthenticationToken(Endpoint):

    """FCO REST API deleteAuthenticationToken endpoint.

    Revoke API access when using the specified authentication token.

    Remarks:
    If you do not specify an authentication token to revoke, the
    authentication token used for the current session authentication
    will be revoked.

    Parameters (type name (required): description):
        str authToken (T):
            The authentication token to revoke.

    Returns (type name: description):
        bool success:
            True if the authentication token was revoked; otherwise,
            false.
    """

    ENDPOINTS = [(Verbs.DELETE, 'authentication/{authToken}'), (Verbs.DELETE,
                 'authentication')]

    ALL_PARAMS = {'authToken'}
    REQUIRED_PARAMS = {'authToken'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'authToken': str}

    RETURNS = {'success': bool}


class ModifySubnet(Endpoint):

    """FCO REST API modifySubnet endpoint.

    This function will modify a subnet.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not modified.

    Parameters (type name (required): description):
        str updatedResource.resourceUUID (T):
            The resourceUUID field of the referenced updatedResource
            object

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.Subnet updatedResource (T):
            The new value of the subnet to be modified

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/subnet/{updatedResource.resourceUUID}')]

    ALL_PARAMS = {'updatedResource.resourceUUID'}
    REQUIRED_PARAMS = {'updatedResource.resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'updatedResource.resourceUUID': str}

    ALL_DATA = {'when', 'updatedResource'}
    REQUIRED_DATA = {'updatedResource'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'updatedResource': cobjects.Subnet}

    RETURNS = {'job': cobjects.Job}


class CreatePluggableResource(Endpoint):

    """FCO REST API createPluggableResource endpoint.

    This function will start a job that will create a Pluggable Resource
    and return the job reference.

    Remarks:
    If you do not specify a date for the when parameter the job will be
    started as soon as possible.

    Data (type name (required): description):
        cobjects.PluggableResource skeletonResource (T):
            The modified pluggable resource
        datetime when (F):
            The date/time in the future when the job will be started.

    Returns (type name: description):
        cobjects.Job job:
            The delete pluggable resource job.
    """

    ENDPOINTS = [(Verbs.POST, 'resources/pluggable_resource')]

    ALL_DATA = {'skeletonResource', 'when'}
    REQUIRED_DATA = {'skeletonResource'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'skeletonResource': cobjects.PluggableResource, 'when':
                  datetime}

    RETURNS = {'job': cobjects.Job}


class ModifyGroup(Endpoint):

    """FCO REST API modifyGroup endpoint.

    This function will modify a group.

    Remarks:
    Note that this function is not intended for use to change the
    membership of a group. The call may be scheduled for a future date
    by setting the 'when' parameter. On successful execution, a Job
    object will be returned. On an exception, the resource is not
    modified.

    Parameters (type name (required): description):
        str updatedResource.resourceUUID (T):
            The resourceUUID field of the referenced updatedResource
            object

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.Group updatedResource (T):
            The group object to be updated

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/group/{updatedResource.resourceUUID}')]

    ALL_PARAMS = {'updatedResource.resourceUUID'}
    REQUIRED_PARAMS = {'updatedResource.resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'updatedResource.resourceUUID': str}

    ALL_DATA = {'when', 'updatedResource'}
    REQUIRED_DATA = {'updatedResource'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'updatedResource': cobjects.Group}

    RETURNS = {'job': cobjects.Job}


class CreateAPIKeyUser(Endpoint):

    """FCO REST API createAPIKeyUser endpoint.

    Create an API Key User for the current customer.

    Remarks:
    An API Key User is bound to the customer it is created for and
    cannot be moved to another customer, only deleted if no longer
    required. The supplied password can be supplied in plain text or
    hashed format, supported hash formats are: MD5, SHA, SHA256,
    htpasswd -m, htpasswd -s and mysql hashes. By default the password
    is assumed to be plain text unless the hashed parameter is set to
    true.

    Data (type name (required): description):
        cobjects.UserDetails skeletonUser (F):
            The skeleton User object.
        str password (T):
            The users password, either plain text or hashed.
        datetime when (F):
            A date object specifying when the job is to be scheduled
        bool hashed (F):
            State if the supplied password is a hashed value.

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job Object
    """

    ENDPOINTS = [(Verbs.POST, 'resources/user'), (Verbs.POST,
                 'resources/user/apikey')]

    ALL_DATA = {'skeletonUser', 'password', 'when', 'hashed'}
    REQUIRED_DATA = {'password'}
    OPTIONAL_DATA = {'skeletonUser', 'when', 'hashed'}
    DATA_TYPES = {'skeletonUser': cobjects.UserDetails, 'password': str,
                  'when': datetime, 'hashed': bool}

    RETURNS = {'job': cobjects.Job}


class ChangeServerStatus(Endpoint):

    """FCO REST API changeServerStatus endpoint.

    This function will change the state of (start, stop, kill or reboot)
    a server.

    Remarks:
    The 'safe' parameter when set will ensure that a clean shutdown is
    always performed. The call may be scheduled for a future date by
    setting the 'when' parameter. On successful execution, a Job object
    will be returned. On an exception, the resource is not modified.

    Parameters (type name (required): description):
        str serverUUID (T):
            The UUID of server for which the status needs to be changed

    Data (type name (required): description):
        enums.ServerStatus newStatus (T):
            The status to which server needs to be changed to
        datetime when (F):
            A date object specifying when the job is to be scheduled
        bool safe (T):
            A flag indicating whether the action can be performed safely
            or not
        cobjects.ResourceMetadata runtimeMetadata (F):
            The metadata to be used at runtime

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/server/{serverUUID}/change_status')]

    ALL_PARAMS = {'serverUUID'}
    REQUIRED_PARAMS = {'serverUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'serverUUID': str}

    ALL_DATA = {'newStatus', 'safe', 'when', 'runtimeMetadata'}
    REQUIRED_DATA = {'newStatus', 'safe'}
    OPTIONAL_DATA = {'runtimeMetadata', 'when'}
    DATA_TYPES = {'newStatus': enums.ServerStatus, 'safe': bool, 'when':
                  datetime, 'runtimeMetadata': cobjects.ResourceMetadata}

    RETURNS = {'job': cobjects.Job}


class CloneResource(Endpoint):

    """FCO REST API cloneResource endpoint.

    This function will clone a snapshot resource.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not cloned.

    Parameters (type name (required): description):
        str snapshotUUID (T):
            The UUID of the snapshot to clone

    Data (type name (required): description):
        str locationUUID (F):
            the UUID of the location to be used for the clone (e.g. a
            VDC)
        datetime when (F):
            A date object specifying when the job is to be scheduled
        str name (T):
            The name of the clone

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object.
    """

    ENDPOINTS = [(Verbs.POST, 'resources/snapshot/{snapshotUUID}/clone')]

    ALL_PARAMS = {'snapshotUUID'}
    REQUIRED_PARAMS = {'snapshotUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'snapshotUUID': str}

    ALL_DATA = {'locationUUID', 'when', 'name'}
    REQUIRED_DATA = {'name'}
    OPTIONAL_DATA = {'locationUUID', 'when'}
    DATA_TYPES = {'locationUUID': str, 'when': datetime, 'name': str}

    RETURNS = {'job': cobjects.Job}


class ListPermissions(Endpoint):

    """FCO REST API listPermissions endpoint.

    This function will fetch a list of permissions matching the
    specified filter conditions.

    Data (type name (required): description):
        cobjects.SearchFilter searchFilter (F):
            The filter to apply
        cobjects.QueryLimit queryLimit (F):
            The query limit to apply

    Returns (type name: description):
        cobjects.ListResult permissions:
            The list of permissions matching the filter
    """

    ENDPOINTS = [(Verbs.GET, 'resources/permission/list'), (Verbs.POST,
                 'resources/permission/list')]

    ALL_DATA = {'searchFilter', 'queryLimit'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'searchFilter', 'queryLimit'}
    DATA_TYPES = {'searchFilter': cobjects.SearchFilter, 'queryLimit':
                  cobjects.QueryLimit}

    RETURNS = {'permissions': cobjects.ListResult}


class CreateFirewallTemplate(Endpoint):

    """FCO REST API createFirewallTemplate endpoint.

    This function will create a firewall template.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not created.

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.FirewallTemplate skeletonFirewallTemplate (T):
            A skeleton of the firewall template object to be created

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.POST, 'resources/firewall_template')]

    ALL_DATA = {'when', 'skeletonFirewallTemplate'}
    REQUIRED_DATA = {'skeletonFirewallTemplate'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'skeletonFirewallTemplate':
                  cobjects.FirewallTemplate}

    RETURNS = {'job': cobjects.Job}


class SetPermissions(Endpoint):

    """FCO REST API setPermissions endpoint.

    This function will set the capabilities for the specified group or
    user on a specific resource.

    Remarks:
    All existing permissions are cleared. This call may be used to
    remove permissions by passing an empty list of permissions, or a
    copy of the existing list with one or more permissions removed.

    Parameters (type name (required): description):
        str resourceUUID (T):
            The UUID of the resource

    Data (type name (required): description):
        List(cobjects.Permission) permissions (T):
            The List of permissions to be applied for the resource

    Returns (type name: description):
        bool success:
            Returns true on success; otherwise, false.
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/{resourceUUID}/permission/set')]

    ALL_PARAMS = {'resourceUUID'}
    REQUIRED_PARAMS = {'resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'resourceUUID': str}

    ALL_DATA = {'permissions'}
    REQUIRED_DATA = {'permissions'}
    OPTIONAL_DATA = set()
    DATA_TYPES = {'permissions': List(cobjects.Permission)}

    RETURNS = {'success': bool}


class ModifyPaymentMethodInstance(Endpoint):

    """FCO REST API modifyPaymentMethodInstance endpoint.

    This function will modify a payment method instance.

    Remarks:
    This will only allow the default flag and the resource name to be
    modified. The call may be scheduled for a future date by setting the
    'when' parameter. On successful execution, a Job object will be
    returned. On an exception, the resource is not modified.

    Parameters (type name (required): description):
        str updatedResource.resourceUUID (T):
            The resourceUUID field of the referenced updatedResource
            object

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.PaymentMethodInstance updatedResource (T):
            The modified payment method instance

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/payment_method_instance/{updatedResource.resourceU'
                  'UID}')]

    ALL_PARAMS = {'updatedResource.resourceUUID'}
    REQUIRED_PARAMS = {'updatedResource.resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'updatedResource.resourceUUID': str}

    ALL_DATA = {'when', 'updatedResource'}
    REQUIRED_DATA = {'updatedResource'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'updatedResource':
                  cobjects.PaymentMethodInstance}

    RETURNS = {'job': cobjects.Job}


class ListUnitTransactionSummary(Endpoint):

    """FCO REST API listUnitTransactionSummary endpoint.

    This function will list the unit transaction summaries matching a
    given filter.

    Remarks:
    On successful execution, a list of unit transaction summaries will
    be returned. On an exception, an empty list is returned.

    Data (type name (required): description):
        cobjects.SearchFilter searchFilter (F):
            The filter to apply
        cobjects.QueryLimit queryLimit (F):
            The query limit for the filter

    Returns (type name: description):
        cobjects.ListResult listUnitTransactionSummary:
            The list of unit transactions
    """

    ENDPOINTS = [(Verbs.GET, 'resources/unit_transaction_summary/list'),
                 (Verbs.POST, 'resources/unit_transaction_summary/list')]

    ALL_DATA = {'searchFilter', 'queryLimit'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'searchFilter', 'queryLimit'}
    DATA_TYPES = {'searchFilter': cobjects.SearchFilter, 'queryLimit':
                  cobjects.QueryLimit}

    RETURNS = {'listUnitTransactionSummary': cobjects.ListResult}


class GetTranslationForUser(Endpoint):

    """FCO REST API getTranslationForUser endpoint.

    Get the Translation associated with the authenticed User.

    Data (type name (required): description):
        List(str) languageStrings (F):
            The language strings supplied by a browsers language detect.
            Each language must be a two character language code (EN) or
            the two character language code and two character region
            code, separated by a hyphen (EN-GB)

    Returns (type name: description):
        cobjects.Translation translation:
            The Translation associated with the User.
    """

    ENDPOINTS = [(Verbs.GET, 'resources/user/translation')]

    ALL_DATA = {'languageStrings'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'languageStrings'}
    DATA_TYPES = {'languageStrings': List(str)}

    RETURNS = {'translation': cobjects.Translation}


class DeleteResource(Endpoint):

    """FCO REST API deleteResource endpoint.

    This function will delete an existing resource object.

    Remarks:
    If cascade is set to true, a 'deep delete' is performed, and each of
    dependent child resource will be deleted. If cascade is false, an
    exception will be thrown if there are child objects. Note that jobs
    are deleted synchronously; deleting a job does not create another
    job. The call may be scheduled for a future date by setting the
    'when' parameter. On successful execution, a Job object will be
    returned. On an exception, the resource is not deleted.

    Parameters (type name (required): description):
        enums.ResourceType resourceType (F):
            The ResourceType of the resource object to be deleted
        str resourceUUID (T):
            The UUID of the resource object to be deleted

    Data (type name (required): description):
        bool cascade (F):
            A flag to determine whether a deep delete is required
        datetime when (F):
            A date object specifying when the job is to be scheduled

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.DELETE, 'resources/{resourceType}/{resourceUUID}'),
                 (Verbs.DELETE, 'resources/{resourceUUID}')]

    ALL_PARAMS = {'resourceType', 'resourceUUID'}
    REQUIRED_PARAMS = {'resourceUUID'}
    OPTIONAL_PARAMS = {'resourceType'}
    PARAMS_TYPES = {'resourceType': enums.ResourceType, 'resourceUUID': str}

    ALL_DATA = {'cascade', 'when'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'cascade', 'when'}
    DATA_TYPES = {'cascade': bool, 'when': datetime}

    RETURNS = {'job': cobjects.Job}


class CreateDeploymentTemplate(Endpoint):

    """FCO REST API createDeploymentTemplate endpoint.

    This function will create a deployment template object.

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.DeploymentTemplate skeletonDeploymentTemplate (T):
            The template object to create

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.POST, 'resources/deployment_template')]

    ALL_DATA = {'skeletonDeploymentTemplate', 'when'}
    REQUIRED_DATA = {'skeletonDeploymentTemplate'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'skeletonDeploymentTemplate':
                  cobjects.DeploymentTemplate}

    RETURNS = {'job': cobjects.Job}


class FetchResource(Endpoint):

    """FCO REST API fetchResource endpoint.

    This function will fetch a resource (such as a disk, image or
    server) over the internet, using the parameters supplied.

    Remarks:
    If the boolean parameter makeImage is set to true, then the call
    will create an image, else it will create a disk or a server,
    dependent upon the resource fetched and what the cluster supports.
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not created.

    Data (type name (required): description):
        int referenceSize (F):
            The size of the resource that you want to create in GB, if
            specified this need to be supported by the PO you have
            selected
        cobjects.FetchParameters fetchParameters (T):
            The parameters holding the url details
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.VirtualResource skeletonResource (T):
            A skeleton object containing details of the resource object
            to be created

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.GET, 'resources/fetch')]

    ALL_DATA = {'referenceSize', 'fetchParameters', 'when', 'skeletonResource'}
    REQUIRED_DATA = {'skeletonResource', 'fetchParameters'}
    OPTIONAL_DATA = {'referenceSize', 'when'}
    DATA_TYPES = {'referenceSize': int, 'fetchParameters':
                  cobjects.FetchParameters, 'when': datetime,
                  'skeletonResource': cobjects.VirtualResource}

    RETURNS = {'job': cobjects.Job}


class CreateVDC(Endpoint):

    """FCO REST API createVDC endpoint.

    This function will create a virtual data centre.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not created.

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.VDC skeletonVDC (T):
            A skeleton of the VDC object to be created

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.POST, 'resources/vdc')]

    ALL_DATA = {'when', 'skeletonVDC'}
    REQUIRED_DATA = {'skeletonVDC'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'skeletonVDC': cobjects.VDC}

    RETURNS = {'job': cobjects.Job}


class CreateSnapshot(Endpoint):

    """FCO REST API createSnapshot endpoint.

    This function will create a snapshot object from a disk or a server.

    Remarks:
    Whether a snapshot object can be created from a disk or a server
    will depend on the capabilities of the cluster containing the disk
    or the server concerned. The call may be scheduled for a future date
    by setting the 'when' parameter. On successful execution, a Job
    object will be returned. On an exception, the resource is not
    created.

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.Snapshot skeletonSnapshot (T):
            A skeleton of the snapshot object to be created

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.POST, 'resources/snapshot')]

    ALL_DATA = {'when', 'skeletonSnapshot'}
    REQUIRED_DATA = {'skeletonSnapshot'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'skeletonSnapshot': cobjects.Snapshot}

    RETURNS = {'job': cobjects.Job}


class CreateSubnet(Endpoint):

    """FCO REST API createSubnet endpoint.

    This function will create a subnet.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not created.

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.Subnet skeletonSubnet (T):
            A skeleton containing the subnet object to be created

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.POST, 'resources/subnet')]

    ALL_DATA = {'skeletonSubnet', 'when'}
    REQUIRED_DATA = {'skeletonSubnet'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'skeletonSubnet': cobjects.Subnet}

    RETURNS = {'job': cobjects.Job}


class AttachNetworkInterface(Endpoint):

    """FCO REST API attachNetworkInterface endpoint.

    This function will attach a network interface to a given server.

    Remarks:
    The server must not be running when the call is made. The index
    parameter is an integer specifying the position in the list of
    network interfaces that the network interface in question should
    take. When index is 0 network interface is added to the first
    position, only if no network interfaces are attached to the given
    server, otherwise is added in the last position. Other network
    interfaces will be shuffled around appropriately. The call may be
    scheduled for a future date by setting the 'when' parameter. On
    successful execution, a Job object will be returned. On an
    exception, the resource is not modified.

    Parameters (type name (required): description):
        str serverUUID (T):
            The UUID of server to which the network interface is to be
            attached
        str networkInterfaceUUID (T):
            The UUID of the network interface to be attached

    Data (type name (required): description):
        int index (T):
            The position in the list of network interfaces that the
            supplied interface is to take
        datetime when (F):
            A date object specifying when the job is to be scheduled

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/server/{serverUUID}/nic/{networkInterfaceUUID}/att'
                  'ach')]

    ALL_PARAMS = {'serverUUID', 'networkInterfaceUUID'}
    REQUIRED_PARAMS = {'serverUUID', 'networkInterfaceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'serverUUID': str, 'networkInterfaceUUID': str}

    ALL_DATA = {'index', 'when'}
    REQUIRED_DATA = {'index'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'index': int, 'when': datetime}

    RETURNS = {'job': cobjects.Job}


class AttachSubnet(Endpoint):

    """FCO REST API attachSubnet endpoint.

    This function will attach a subnet an existing network.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not attached.

    Parameters (type name (required): description):
        str networkUUID (T):
            The UUID of the network object
        str subnetUUID (T):
            The UUID of the subnet object

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/network/{networkUUID}/subnet/{subnetUUID}/attach')]

    ALL_PARAMS = {'networkUUID', 'subnetUUID'}
    REQUIRED_PARAMS = {'networkUUID', 'subnetUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'networkUUID': str, 'subnetUUID': str}

    ALL_DATA = {'when'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime}

    RETURNS = {'job': cobjects.Job}


class ListReferralPromoCode(Endpoint):

    """FCO REST API listReferralPromoCode endpoint.

    This function will return list of referral promocodes which meets
    the filter criteria.

    Data (type name (required): description):
        cobjects.SearchFilter searchFilter (F):
            The search filter to be used
        cobjects.QueryLimit queryLimit (F):
            The query limit to be used

    Returns (type name: description):
        cobjects.ListResult listReferralPromoCode:
            The list of ReferralPromoCode objects
    """

    ENDPOINTS = [(Verbs.GET, 'resources/referral_promocode/list'), (Verbs.POST,
                 'resources/referral_promocode/list')]

    ALL_DATA = {'searchFilter', 'queryLimit'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'searchFilter', 'queryLimit'}
    DATA_TYPES = {'searchFilter': cobjects.SearchFilter, 'queryLimit':
                  cobjects.QueryLimit}

    RETURNS = {'listReferralPromoCode': cobjects.ListResult}


class ResumeTransaction(Endpoint):

    """FCO REST API resumeTransaction endpoint.

    Resumes a transaction which was awaiting interactive input.

    Remarks:
    The configured values are not passed to this method as any required
    data should have been stored by Lua in the transaction. , type =
    COMMNT_TYPE.WSDL_DOC

    Parameters (type name (required): description):
        str transactionUUID (T):
            The transaction to be resumed

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled

    Returns (type name: description):
        cobjects.Job job:
            The job for the resumed transaction
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/transaction/{transactionUUID}/resume')]

    ALL_PARAMS = {'transactionUUID'}
    REQUIRED_PARAMS = {'transactionUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'transactionUUID': str}

    ALL_DATA = {'when'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime}

    RETURNS = {'job': cobjects.Job}


class CreateReferralPromoCode(Endpoint):

    """FCO REST API createReferralPromoCode endpoint.

    This function will return a the newly created Referral promocode
    Object.

    Remarks:
    On an exception, the referral promocode is not created.

    Data (type name (required): description):
        cobjects.ReferralPromoCode referralPromoCode (T):
            The ReferralPromoCode object that has to be created

    Returns (type name: description):
        cobjects.ReferralPromoCode referralPromoCode:
            The ReferralPromoCode object that has been created
    """

    ENDPOINTS = [(Verbs.POST, 'resources/referral_promocode')]

    ALL_DATA = {'referralPromoCode'}
    REQUIRED_DATA = {'referralPromoCode'}
    OPTIONAL_DATA = set()
    DATA_TYPES = {'referralPromoCode': cobjects.ReferralPromoCode}

    RETURNS = {'referralPromoCode': cobjects.ReferralPromoCode}


class ModifyServer(Endpoint):

    """FCO REST API modifyServer endpoint.

    This function will modify an existing server object.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not modified.

    Parameters (type name (required): description):
        str updatedResource.resourceUUID (T):
            The resourceUUID field of the referenced updatedResource
            object

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.Server updatedResource (T):
            The modified server object to be used

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/server/{updatedResource.resourceUUID}')]

    ALL_PARAMS = {'updatedResource.resourceUUID'}
    REQUIRED_PARAMS = {'updatedResource.resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'updatedResource.resourceUUID': str}

    ALL_DATA = {'when', 'updatedResource'}
    REQUIRED_DATA = {'updatedResource'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'updatedResource': cobjects.Server}

    RETURNS = {'job': cobjects.Job}


class ModifySSHKey(Endpoint):

    """FCO REST API modifySSHKey endpoint.

    This function will modify an ssh key.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not modified.

    Parameters (type name (required): description):
        str updatedSSHKey.resourceUUID (T):
            The resourceUUID field of the referenced updatedSSHKey
            object

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.SSHKey updatedSSHKey (T):
            sshKey to modify

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/sshkey/{updatedSSHKey.resourceUUID}')]

    ALL_PARAMS = {'updatedSSHKey.resourceUUID'}
    REQUIRED_PARAMS = {'updatedSSHKey.resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'updatedSSHKey.resourceUUID': str}

    ALL_DATA = {'when', 'updatedSSHKey'}
    REQUIRED_DATA = {'updatedSSHKey'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'updatedSSHKey': cobjects.SSHKey}

    RETURNS = {'job': cobjects.Job}


class OpenVNCConnection(Endpoint):

    """FCO REST API openVNCConnection endpoint.

    This function will open virtual network connection for a given
    server.

    Remarks:
    On successful execution, the VNC Connection object is returned, and
    a connection can be opened at any point in an interval configurable
    by the licensee. On an exception, the connection will not be opened

    Parameters (type name (required): description):
        str serverUUID (T):
            The UUID of server to which connection needs to be opened

    Data (type name (required): description):
        enums.VNCHandler handlerType (T):
            The type of connection being requested

    Returns (type name: description):
        cobjects.VNCConnection vncConnection:
            The VNC connection object
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/server/{serverUUID}/vnc/open')]

    ALL_PARAMS = {'serverUUID'}
    REQUIRED_PARAMS = {'serverUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'serverUUID': str}

    ALL_DATA = {'handlerType'}
    REQUIRED_DATA = {'handlerType'}
    OPTIONAL_DATA = set()
    DATA_TYPES = {'handlerType': enums.VNCHandler}

    RETURNS = {'vncConnection': cobjects.VNCConnection}


class CreateSSHKey(Endpoint):

    """FCO REST API createSSHKey endpoint.

    This function will create an ssh key.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not modified.

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.SSHKey skeletonSSHKey (T):
            The ssh key to be created

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.POST, 'resources/sshkey')]

    ALL_DATA = {'skeletonSSHKey', 'when'}
    REQUIRED_DATA = {'skeletonSSHKey'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'skeletonSSHKey': cobjects.SSHKey}

    RETURNS = {'job': cobjects.Job}


class RenderInvoice(Endpoint):

    """FCO REST API renderInvoice endpoint.

    This function will return Invoice/Credit note PDF in Base64 format
    or in HTML fromat.

    Parameters (type name (required): description):
        str invoiceUUID (T):
            The Invoice/Credit note to be rendered
        str renderingType (T):
            The type of rendring required, base64 or html are the two
            supported formats

    Returns (type name: description):
        str invoicePDF:
            The Invoice/Credit note PDF in Base64 or HTML fromat format
    """

    ENDPOINTS = [(Verbs.GET,
                 'resources/invoice/{invoiceUUID}/render_pdf/{renderingType}')]

    ALL_PARAMS = {'invoiceUUID', 'renderingType'}
    REQUIRED_PARAMS = {'invoiceUUID', 'renderingType'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'invoiceUUID': str, 'renderingType': str}

    RETURNS = {'invoicePDF': str}


class ModifyBlob(Endpoint):

    """FCO REST API modifyBlob endpoint.

    This function will modify the a blob.

    Remarks:
    On successful execution it will return the modified blob.

    Parameters (type name (required): description):
        str blob.resourceUUID (T):
            The resourceUUID field of the referenced blob object

    Data (type name (required): description):
        cobjects.Blob blob (T):
            The blob to be modified

    Returns (type name: description):
        cobjects.Blob updatedBlob:
            The modified blob.
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/blob/{blob.resourceUUID}')]

    ALL_PARAMS = {'blob.resourceUUID'}
    REQUIRED_PARAMS = {'blob.resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'blob.resourceUUID': str}

    ALL_DATA = {'blob'}
    REQUIRED_DATA = {'blob'}
    OPTIONAL_DATA = set()
    DATA_TYPES = {'blob': cobjects.Blob}

    RETURNS = {'updatedBlob': cobjects.Blob}


class UpdateCustomer(Endpoint):

    """FCO REST API updateCustomer endpoint.

    This function will update an existing customer using the supplied
    fields and return the updated customer object.

    Remarks:
    On an exception, the customer object is not updated and no customer
    object is returned.

    Parameters (type name (required): description):
        str customerDetails.resourceUUID (T):
            The resourceUUID field of the referenced customerDetails
            object

    Data (type name (required): description):
        cobjects.CustomerDetails customerDetails (T):
            The customer details object with which to update the
            customer

    Returns (type name: description):
        cobjects.CustomerDetails customer:
            The updated customer details object
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/customer/{customerDetails.resourceUUID}')]

    ALL_PARAMS = {'customerDetails.resourceUUID'}
    REQUIRED_PARAMS = {'customerDetails.resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'customerDetails.resourceUUID': str}

    ALL_DATA = {'customerDetails'}
    REQUIRED_DATA = {'customerDetails'}
    OPTIONAL_DATA = set()
    DATA_TYPES = {'customerDetails': cobjects.CustomerDetails}

    RETURNS = {'customer': cobjects.CustomerDetails}


class RemoveKey(Endpoint):

    """FCO REST API removeKey endpoint.

    This function will remove keys from the given resource object.

    Remarks:
    On successful execution, the resource object is returned with the
    given key removed. On an exception, the key will not be removed from
    Resource.

    Parameters (type name (required): description):
        str resourceUUID (T):
            The UUID object of the resource object from which key is to
            be removed

    Data (type name (required): description):
        cobjects.ResourceKey resourceKey (T):
            The resource key object which needs to be removed

    Returns (type name: description):
        cobjects.Resource resource:
            The resource object after removing the key
    """

    ENDPOINTS = [(Verbs.DELETE, 'resources/{resourceUUID}/key')]

    ALL_PARAMS = {'resourceUUID'}
    REQUIRED_PARAMS = {'resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'resourceUUID': str}

    ALL_DATA = {'resourceKey'}
    REQUIRED_DATA = {'resourceKey'}
    OPTIONAL_DATA = set()
    DATA_TYPES = {'resourceKey': cobjects.ResourceKey}

    RETURNS = {'resource': cobjects.Resource}


class GetBlobContent(Endpoint):

    """FCO REST API getBlobContent endpoint.

    This function will return blob content for a given blob.

    Parameters (type name (required): description):
        str blobUUID (T):
            The UUID of the blob

    Returns (type name: description):
        str blobValue:
            The content of the blob
    """

    ENDPOINTS = [(Verbs.GET, 'resources/blob/{blobUUID}/content')]

    ALL_PARAMS = {'blobUUID'}
    REQUIRED_PARAMS = {'blobUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'blobUUID': str}

    RETURNS = {'blobValue': str}


class WaitForJob(Endpoint):

    """FCO REST API waitForJob endpoint.

    This function will wait for a job to complete.

    Remarks:
    On successful execution, a Job object will be returned. On an
    exception, the wait is not completed.

    Parameters (type name (required): description):
        str jobUUID (T):
            The UUID of the job to to wait for

    Data (type name (required): description):
        bool noWaitForChildren (T):
            A boolean flag which indicates whether the caller wants to
            wait only for the job specified (if the flag is true) or to
            wait until both the job specified and all of its child jobs
            have completed (if the flag is false). The default is false,
            indicating that the call will wait until the job and all its
            child jobs have completed.

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.GET, 'resources/job/{jobUUID}/wait')]

    ALL_PARAMS = {'jobUUID'}
    REQUIRED_PARAMS = {'jobUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'jobUUID': str}

    ALL_DATA = {'noWaitForChildren'}
    REQUIRED_DATA = {'noWaitForChildren'}
    OPTIONAL_DATA = set()
    DATA_TYPES = {'noWaitForChildren': bool}

    RETURNS = {'job': cobjects.Job}


class ModifyDeploymentInstance(Endpoint):

    """FCO REST API modifyDeploymentInstance endpoint.

    This function will modify deployment instance.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not modified.

    Parameters (type name (required): description):
        str updatedResource.resourceUUID (T):
            The resourceUUID field of the referenced updatedResource
            object

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.DeploymentInstance updatedResource (T):
            The VDC object to be modified

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/deployment_instance/{updatedResource.resourceUUID}'
                  )]

    ALL_PARAMS = {'updatedResource.resourceUUID'}
    REQUIRED_PARAMS = {'updatedResource.resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'updatedResource.resourceUUID': str}

    ALL_DATA = {'when', 'updatedResource'}
    REQUIRED_DATA = {'updatedResource'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'updatedResource':
                  cobjects.DeploymentInstance}

    RETURNS = {'job': cobjects.Job}


class InvokeAction(Endpoint):

    """FCO REST API invokeAction endpoint.

    This function will start a job that will invoke an action for a
    resouce.

    Remarks:
    Actions created by configuration provider you must specify the
    product component type uuid If you do not specify a date for the
    when parameter the job will be started as soon as possible.

    Parameters (type name (required): description):
        str resourceUUID (T):
            The UUID of the resource using the config provider
        str actionKey (T):
            The key of the action to invoke

    Data (type name (required): description):
        str pctUUID (T):
            The UUID of the product component type
        datetime when (F):
            The date/time in the future when the job will be started.
        Dict(str, str) inputParameters (T):
            The required input parameters for the action

    Returns (type name: description):
        cobjects.Job job:
            The invoke pluggable resource job.
    """

    ENDPOINTS = [(Verbs.POST,
                 'resources/{resourceUUID}/action/{actionKey}/invoke'),
                 (Verbs.POST, 'resources/{resourceUUID}/action/invoke')]

    ALL_PARAMS = {'resourceUUID', 'actionKey'}
    REQUIRED_PARAMS = {'resourceUUID', 'actionKey'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'resourceUUID': str, 'actionKey': str}

    ALL_DATA = {'pctUUID', 'when', 'inputParameters'}
    REQUIRED_DATA = {'pctUUID', 'inputParameters'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'pctUUID': str, 'when': datetime, 'inputParameters':
                  Dict(str, str)}

    RETURNS = {'job': cobjects.Job}


class CreateDeploymentTemplateFromInstance(Endpoint):

    """FCO REST API createDeploymentTemplateFromInstance endpoint.

    This function will create deployment template from deployment
    instance.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the template is not created.

    Parameters (type name (required): description):
        str instanceUUID (T):
            The UUID of instance to be saved as a deployment template

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.POST,
                 'resources/deployment_instance/{instanceUUID}/create_template'
                  )]

    ALL_PARAMS = {'instanceUUID'}
    REQUIRED_PARAMS = {'instanceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'instanceUUID': str}

    ALL_DATA = {'when'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime}

    RETURNS = {'job': cobjects.Job}


class ModifyFirewall(Endpoint):

    """FCO REST API modifyFirewall endpoint.

    This function will modify a firewall.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not modified.

    Parameters (type name (required): description):
        str updatedResource.resourceUUID (T):
            The resourceUUID field of the referenced updatedResource
            object

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.Firewall updatedResource (T):
            The modified firewall object

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/firewall/{updatedResource.resourceUUID}')]

    ALL_PARAMS = {'updatedResource.resourceUUID'}
    REQUIRED_PARAMS = {'updatedResource.resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'updatedResource.resourceUUID': str}

    ALL_DATA = {'when', 'updatedResource'}
    REQUIRED_DATA = {'updatedResource'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'updatedResource': cobjects.Firewall}

    RETURNS = {'job': cobjects.Job}


class ModifyFirewallTemplate(Endpoint):

    """FCO REST API modifyFirewallTemplate endpoint.

    This function will modify a firewall template.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not modified.

    Parameters (type name (required): description):
        str updatedResource.resourceUUID (T):
            The resourceUUID field of the referenced updatedResource
            object

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.FirewallTemplate updatedResource (T):
            The modified firewall template

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/firewall_template/{updatedResource.resourceUUID}')]

    ALL_PARAMS = {'updatedResource.resourceUUID'}
    REQUIRED_PARAMS = {'updatedResource.resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'updatedResource.resourceUUID': str}

    ALL_DATA = {'when', 'updatedResource'}
    REQUIRED_DATA = {'updatedResource'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'updatedResource':
                  cobjects.FirewallTemplate}

    RETURNS = {'job': cobjects.Job}


class ListUnitTransactions(Endpoint):

    """FCO REST API listUnitTransactions endpoint.

    This function will list the unit transactions matching a given
    filter.

    Remarks:
    On successful execution, a list of unit transactions will be
    returned. On an exception, an empty list is returned.

    Data (type name (required): description):
        cobjects.SearchFilter searchFilter (F):
            The filter to apply
        cobjects.QueryLimit queryLimit (F):
            The query limit for the filter

    Returns (type name: description):
        cobjects.ListResult listUnitTransaction:
            The list of unit transactions
    """

    ENDPOINTS = [(Verbs.GET, 'resources/unit_transaction/list'), (Verbs.POST,
                 'resources/unit_transaction/list')]

    ALL_DATA = {'searchFilter', 'queryLimit'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'searchFilter', 'queryLimit'}
    DATA_TYPES = {'searchFilter': cobjects.SearchFilter, 'queryLimit':
                  cobjects.QueryLimit}

    RETURNS = {'listUnitTransaction': cobjects.ListResult}


class ModifyVDC(Endpoint):

    """FCO REST API modifyVDC endpoint.

    This function will modify virtual data centre.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not modified.

    Parameters (type name (required): description):
        str updatedResource.resourceUUID (T):
            The resourceUUID field of the referenced updatedResource
            object

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.VDC updatedResource (T):
            The VDC object to be modified

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/vdc/{updatedResource.resourceUUID}')]

    ALL_PARAMS = {'updatedResource.resourceUUID'}
    REQUIRED_PARAMS = {'updatedResource.resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'updatedResource.resourceUUID': str}

    ALL_DATA = {'when', 'updatedResource'}
    REQUIRED_DATA = {'updatedResource'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'updatedResource': cobjects.VDC}

    RETURNS = {'job': cobjects.Job}


class ListFavourites(Endpoint):

    """FCO REST API listFavourites endpoint.

    This function list current user's favourites list. Optionally can be
    filtered by resource type.

    Parameters (type name (required): description):
        enums.ResourceType resourceType (F):
            The optional resource type to filter by

    Returns (type name: description):
        cobjects.ListResult favorites:
            A ListResult of favorited resources as simple resources
    """

    ENDPOINTS = [(Verbs.GET, 'resources/{resourceType}/favourites'),
                 (Verbs.GET, 'resources/favourites')]

    ALL_PARAMS = {'resourceType'}
    REQUIRED_PARAMS = set()
    OPTIONAL_PARAMS = {'resourceType'}
    PARAMS_TYPES = {'resourceType': enums.ResourceType}

    RETURNS = {'favorites': cobjects.ListResult}


class ModifySnapshot(Endpoint):

    """FCO REST API modifySnapshot endpoint.

    This function will modify an existing snapshot.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not modified.

    Parameters (type name (required): description):
        str updatedResource.resourceUUID (T):
            The resourceUUID field of the referenced updatedResource
            object

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.Snapshot updatedResource (T):
            The updated snapshot object

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/snapshot/{updatedResource.resourceUUID}')]

    ALL_PARAMS = {'updatedResource.resourceUUID'}
    REQUIRED_PARAMS = {'updatedResource.resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'updatedResource.resourceUUID': str}

    ALL_DATA = {'when', 'updatedResource'}
    REQUIRED_DATA = {'updatedResource'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'updatedResource': cobjects.Snapshot}

    RETURNS = {'job': cobjects.Job}


class ModifyResource(Endpoint):

    """FCO REST API modifyResource endpoint.

    This function will modify an existing resource object.

    Remarks:
    A new object is passed in which forms the basis of the modified
    object. The call may be scheduled for a future date by setting the
    'when' parameter. On successful execution, a Job object will be
    returned. On an exception, the resource is not modified.

    Parameters (type name (required): description):
        str updatedResource.resourceUUID (T):
            The resourceUUID field of the referenced updatedResource
            object

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.VirtualResource updatedResource (T):
            The updated resource object

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/{updatedResource.resourceUUID}')]

    ALL_PARAMS = {'updatedResource.resourceUUID'}
    REQUIRED_PARAMS = {'updatedResource.resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'updatedResource.resourceUUID': str}

    ALL_DATA = {'when', 'updatedResource'}
    REQUIRED_DATA = {'updatedResource'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'updatedResource':
                  cobjects.VirtualResource}

    RETURNS = {'job': cobjects.Job}


class FetchDisk(Endpoint):

    """FCO REST API fetchDisk endpoint.

    This function will fetch a disk over the internet, using the
    parameters supplied.

    Remarks:
    If the boolean parameter makeImage is set to true, then the call
    will create an image, else it will create a disk dependent upon the
    resource fetched and what the cluster supports. The call may be
    scheduled for a future date by setting the 'when' parameter. On
    successful execution, a Job object will be returned. On an
    exception, the resource is not created.

    Data (type name (required): description):
        cobjects.FetchParameters fetchParameters (T):
            The parameters holding the url details
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.Disk skeletonDisk (T):
            A skeleton object containing details of the resource object
            to be created

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.GET, 'resources/fetch/disk')]

    ALL_DATA = {'fetchParameters', 'when', 'skeletonDisk'}
    REQUIRED_DATA = {'fetchParameters', 'skeletonDisk'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'fetchParameters': cobjects.FetchParameters, 'when':
                  datetime, 'skeletonDisk': cobjects.Disk}

    RETURNS = {'job': cobjects.Job}


class SetUserKeys(Endpoint):

    """FCO REST API setUserKeys endpoint.

    This Operation will add a set of resource keys of user type to the
    given resource.

    Parameters (type name (required): description):
        str resourceUUID (T):
            The UUID of the resource

    Data (type name (required): description):
        cobjects.KeyList keyList (T):
            The Map consisting of namespace as key and list of values

    Returns (type name: description):
        cobjects.Resource resource:
            Returns resource on success
    """

    ENDPOINTS = [(Verbs.POST, 'resources/{resourceUUID}/keys')]

    ALL_PARAMS = {'resourceUUID'}
    REQUIRED_PARAMS = {'resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'resourceUUID': str}

    ALL_DATA = {'keyList'}
    REQUIRED_DATA = {'keyList'}
    OPTIONAL_DATA = set()
    DATA_TYPES = {'keyList': cobjects.KeyList}

    RETURNS = {'resource': cobjects.Resource}


class CancelJob(Endpoint):

    """FCO REST API cancelJob endpoint.

    This function will cancel a job.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the job is not cancelled.

    Parameters (type name (required): description):
        str JobUUID (T):
            The UUID of the job which is to be cancelled

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/job/{JobUUID}/cancel')]

    ALL_PARAMS = {'JobUUID'}
    REQUIRED_PARAMS = {'JobUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'JobUUID': str}

    RETURNS = {'job': cobjects.Job}


class UnlockUser(Endpoint):

    """FCO REST API unlockUser endpoint.

    This function will remove a user from the Locked group.

    Parameters (type name (required): description):
        str userUUID (T):
            The UUID of the user to unlock

    Returns (type name: description):
        bool success:
            Returns true on success; otherwise, false.
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/user/{userUUID}/unlock')]

    ALL_PARAMS = {'userUUID'}
    REQUIRED_PARAMS = {'userUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'userUUID': str}

    RETURNS = {'success': bool}


class AddToFavourites(Endpoint):

    """FCO REST API addToFavourites endpoint.

    This function adds a resource on to the favourites list.

    Parameters (type name (required): description):
        enums.ResourceType resourceType (F):
            The resource type of the favorited resource
        str resourceUUID (T):
            The UUID of the resource

    Returns (type name: description):
        cobjects.SimpleResource resource:
            A SimpleResource representation of the newly favorited
            resource.
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/{resourceType}/favourites/{resourceUUID}'),
                 (Verbs.PUT, 'resources/favourites/{resourceUUID}'),
                 (Verbs.PUT, 'resources/favourites')]

    ALL_PARAMS = {'resourceType', 'resourceUUID'}
    REQUIRED_PARAMS = {'resourceUUID'}
    OPTIONAL_PARAMS = {'resourceType'}
    PARAMS_TYPES = {'resourceType': enums.ResourceType, 'resourceUUID': str}

    RETURNS = {'resource': cobjects.SimpleResource}


class ListProductPurchases(Endpoint):

    """FCO REST API listProductPurchases endpoint.

    This function will list the product purchases matching a given
    filter.

    Remarks:
    On successful execution, a list of product purchases will be
    returned. On an exception, an empty list is returned.

    Data (type name (required): description):
        cobjects.SearchFilter searchFilter (F):
            The filter to apply
        cobjects.QueryLimit queryLimit (F):
            The query limit to apply

    Returns (type name: description):
        cobjects.ListResult listProductPurchases:
            The list of matching product purchases
    """

    ENDPOINTS = [(Verbs.GET, 'resources/product_purchase/list'), (Verbs.POST,
                 'resources/product_purchase/list')]

    ALL_DATA = {'searchFilter', 'queryLimit'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'searchFilter', 'queryLimit'}
    DATA_TYPES = {'searchFilter': cobjects.SearchFilter, 'queryLimit':
                  cobjects.QueryLimit}

    RETURNS = {'listProductPurchases': cobjects.ListResult}


class PublishResource(Endpoint):

    """FCO REST API publishResource endpoint.

    This function will publish an image to a Customer or a Billing
    Entity.

    Parameters (type name (required): description):
        str resourceUUID (T):
            The UUID of the resource to publish

    Data (type name (required): description):
        bool exclude (F):
            To exclude/include the publishTo
        str publishTo (T):
            The UUID of the customer or billing entity to publish to

    Returns (type name: description):
        bool success:
            Returns true on success; otherwise, false.
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/{resourceUUID}/publish')]

    ALL_PARAMS = {'resourceUUID'}
    REQUIRED_PARAMS = {'resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'resourceUUID': str}

    ALL_DATA = {'exclude', 'publishTo'}
    REQUIRED_DATA = {'publishTo'}
    OPTIONAL_DATA = {'exclude'}
    DATA_TYPES = {'exclude': bool, 'publishTo': str}

    RETURNS = {'success': bool}


class DoQuery(Endpoint):

    """FCO REST API doQuery endpoint.

    This function will query the database, aggregating and grouping
    results if relevant.

    Remarks:
    Queries may only be made on a particular resource type; resource
    type for this purposes includes pseudo-resources such as unit
    transactions, unit transaction summaries, products, and product
    purchases. The call takes a Query object which specifies the query
    to be made, and returns a QueryResult object. See the documentation
    for the Query and QueryResult objects for more details. On
    successful execution, a QueryResult will be returned. On an
    exception, the no QueryResult is returned.

    Data (type name (required): description):
        cobjects.Query query (T):
            The parameters of the query

    Returns (type name: description):
        cobjects.QueryResult queryResult:
            The result of the query
    """

    ENDPOINTS = [(Verbs.GET, 'do_query'), (Verbs.PUT, 'do_query')]

    ALL_DATA = {'query'}
    REQUIRED_DATA = {'query'}
    OPTIONAL_DATA = set()
    DATA_TYPES = {'query': cobjects.Query}

    RETURNS = {'queryResult': cobjects.QueryResult}


class RemoveIP(Endpoint):

    """FCO REST API removeIP endpoint.

    This function will remove an IP address from a network interface.

    Remarks:
    Note that you can only remove IPv4 addresses from network
    interfaces; IPv6 addresses are permanently assigned. Removing an IP
    address from the NIC will result in any firewall associated with
    that IP address getting removed as well. Please note: if the network
    interface is linked to a IP network, removing the IP address of the
    NIC will mean that you will lose the IP address concerned. The call
    may be scheduled for a future date by setting the 'when' parameter.
    On successful execution, a Job object will be returned. On an
    exception, the resource is not modified.

    Parameters (type name (required): description):
        str networkInterfaceUUID (T):
            The UUID of the network interface
        str ipAddress (T):
            The IP address to be removed

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/nic/{networkInterfaceUUID}/ip_address/{ipAddress}/'
                  'remove')]

    ALL_PARAMS = {'networkInterfaceUUID', 'ipAddress'}
    REQUIRED_PARAMS = {'networkInterfaceUUID', 'ipAddress'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'networkInterfaceUUID': str, 'ipAddress': str}

    ALL_DATA = {'when'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime}

    RETURNS = {'job': cobjects.Job}


class CreatePaymentMethodInstance(Endpoint):

    """FCO REST API createPaymentMethodInstance endpoint.

    Creates a payment method instance.

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        List(cobjects.Value) configuredValues (F):
            A list of configuration values for the payment method
        str interactiveInputReturnURL (F):
            The URL for interactive input return
        bool allowInteractive (T):
            Indicates whether callbacks may be used by this payment
            method instance for 3DS transactions
        cobjects.PaymentMethodInstance paymentMethodInstance (T):
            A skeleton payment method instance

    Returns (type name: description):
        cobjects.Job job:
            A job representing the creation of the payment method
            instance
    """

    ENDPOINTS = [(Verbs.POST, 'resources/payment_method_instance')]

    ALL_DATA = {'interactiveInputReturnURL', 'configuredValues', 'when',
                'allowInteractive', 'paymentMethodInstance'}
    REQUIRED_DATA = {'allowInteractive', 'paymentMethodInstance'}
    OPTIONAL_DATA = {'when', 'configuredValues', 'interactiveInputReturnURL'}
    DATA_TYPES = {'when': datetime, 'configuredValues': List(cobjects.Value),
                  'interactiveInputReturnURL': str, 'allowInteractive': bool,
                  'paymentMethodInstance': cobjects.PaymentMethodInstance}

    RETURNS = {'job': cobjects.Job}


class ListResourceKeysForResource(Endpoint):

    """FCO REST API listResourceKeysForResource endpoint.

    List the resource keys for the given resource.

    Remarks:
    You will only be able to list resource keys for the current user or
    resources owned by the current customer.

    Parameters (type name (required): description):
        str resourceUUID (T):
            The UUID of the required resource.

    Returns (type name: description):
        cobjects.ListResult resourceKeys:
            A list of resource keys for the given resource.
    """

    ENDPOINTS = [(Verbs.GET, 'resources/{resourceUUID}/key')]

    ALL_PARAMS = {'resourceUUID'}
    REQUIRED_PARAMS = {'resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'resourceUUID': str}

    RETURNS = {'resourceKeys': cobjects.ListResult}


class CheckPermissions(Endpoint):

    """FCO REST API checkPermissions endpoint.

    This function will determine whether the specified actions would be
    permitted for a resource.

    Parameters (type name (required): description):
        str resourceUUID (T):
            The UUID of the resource.

    Data (type name (required): description):
        List(cobjects.CapabilityAction) capabilityActions (T):
            A list of CapablityAction object to check against the
            resource.

    Returns (type name: description):
        cobjects.MapHolder permissions:
            A map of the supplied CapabilityAction objects to the
            Boolean result stating if the supplied resource has access.
    """

    ENDPOINTS = [(Verbs.GET,
                 'resources/{resourceUUID}/permission/permitted/list')]

    ALL_PARAMS = {'resourceUUID'}
    REQUIRED_PARAMS = {'resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'resourceUUID': str}

    ALL_DATA = {'capabilityActions'}
    REQUIRED_DATA = {'capabilityActions'}
    OPTIONAL_DATA = set()
    DATA_TYPES = {'capabilityActions': List(cobjects.CapabilityAction)}

    RETURNS = {'permissions': cobjects.MapHolder}


class GetAuthenticationToken(Endpoint):

    """FCO REST API getAuthenticationToken endpoint.

    Gets an API authentication token for the currently authenticated
    user/customer combination.

    Data (type name (required): description):
        bool automaticallyRenew (F):
            true if the token will automatically renew when used;
            otherwise, false.
        int expiry (F):
            The number of seconds from the time of creation that the
            token will expire.

    Returns (type name: description):
        cobjects.AuthenticationToken authToken:
            The authentication token for the specified user/customer
            combination.
    """

    ENDPOINTS = [(Verbs.GET, 'authentication')]

    ALL_DATA = {'automaticallyRenew', 'expiry'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'automaticallyRenew', 'expiry'}
    DATA_TYPES = {'automaticallyRenew': bool, 'expiry': int}

    RETURNS = {'authToken': cobjects.AuthenticationToken}


class InvokeReportMethod(Endpoint):

    """FCO REST API invokeReportMethod endpoint.

    Generate a report using the specified report method and input
    values.

    Parameters (type name (required): description):
        str reportMethodUUID (T):
            The UUID of the required report method.

    Data (type name (required): description):
        List(cobjects.Value) inputValues (T):
            The configured input values.

    Returns (type name: description):
        str reportData:
            The generated report data.
    """

    ENDPOINTS = [(Verbs.POST,
                 'resources/report_method/{reportMethodUUID}/invoke'),
                 (Verbs.GET,
                 'resources/report_method/{reportMethodUUID}/invoke')]

    ALL_PARAMS = {'reportMethodUUID'}
    REQUIRED_PARAMS = {'reportMethodUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'reportMethodUUID': str}

    ALL_DATA = {'inputValues'}
    REQUIRED_DATA = {'inputValues'}
    OPTIONAL_DATA = set()
    DATA_TYPES = {'inputValues': List(cobjects.Value)}

    RETURNS = {'reportData': str}


class RevokeImage(Endpoint):

    """FCO REST API revokeImage endpoint.

    This function will revoke the publication of an image to a Customer
    or Billing Entity.

    Parameters (type name (required): description):
        str imageUUID (T):
            The UUID of the image to revoke

    Data (type name (required): description):
        bool exclude (F):
            To exclude/include the publishTo
        str publishTo (T):
            The UUID of the customer or billing from which publication
            should be revoked

    Returns (type name: description):
        bool success:
            Returns true on success; otherwise, false.
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/image/{imageUUID}/revoke')]

    ALL_PARAMS = {'imageUUID'}
    REQUIRED_PARAMS = {'imageUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'imageUUID': str}

    ALL_DATA = {'exclude', 'publishTo'}
    REQUIRED_DATA = {'publishTo'}
    OPTIONAL_DATA = {'exclude'}
    DATA_TYPES = {'exclude': bool, 'publishTo': str}

    RETURNS = {'success': bool}


class FetchServer(Endpoint):

    """FCO REST API fetchServer endpoint.

    This function will fetch a server over the internet, using the
    parameters supplied.

    Remarks:
    If the boolean parameter makeImage is set to true, then the call
    will create an image, else it will create a server, dependent upon
    the resource fetched and what the cluster supports. The call may be
    scheduled for a future date by setting the 'when' parameter. On
    successful execution, a Job object will be returned. On an
    exception, the resource is not created.

    Data (type name (required): description):
        cobjects.Server skeletonServer (T):
            A skeleton object containing details of the resource object
            to be created
        cobjects.FetchParameters fetchParameters (T):
            The parameters holding the url details
        datetime when (F):
            A date object specifying when the job is to be scheduled

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.GET, 'resources/fetch/server')]

    ALL_DATA = {'skeletonServer', 'fetchParameters', 'when'}
    REQUIRED_DATA = {'skeletonServer', 'fetchParameters'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'skeletonServer': cobjects.Server, 'fetchParameters':
                  cobjects.FetchParameters, 'when': datetime}

    RETURNS = {'job': cobjects.Job}


class GetResourceTypes(Endpoint):

    """FCO REST API getResourceTypes endpoint.

    This function will return list of available resource types.

    Remarks:
    Each of the resource types returned may be used as in a filter
    passed to listResources. On successful execution, a list of resource
    types will be returned. On an exception, an empty list is returned.

    Returns (type name: description):
        cobjects.MapHolder resourceTypeMap:
            A map holder of resource types
    """

    ENDPOINTS = [(Verbs.GET, 'resources/types')]

    RETURNS = {'resourceTypeMap': cobjects.MapHolder}


class CancelTransaction(Endpoint):

    """FCO REST API cancelTransaction endpoint.

    Cancels a transaction.

    Parameters (type name (required): description):
        str transactionUUID (T):
            The transaction to be cancelled

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled

    Returns (type name: description):
        cobjects.Job job:
            The job for the cancelled transaction.
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/transaction/{transactionUUID}/cancel')]

    ALL_PARAMS = {'transactionUUID'}
    REQUIRED_PARAMS = {'transactionUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'transactionUUID': str}

    ALL_DATA = {'when'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime}

    RETURNS = {'job': cobjects.Job}


class AttachSSHKey(Endpoint):

    """FCO REST API attachSSHKey endpoint.

    This function will attach an SSH key to a given server.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not attached.

    Parameters (type name (required): description):
        str SSHKeyUUID (T):
            The UUID of the ssh key to attach
        str serverUUID (T):
            The UUID of the server to which the ssh key should be
            attached

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/server/{serverUUID}/sshkey/{SSHKeyUUID}/attach')]

    ALL_PARAMS = {'SSHKeyUUID', 'serverUUID'}
    REQUIRED_PARAMS = {'SSHKeyUUID', 'serverUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'SSHKeyUUID': str, 'serverUUID': str}

    ALL_DATA = {'when'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime}

    RETURNS = {'job': cobjects.Job}


class DeleteUserFromGroup(Endpoint):

    """FCO REST API deleteUserFromGroup endpoint.

    This function will remove a user from the specified group, or all
    groups if the group UUID is null.

    Parameters (type name (required): description):
        str userUUID (T):
            The UUID of the user to remove
        str groupUUID (T):
            The UUID of the group to update

    Returns (type name: description):
        bool success:
            Returns true on success; otherwise, false.
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/group/{groupUUID}/user/{userUUID}/remove')]

    ALL_PARAMS = {'userUUID', 'groupUUID'}
    REQUIRED_PARAMS = {'userUUID', 'groupUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'userUUID': str, 'groupUUID': str}

    RETURNS = {'success': bool}


class DeployTemplate(Endpoint):

    """FCO REST API deployTemplate endpoint.

    This function will deploy a template object.

    Data (type name (required): description):
        cobjects.DeploymentInstance skeletonDeploymentInstance (T):
            The instance of the template to be deployed
        datetime when (F):
            A date object specifying when the job is to be scheduled

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.POST, 'resources/deployment_instance/deploy')]

    ALL_DATA = {'skeletonDeploymentInstance', 'when'}
    REQUIRED_DATA = {'skeletonDeploymentInstance'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'skeletonDeploymentInstance': cobjects.DeploymentInstance,
                  'when': datetime}

    RETURNS = {'job': cobjects.Job}


class GetPDFInvoice(Endpoint):

    """FCO REST API getPDFInvoice endpoint.

    This function will return an Invoice or Credit Note PDF.

    Remarks:
    This method returns a byte array that can be converted into the PDF
    file.

    Parameters (type name (required): description):
        str invoiceUUID (T):
            The UUID of the Invoice or Credit Note to be rendered

    Returns (type name: description):
        List(str) invoicePDF:
            The Invoice or Credit Note PDF
    """

    ENDPOINTS = [(Verbs.GET, 'resources/invoice/{invoiceUUID}/render_pdf')]

    ALL_PARAMS = {'invoiceUUID'}
    REQUIRED_PARAMS = {'invoiceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'invoiceUUID': str}

    RETURNS = {'invoicePDF': List(str)}


class ChangeDeploymentInstanceStatus(Endpoint):

    """FCO REST API changeDeploymentInstanceStatus endpoint.

    This function will change the state of (start, stop, kill or reboot)
    resources in the deployment instance.

    Remarks:
    The 'safe' parameter when set will ensure that a clean shutdown is
    always performed. The call may be scheduled for a future date by
    setting the 'when' parameter. On successful execution, a Job object
    will be returned. On an exception, the resource is not modified.

    Parameters (type name (required): description):
        str deploymentInstanceUUID (T):
            The UUID of deployment instance for which the status needs
            to be changed

    Data (type name (required): description):
        enums.DeploymentInstanceStatus newStatus (T):
            The status to which instance needs to be changed to
        datetime when (F):
            A date object specifying when the job is to be scheduled
        bool safe (T):
            A flag indicating whether the action can be performed safely
            or not
        cobjects.ResourceMetadata runtimeMetadata (F):
            The metadata to be used at runtime

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/deployment_instance/{deploymentInstanceUUID}/chang'
                  'estatus')]

    ALL_PARAMS = {'deploymentInstanceUUID'}
    REQUIRED_PARAMS = {'deploymentInstanceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'deploymentInstanceUUID': str}

    ALL_DATA = {'newStatus', 'safe', 'when', 'runtimeMetadata'}
    REQUIRED_DATA = {'newStatus', 'safe'}
    OPTIONAL_DATA = {'runtimeMetadata', 'when'}
    DATA_TYPES = {'newStatus': enums.DeploymentInstanceStatus, 'safe': bool,
                  'when': datetime, 'runtimeMetadata':
                  cobjects.ResourceMetadata}

    RETURNS = {'job': cobjects.Job}


class PurchaseUnits(Endpoint):

    """FCO REST API purchaseUnits endpoint.

    This function will purchase the specified number of units using the
    payment method instance.

    Data (type name (required): description):
        str paymentMethodInstanceUUID (F):
            The payment method to be used for the purchase
        str interactiveInputReturnURL (F):
            The URL for interactive input return
        str productOfferUUID (F):
            The UUID of the product offer to which the transaction
            applies
        float units (T):
            The number of units for the transactions
        bool dryrun (F):
            In the dryrun flag is set the call will not do a actual
            purchase, a TEST invoice object will be send to the caller
            indicating the amount which will be chared if the actual
            purchase was done

    Returns (type name: description):
        cobjects.Resource job:
            Returns the job linked with the current unit purchase. If
            dryrun is set to true this a TEST invoice Object will be
            returned
    """

    ENDPOINTS = [(Verbs.POST, 'purchase_units')]

    ALL_DATA = {'paymentMethodInstanceUUID', 'productOfferUUID', 'dryrun',
                'units', 'interactiveInputReturnURL'}
    REQUIRED_DATA = {'units'}
    OPTIONAL_DATA = {'paymentMethodInstanceUUID', 'productOfferUUID', 'dryrun',
                     'interactiveInputReturnURL'}
    DATA_TYPES = {'paymentMethodInstanceUUID': str, 'productOfferUUID': str,
                  'units': float, 'dryrun': bool, 'interactiveInputReturnURL':
                  str}

    RETURNS = {'job': cobjects.Resource}


class CreateServer(Endpoint):

    """FCO REST API createServer endpoint.

    This function will create a server using the supplied skeleton
    object.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not created.

    Data (type name (required): description):
        List(str) sshKeyUUIDList (F):
            A list of UUIDs of SSHKeys
        cobjects.Server skeletonServer (T):
            A server object containing the details of the server that is
            to be created
        cobjects.FetchParameters fetchParameters (F):
            The parameters holding the url details
        datetime when (F):
            A date object specifying when the job is to be scheduled

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.POST, 'resources/server')]

    ALL_DATA = {'sshKeyUUIDList', 'skeletonServer', 'fetchParameters', 'when'}
    REQUIRED_DATA = {'skeletonServer'}
    OPTIONAL_DATA = {'sshKeyUUIDList', 'fetchParameters', 'when'}
    DATA_TYPES = {'sshKeyUUIDList': List(str), 'skeletonServer':
                  cobjects.Server, 'fetchParameters': cobjects.FetchParameters,
                  'when': datetime}

    RETURNS = {'job': cobjects.Job}


class RevokeResource(Endpoint):

    """FCO REST API revokeResource endpoint.

    This function will revoke the publication of an image/template to a
    Customer or Billing Entity.

    Parameters (type name (required): description):
        str resourceUUID (T):
            The UUID of the resource to revoke

    Data (type name (required): description):
        bool exclude (F):
            To exclude/include the publishTo
        str publishTo (T):
            The UUID of the customer or billing from which publication
            should be revoked

    Returns (type name: description):
        bool success:
            Returns true on successs; otherwise, false.
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/{resourceUUID}/revoke')]

    ALL_PARAMS = {'resourceUUID'}
    REQUIRED_PARAMS = {'resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'resourceUUID': str}

    ALL_DATA = {'exclude', 'publishTo'}
    REQUIRED_DATA = {'publishTo'}
    OPTIONAL_DATA = {'exclude'}
    DATA_TYPES = {'exclude': bool, 'publishTo': str}

    RETURNS = {'success': bool}


class RevertToResource(Endpoint):

    """FCO REST API revertToResource endpoint.

    This function will revert all the changes of a resource object, back
    to its template.

    Remarks:
    For instance, this call can be used to revert a server or a disk
    back to its original snapshot. The call may be scheduled for a
    future date by setting the 'when' parameter. On successful
    execution, a Job object will be returned. On an exception, the
    resource is not reverted.

    Parameters (type name (required): description):
        str resourceUUID (T):
            The UUID of the snapshot resource to be reverted

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        str newSnapshotName (F):
            A name to be assigned to a snapshot which can optionally be
            created to store the current state. If this is null or
            empty, no snapshot will be created.

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/{resourceUUID}/revert')]

    ALL_PARAMS = {'resourceUUID'}
    REQUIRED_PARAMS = {'resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'resourceUUID': str}

    ALL_DATA = {'newSnapshotName', 'when'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'when', 'newSnapshotName'}
    DATA_TYPES = {'when': datetime, 'newSnapshotName': str}

    RETURNS = {'job': cobjects.Job}


class CreateBlob(Endpoint):

    """FCO REST API createBlob endpoint.

    This function will create a blob.

    Remarks:
    On successful execution it will return the newly created blob.

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.Blob skeletonBlob (T):
            The blob to be created

    Returns (type name: description):
        cobjects.Blob blob:
            The details of the blob to be created
    """

    ENDPOINTS = [(Verbs.POST, 'resources/blob')]

    ALL_DATA = {'skeletonBlob', 'when'}
    REQUIRED_DATA = {'skeletonBlob'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'skeletonBlob': cobjects.Blob}

    RETURNS = {'blob': cobjects.Blob}


class DeleteReferralPromoCode(Endpoint):

    """FCO REST API deleteReferralPromoCode endpoint.

    This function will remove the given referral promo code.

    Remarks:
    On an exception, the referral promo code is not deleted.

    Parameters (type name (required): description):
        str promoCode (T):
            The referral promocode to be removed

    Returns (type name: description):
        bool success:
            Returns true on success; otherwise, false.
    """

    ENDPOINTS = [(Verbs.DELETE, 'resources/referral_promocode/{promoCode}')]

    ALL_PARAMS = {'promoCode'}
    REQUIRED_PARAMS = {'promoCode'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'promoCode': str}

    RETURNS = {'success': bool}


class DetachSSHKey(Endpoint):

    """FCO REST API detachSSHKey endpoint.

    This function will detach an SSH key to a given server.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not detached.

    Parameters (type name (required): description):
        str SSHKeyUUID (T):
            The UUID of the ssh key to detach
        str serverUUID (T):
            The UUID of the server from which the ssh key should be
            detached

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/server/{serverUUID}/sshkey/{SSHKeyUUID}/detach')]

    ALL_PARAMS = {'SSHKeyUUID', 'serverUUID'}
    REQUIRED_PARAMS = {'SSHKeyUUID', 'serverUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'SSHKeyUUID': str, 'serverUUID': str}

    ALL_DATA = {'when'}
    REQUIRED_DATA = set()
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime}

    RETURNS = {'job': cobjects.Job}


class DescribeResource(Endpoint):

    """FCO REST API describeResource endpoint.

    Gets the Product Component Types that define an resource.

    Parameters (type name (required): description):
        str skeletonResource.resourceType (T):
            The resourceType field of the referenced skeletonResource
            object

    Data (type name (required): description):
        cobjects.Resource skeletonResource (T):
            The skeleton resource object.

    Returns (type name: description):
        List(cobjects.ProductComponentType) productComponentTypes:
            A list of product component types that define the resource.
    """

    ENDPOINTS = [(Verbs.GET,
                 'resources/{skeletonResource.resourceType}/describe'),
                 (Verbs.GET, 'resources/describe'), (Verbs.POST,
                 'resources/{skeletonResource.resourceType}/describe'),
                 (Verbs.POST, 'resources/describe')]

    ALL_PARAMS = {'skeletonResource.resourceType'}
    REQUIRED_PARAMS = {'skeletonResource.resourceType'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'skeletonResource.resourceType': str}

    ALL_DATA = {'skeletonResource'}
    REQUIRED_DATA = {'skeletonResource'}
    OPTIONAL_DATA = set()
    DATA_TYPES = {'skeletonResource': cobjects.Resource}

    RETURNS = {'productComponentTypes': List(cobjects.ProductComponentType)}


class ApplyFirewallTemplate(Endpoint):

    """FCO REST API applyFirewallTemplate endpoint.

    This function will apply a firewall template to a given IP address.

    Remarks:
    IPv4 firewall templates can only be applied to IPv4 addresses, and
    IPv6 firewall templates can only be applied to IPv6 addresses. The
    call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the firewall template is not applied.

    Parameters (type name (required): description):
        str firewallTemplateUUID (T):
            The UUID of the firewall template

    Data (type name (required): description):
        datetime when (T):
            A date object specifying when the job is to be scheduled,
            required=false
        str ipAddress (T):
            The IP address to which the firewall template needs to be
            applied

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/firewall_template/{firewallTemplateUUID}/apply')]

    ALL_PARAMS = {'firewallTemplateUUID'}
    REQUIRED_PARAMS = {'firewallTemplateUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'firewallTemplateUUID': str}

    ALL_DATA = {'ipAddress', 'when'}
    REQUIRED_DATA = {'ipAddress', 'when'}
    OPTIONAL_DATA = set()
    DATA_TYPES = {'when': datetime, 'ipAddress': str}

    RETURNS = {'job': cobjects.Job}


class CreateNetworkInterface(Endpoint):

    """FCO REST API createNetworkInterface endpoint.

    This function will create a network interface.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not modified.

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.Nic skeletonNIC (T):
            The network interface object to be created

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.POST, 'resources/nic')]

    ALL_DATA = {'when', 'skeletonNIC'}
    REQUIRED_DATA = {'skeletonNIC'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'skeletonNIC': cobjects.Nic}

    RETURNS = {'job': cobjects.Job}


class ModifyNetworkInterface(Endpoint):

    """FCO REST API modifyNetworkInterface endpoint.

    This function will modify a network interface.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not modified.

    Parameters (type name (required): description):
        str updatedResource.resourceUUID (T):
            The resourceUUID field of the referenced updatedResource
            object

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.Nic updatedResource (T):
            The modified network interface object

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT, 'resources/nic/{updatedResource.resourceUUID}')]

    ALL_PARAMS = {'updatedResource.resourceUUID'}
    REQUIRED_PARAMS = {'updatedResource.resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'updatedResource.resourceUUID': str}

    ALL_DATA = {'when', 'updatedResource'}
    REQUIRED_DATA = {'updatedResource'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'updatedResource': cobjects.Nic}

    RETURNS = {'job': cobjects.Job}


class CreateGroup(Endpoint):

    """FCO REST API createGroup endpoint.

    This function will create a new empty group.

    Remarks:
    The group cannot be created pre-populated with users; use
    addUserToGroup to add the users after creation. The call may be
    scheduled for a future date by setting the 'when' parameter. On
    successful execution, a Job object will be returned. On an
    exception, the resource is not created.

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.Group skeletonGroup (T):
            The skeleton group to create - note that the skeleton group
            cannot contain users

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.POST, 'resources/group')]

    ALL_DATA = {'when', 'skeletonGroup'}
    REQUIRED_DATA = {'skeletonGroup'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'skeletonGroup': cobjects.Group}

    RETURNS = {'job': cobjects.Job}


class ModifyNetwork(Endpoint):

    """FCO REST API modifyNetwork endpoint.

    This function will modify a network object.

    Remarks:
    The call may be scheduled for a future date by setting the 'when'
    parameter. On successful execution, a Job object will be returned.
    On an exception, the resource is not modified.

    Parameters (type name (required): description):
        str updatedResource.resourceUUID (T):
            The resourceUUID field of the referenced updatedResource
            object

    Data (type name (required): description):
        datetime when (F):
            A date object specifying when the job is to be scheduled
        cobjects.Network updatedResource (T):
            The network object to be modified

    Returns (type name: description):
        cobjects.Job job:
            The scheduled Job object
    """

    ENDPOINTS = [(Verbs.PUT,
                 'resources/network/{updatedResource.resourceUUID}')]

    ALL_PARAMS = {'updatedResource.resourceUUID'}
    REQUIRED_PARAMS = {'updatedResource.resourceUUID'}
    OPTIONAL_PARAMS = set()
    PARAMS_TYPES = {'updatedResource.resourceUUID': str}

    ALL_DATA = {'when', 'updatedResource'}
    REQUIRED_DATA = {'updatedResource'}
    OPTIONAL_DATA = {'when'}
    DATA_TYPES = {'when': datetime, 'updatedResource': cobjects.Network}

    RETURNS = {'job': cobjects.Job}
