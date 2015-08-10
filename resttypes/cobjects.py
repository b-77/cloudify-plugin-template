# coding=UTF-8

"""All the REST Complex Objects used by the FCO REST API."""

import resttypes.enums as enums
from resttypes import to_str
from resttypes import is_acceptable as c_is_acceptable
from resttypes import construct_data as c_construct_data
from typed import Typed
from typed.builtins import (List, Dict)

from datetime import datetime

# from cloudify import ctx


class ComplexObject(Typed):

    """Generic class for FCO REST API Complex Objects."""

    def __init__(self, data=None, *args,  **kwargs):
        """Initialise FCO REST API Complex Object."""
        super(ComplexObject, self).__init__(self)

        # We can append underscores to avoid keyword conflicts
        kwargs = {k.rstrip('_'): to_str(v) for k, v in kwargs.items()}

        if data is None:
            data = {}

        if hasattr(data, 'update'):
            data.update(kwargs)
        elif hasattr(data, 'extend'):
            data.extend(args)

        # TODO: creating the data structure should make it acceptable
        if not self.is_acceptable(data):
            # ctx.logger.info(data)
            raise Exception('Invalid data to create class {}'
                            .format(type(self).__name__))

        self._data = self.construct_data(data)

    def __getattr__(self, attr):
        """Easily access FCO REST API Complex Object attributes."""
        if attr not in self.ALL_ATTRIBS:
            raise Exception('Complex Object {} does not have {}'
                            .format(type(self).__name__, attr))
        else:
            return self._data.get(attr)

    def __str__(self):
        return '({}){}'.format(self.__class__.__name__, str(self._data))

    # TODO: catch exceptions upstairs
    @classmethod
    def is_acceptable(cls, inst):
        req = cls.REQUIRED_ATTRIBS.copy()
        opt = cls.OPTIONAL_ATTRIBS.copy()
        try:
            for k, v in inst.items():
                # ctx.logger.info(' -> {}: {}, {}'.format(k, v, cls.TYPES[k]))
                if k in req:
                    req.remove(k)
                else:
                    opt.remove(k)
                if not c_is_acceptable(v, cls.TYPES[k], cls._noneable):
                    return False
        except:
            raise
        return not req or cls._noneable

    @classmethod
    def construct_data(cls, inst):
        inst = inst.copy()
        for k, v in inst.items():
            inst[k] = c_construct_data(v, cls.TYPES[k], cls._noneable)
        return inst


class GenericContainer(ComplexObject):

    """Generic container for unspecified types.

    Every attribute request will either return the value of the corresponding
    entry in the stored dict or list, or None. Used when type not specified in
    the API documentation.
    """

    def __getattr__(self, item):
        """Returns the mapped value of the attribute requested or None.

        If a GenericContainer object was explicitly instantiated with an
        unsupported type it will return that type for every attribute request,
        so long as the type does not support the 'get' method.
        """
        if hasattr(self._data, 'get'):
            return self._data.get(item)
        return self._data

    @classmethod
    def is_acceptable(cls, inst):
        """All data is acceptable for the GenericContainer."""
        return True

    @classmethod
    def construct_data(cls, inst):
        """Recursively create instances of itself from lists and dicts.

        Recursion stops when encountering an unsupported type, in whiczh case
        that type is set as the value.
        """
        supported = (list, dict)
        if isinstance(inst, list):
            inst = list(inst)
            for k, v in enumerate(inst):
                if type(v) in supported:
                    inst[k] = GenericContainer(v)
        elif isinstance(inst, dict):
            inst = inst.copy()
            for k, v in inst.items():
                if type(v) in supported:
                    inst[k] = GenericContainer(v)
        return inst


class InvoiceItem(ComplexObject):

    """FCO REST API InvoiceItem complex object.

    Name.

    Attributes (type name (required): description:
        float invoiceItemTaxAmt (T):
            The amount of tax associated with the invoice line
        float invoiceItemTotalExc (T):
            The value associated with the invoice line (excluding tax)
        str description (T):
            The invoice line description
        float taxRate (T):
            The tax rate
        str productPurchaseUUID (T):
            Purcshase UUID is the invoice item is linked with a purchase
        float invoiceItemTotalInc (T):
            The invoice line total (including tax)
        str invoiceUUID (T):
            The UUID of the invoice
        float unitPrice (T):
            The unit price associated with the invoice item
        int quantity (T):
            The quantity associated with the invoice item
    """

    ALL_ATTRIBS = {'invoiceItemTaxAmt', 'invoiceItemTotalExc', 'description',
                   'taxRate', 'productPurchaseUUID', 'invoiceItemTotalInc',
                   'invoiceUUID', 'unitPrice', 'quantity'}
    REQUIRED_ATTRIBS = {'invoiceItemTaxAmt', 'invoiceItemTotalExc',
                        'description', 'taxRate', 'productPurchaseUUID',
                        'invoiceItemTotalInc', 'invoiceUUID', 'unitPrice',
                        'quantity'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'invoiceItemTaxAmt': float, 'invoiceItemTotalExc': float,
             'description': str, 'taxRate': float, 'productPurchaseUUID': str,
             'invoiceItemTotalInc': float, 'invoiceUUID': str, 'unitPrice':
             float, 'quantity': int}


class ResourceKey(ComplexObject):

    """FCO REST API ResourceKey complex object.

    Name.

    Attributes (type name (required): description:
        int extraFlag (T):
            Extra flag to indicate whether key is a sticky key
        str name (T):
            The name of the key
        float weight (T):
            The affinity weight of the key (zero means none)
        str value (T):
            The value set on the key
        str resourceUUID (T):
            The UUID of the resource to which the key is attached
        enums.ResourceKeyType type (T):
            The type of the key (system or user)
    """

    ALL_ATTRIBS = {'extraFlag', 'name', 'weight', 'value', 'resourceUUID',
                   'type'}
    REQUIRED_ATTRIBS = {'extraFlag', 'name', 'weight', 'value', 'resourceUUID',
                        'type'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'extraFlag': int, 'name': str, 'weight': float, 'value': str,
             'resourceUUID': str, 'type': enums.ResourceKeyType}


class PublishTo(ComplexObject):

    """FCO REST API PublishTo complex object.

    Name.

    Attributes (type name (required): description:
        enums.ResourceType resourceType (T):
            the type of the resource to whom publication is made
        bool exclude (T):
            the include/exclude tag name
        str resourceName (T):
            the name of the resource to whom publication is made
        str resourceUUID (T):
            the UUID of the resource to whom publication is made (either
            a customer, or a billing entity, or NULL for the platform as
            a whole)
    """

    ALL_ATTRIBS = {'resourceType', 'exclude', 'resourceUUID', 'resourceName'}
    REQUIRED_ATTRIBS = {'resourceType', 'exclude', 'resourceName',
                        'resourceUUID'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'resourceType': enums.ResourceType, 'exclude': bool,
             'resourceName': str, 'resourceUUID': str}


class OrderedField(ComplexObject):

    """FCO REST API OrderedField complex object.

    Name.

    Attributes (type name (required): description:
        enums.Aggregation aggregationFunction (F):
            Either null, or (if specified) the aggregationFunction
            associated with the aggregated query
        str fieldName (T):
            The field name to order by
        enums.ResultOrder sortOrder (T):
            The direction to order by (ascending or descending)
    """

    ALL_ATTRIBS = {'aggregationFunction', 'fieldName', 'sortOrder'}
    REQUIRED_ATTRIBS = {'fieldName', 'sortOrder'}
    OPTIONAL_ATTRIBS = {'aggregationFunction'}
    TYPES = {'aggregationFunction': enums.Aggregation, 'fieldName': str,
             'sortOrder': enums.ResultOrder}


class ResultRow(ComplexObject):

    """FCO REST API ResultRow complex object.

    Name.

    Attributes (type name (required): description:
        List(str) column (T):
            An array of the values of the fields and aggregated fields
            in the order specified in the query, in all cases returned
            as strings.
        Dict(str, str) columnMap (T):
            The hash of the output field or aggregation field, and the
            value of that field or aggregated field, in all cases
            returned as strings.
    """

    ALL_ATTRIBS = {'column', 'columnMap'}
    REQUIRED_ATTRIBS = {'column', 'columnMap'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'column': List(str), 'columnMap': Dict(str, str)}


class ReferralPromoCode(ComplexObject):

    """FCO REST API ReferralPromoCode complex object.

    Name.

    Attributes (type name (required): description:
        enums.ReferralStatus status (F):
            The referral status of the promo code
        bool used (F):
            A flag to indicate the promotion code has been used
        bool reuse (F):
            A flag to indicate whether the promotion code can be reused
        str promotionUUID (T):
            The promotion UUID
        str promoCode (T):
            The promotion code
        str invitorCustomerUUID (F):
            The invitor's customer UUID with which it is associated
        str emailAddress (T):
            The email address associated with the promo code
        str inviteeCustomerUUID (T):
            The invitee's customer UUID with which it is associated
        datetime expiryDate (T):
            The expiry date of the promo code
    """

    ALL_ATTRIBS = {'status', 'used', 'reuse', 'promotionUUID', 'promoCode',
                   'invitorCustomerUUID', 'emailAddress',
                   'inviteeCustomerUUID', 'expiryDate'}
    REQUIRED_ATTRIBS = {'expiryDate', 'promoCode', 'emailAddress',
                        'inviteeCustomerUUID', 'promotionUUID'}
    OPTIONAL_ATTRIBS = {'status', 'used', 'reuse', 'invitorCustomerUUID'}
    TYPES = {'status': enums.ReferralStatus, 'used': bool, 'reuse': bool,
             'promotionUUID': str, 'promoCode': str, 'invitorCustomerUUID':
             str, 'emailAddress': str, 'inviteeCustomerUUID': str,
             'expiryDate': datetime}


class ResourceMetadata(ComplexObject):

    """FCO REST API ResourceMetadata complex object.

    Name.

    Attributes (type name (required): description:
        str resourceUUID (T):
            The UUID of the resource to which the metadata is attached
        str publicMetadata (T):
            The public metadata
        str systemMetadata (T):
            The system metadata
        str restrictedMetadata (T):
            The restricted metadata
        str privateMetadata (T):
            The private metadata
    """

    ALL_ATTRIBS = {'resourceUUID', 'publicMetadata', 'systemMetadata',
                   'restrictedMetadata', 'privateMetadata'}
    REQUIRED_ATTRIBS = {'resourceUUID', 'publicMetadata', 'systemMetadata',
                        'restrictedMetadata', 'privateMetadata'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'resourceUUID': str, 'publicMetadata': str, 'systemMetadata': str,
             'restrictedMetadata': str, 'privateMetadata': str}


class PromoCode(ComplexObject):

    """FCO REST API PromoCode complex object.

    Name.

    Attributes (type name (required): description:
        str promoCode (T):
            The promotion code
        bool reuse (F):
            A flag to indicate whether the promotion code can be reused
        bool used (F):
            A flag to indicate the promotion code has been used
        str promotionUUID (T):
            The promotion UUID
    """

    ALL_ATTRIBS = {'promoCode', 'reuse', 'used', 'promotionUUID'}
    REQUIRED_ATTRIBS = {'promoCode', 'promotionUUID'}
    OPTIONAL_ATTRIBS = {'used', 'reuse'}
    TYPES = {'promoCode': str, 'reuse': bool, 'used': bool, 'promotionUUID':
             str}


class UnitTransactionSummary(ComplexObject):

    """FCO REST API UnitTransactionSummary complex object.

    Name.

    Attributes (type name (required): description:
        datetime transactionDate (T):
            The date associated with the transaction summary
        str customerName (F):
            The name of the customer associated with the transaction
            summary
        enums.ResourceType resourceType (T):
            The type of the resource
        float unitCredits (T):
            The total credits within the summary period
        float freeUnits (T):
            The total free units within the summary period
        str customerUUID (T):
            The UUID associated with the transaction summary
        str billingEntityUUID (T):
            Billing Entity UUID of the customer
        float unitDebits (T):
            The total debits within the summary period
    """

    ALL_ATTRIBS = {'unitCredits', 'customerName', 'resourceType',
                   'transactionDate', 'freeUnits', 'customerUUID',
                   'billingEntityUUID', 'unitDebits'}
    REQUIRED_ATTRIBS = {'transactionDate', 'resourceType', 'unitCredits',
                        'freeUnits', 'customerUUID', 'billingEntityUUID',
                        'unitDebits'}
    OPTIONAL_ATTRIBS = {'customerName'}
    TYPES = {'transactionDate': datetime, 'customerName': str, 'resourceType':
             enums.ResourceType, 'unitCredits': float, 'freeUnits': float,
             'customerUUID': str, 'billingEntityUUID': str, 'unitDebits':
             float}


class Address(ComplexObject):

    """FCO REST API Address complex object.

    Name.

    Attributes (type name (required): description:
        str address1 (F):
            The first line of the address
        str address2 (F):
            The second line of the address
        str address3 (F):
            The third line of the address or town
        str address4 (F):
            The fourth line of the address or county
        str address5 (F):
            The fifth line of the address or country
        str address6 (F):
            The sixth line of the address or postal code
    """

    ALL_ATTRIBS = {'address1', 'address2', 'address3', 'address4', 'address5',
                   'address6'}
    REQUIRED_ATTRIBS = set()
    OPTIONAL_ATTRIBS = {'address1', 'address2', 'address3', 'address4',
                        'address5', 'address6'}
    TYPES = {'address1': str, 'address2': str, 'address3': str, 'address4':
             str, 'address5': str, 'address6': str}


class AuthenticationToken(ComplexObject):

    """FCO REST API AuthenticationToken complex object.

    Name.

    Attributes (type name (required): description:
        str publicToken (T):
            The public facing unique token value.
        str creatorCustomerUUID (T):
            The UUID of the Customer that created the authentication
            token.
        int expires (T):
            The time that the token will expire as a Unix timestamp.
        str customerUUID (T):
            The UUID of the associated Customer.
        str userUUID (T):
            The UUID of the associated User.
        int renewalAmount (T):
            The amount of time, in seconds, that the token will
            automatically renew by
        str creatorUserUUID (T):
            The UUID of the User that created the authentication token.
        bool automaticRenewal (T):
            State if the token will be automatically renewed when used.
    """

    ALL_ATTRIBS = {'publicToken', 'creatorCustomerUUID', 'expires',
                   'customerUUID', 'userUUID', 'renewalAmount',
                   'automaticRenewal', 'creatorUserUUID'}
    REQUIRED_ATTRIBS = {'publicToken', 'creatorCustomerUUID', 'expires',
                        'customerUUID', 'userUUID', 'renewalAmount',
                        'creatorUserUUID', 'automaticRenewal'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'publicToken': str, 'creatorCustomerUUID': str, 'expires': int,
             'customerUUID': str, 'userUUID': str, 'renewalAmount': int,
             'creatorUserUUID': str, 'automaticRenewal': bool}


class JadeList(ComplexObject):

    """FCO REST API JadeList complex object.

    Name.

    Attributes (type name (required): description:
        List(str) details (T):
            The list of strings
    """

    ALL_ATTRIBS = {'details'}
    REQUIRED_ATTRIBS = {'details'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'details': List(str)}


class PseudoResource(ComplexObject):

    """FCO REST API PseudoResource complex object.

    Name.

    Attributes (type name (required): description:
        enums.ResourceType resourceType (T):
            The type of the resource
    """

    ALL_ATTRIBS = {'resourceType'}
    REQUIRED_ATTRIBS = {'resourceType'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'resourceType': enums.ResourceType}


class StatementDetail(ComplexObject):

    """FCO REST API StatementDetail complex object.

    Name.

    Attributes (type name (required): description:
        float debitAmount (T):
            The debit amount for the statement detail.
        float balanceTodate (T):
            The balance of the customer when the statement detail was
            created.
        int timestamp (T):
            The date/time the statement detail was created.
        str description (T):
            The description of the statement detail.
        float creditAmount (T):
            The credit amount for the statement detail.
        str customerUUID (T):
            The UUID of the customer associated with the statement
            detail.
        float lastBalance (T):
            The balance of the customer before the statement detail was
            created.
        str reference (T):
            The UUID of the invoice, transaction or credit note
            associated with the statement detail.
        enums.StatementType recordType (T):
            The type of statement detail.
    """

    ALL_ATTRIBS = {'debitAmount', 'balanceTodate', 'timestamp', 'creditAmount',
                   'customerUUID', 'lastBalance', 'recordType', 'reference',
                   'description'}
    REQUIRED_ATTRIBS = {'debitAmount', 'balanceTodate', 'timestamp',
                        'description', 'creditAmount', 'customerUUID',
                        'lastBalance', 'reference', 'recordType'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'debitAmount': float, 'balanceTodate': float, 'timestamp': int,
             'description': str, 'creditAmount': float, 'customerUUID': str,
             'lastBalance': float, 'reference': str, 'recordType':
             enums.StatementType}


class ExternalVm(ComplexObject):

    """FCO REST API ExternalVm complex object.

    Name.

    Attributes (type name (required): description:
        bool isRunning (T):
                     No documentation is available for this field #####
        str name (T):
                     No documentation is available for this field #####
        str hostContainer (T):
                     No documentation is available for this field #####
        int diskCount (T):
                     No documentation is available for this field #####
        int cpuCount (T):
                     No documentation is available for this field #####
        int ramCount (T):
                     No documentation is available for this field #####
        int nicCount (T):
                     No documentation is available for this field #####
        str uid (T):
                     No documentation is available for this field #####
    """

    ALL_ATTRIBS = {'isRunning', 'name', 'hostContainer', 'diskCount',
                   'cpuCount', 'ramCount', 'nicCount', 'uid'}
    REQUIRED_ATTRIBS = {'isRunning', 'name', 'hostContainer', 'diskCount',
                        'cpuCount', 'ramCount', 'nicCount', 'uid'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'isRunning': bool, 'name': str, 'hostContainer': str, 'diskCount':
             int, 'cpuCount': int, 'ramCount': int, 'nicCount': int, 'uid':
             str}


class VncForwarderDetails(ComplexObject):

    """FCO REST API VncForwarderDetails complex object.

    Name.

    Attributes (type name (required): description:
        int proxyPort (T):
            VNC proxy port
        str nodeDomain (T):
            Node domain
        str nodePassword (T):
            The password for the node
        str protocol (T):
            VNC protocol
        int sessionStartTime (T):
            Session start time in milliseconds
        str handler (T):
            Handler type
        str preconnectionBlob (T):
            Pre connection data
        str sessionKey (T):
            Holds the autogenerated session key
        int nodePort (T):
            VNC node port
        str nodeUsername (T):
            The username for the node
        str nodeIp (T):
            VNC node IP
        int serverId (T):
            The server ID
        str password (T):
            VNC password of the server
        str proxyIp (T):
            IP address of the cluster proxy server
    """

    ALL_ATTRIBS = {'proxyPort', 'nodeDomain', 'nodePassword', 'protocol',
                   'sessionKey', 'sessionStartTime', 'preconnectionBlob',
                   'handler', 'nodePort', 'nodeUsername', 'nodeIp', 'serverId',
                   'password', 'proxyIp'}
    REQUIRED_ATTRIBS = {'proxyPort', 'nodeDomain', 'nodePassword', 'protocol',
                        'sessionStartTime', 'handler', 'preconnectionBlob',
                        'sessionKey', 'nodePort', 'nodeUsername', 'nodeIp',
                        'serverId', 'password', 'proxyIp'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'proxyPort': int, 'nodeDomain': str, 'nodePassword': str,
             'protocol': str, 'sessionStartTime': int, 'handler': str,
             'preconnectionBlob': str, 'sessionKey': str, 'nodePort': int,
             'nodeUsername': str, 'nodeIp': str, 'serverId': int, 'password':
             str, 'proxyIp': str}


class TemplateProtectionPermission(ComplexObject):

    """FCO REST API TemplateProtectionPermission complex object.

    Name.

    Attributes (type name (required): description:
        bool canModify (T):
            Must be set if the resources derived deployment instances it
            can be modified
        bool canDeleteIndividually (T):
            Must be set if the each resources in deployment instance can
            be deleted individually
        bool canIndividuallyStartStop (T):
            Must be set if the each server in deployment instance can be
            individually started and stopped
    """

    ALL_ATTRIBS = {'canModify', 'canDeleteIndividually',
                   'canIndividuallyStartStop'}
    REQUIRED_ATTRIBS = {'canModify', 'canDeleteIndividually',
                        'canIndividuallyStartStop'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'canModify': bool, 'canDeleteIndividually': bool,
             'canIndividuallyStartStop': bool}


class TransactionLog(ComplexObject):

    """FCO REST API TransactionLog complex object.

    Name.

    Attributes (type name (required): description:
        str reference (T):
            The textual reference of the transaction as used by the
            payment processing module
        datetime lastModified (F):
            The date at which the transaction was last modified
        str request (T):
            The payment request as used by the payment processing module
        int id (F):
            The numeric order ID
        str customerUUID (T):
            The UUID of customer to which the transaction relates
        str billingEntityUUID (F):
            The UUID of billing entity to which the transaction relates
        str response (T):
            The payment response as used by the payment processing
            module
    """

    ALL_ATTRIBS = {'reference', 'lastModified', 'request', 'response',
                   'customerUUID', 'billingEntityUUID', 'id'}
    REQUIRED_ATTRIBS = {'request', 'response', 'reference', 'customerUUID'}
    OPTIONAL_ATTRIBS = {'lastModified', 'billingEntityUUID', 'id'}
    TYPES = {'reference': str, 'lastModified': datetime, 'request': str, 'id':
             int, 'customerUUID': str, 'billingEntityUUID': str, 'response':
             str}


class ImagePermission(ComplexObject):

    """FCO REST API ImagePermission complex object.

    Name.

    Attributes (type name (required): description:
        bool canCreateServer (T):
            Must be set if the image or disks/servers derived from it
            can be used to create a server
        bool canHaveAdditionalDisks (T):
            Must be set if the image or disks/servers derived from it
            can have additional disks attached
        bool canSnapshot (T):
            Must be set if the image or disks/servers derived from it
            can be snapshotted
        bool canConsole (T):
            Must be set if the image or disks/servers derived from it
            can have a console opened to them
        bool canBeSecondaryDisk (T):
            Must be set if the image or disks derived from it can be
            attached as a non-boot disk
        bool canClone (T):
            Must be set if the image or disks/servers derived from it
            can be cloned
        bool canStart (T):
            Must be set if the image or disks/servers derived from it
            can be started
        bool canBeDetachedFromServer (T):
            Must be set if the image or disks derived from it can be
            detached from a server
        bool canImage (T):
            Must be set if the image or disks/servers derived from it
            can be made into an image
    """

    ALL_ATTRIBS = {'canCreateServer', 'canHaveAdditionalDisks', 'canSnapshot',
                   'canConsole', 'canBeSecondaryDisk', 'canClone', 'canStart',
                   'canBeDetachedFromServer', 'canImage'}
    REQUIRED_ATTRIBS = {'canCreateServer', 'canHaveAdditionalDisks',
                        'canSnapshot', 'canConsole', 'canBeSecondaryDisk',
                        'canClone', 'canStart', 'canBeDetachedFromServer',
                        'canImage'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'canCreateServer': bool, 'canHaveAdditionalDisks': bool,
             'canSnapshot': bool, 'canConsole': bool, 'canBeSecondaryDisk':
             bool, 'canClone': bool, 'canStart': bool,
             'canBeDetachedFromServer': bool, 'canImage': bool}


class FilterCondition(ComplexObject):

    """FCO REST API FilterCondition complex object.

    Name.

    Attributes (type name (required): description:
        str field (T):
            The field the filter condition must match
        enums.Condition condition (T):
            The filter condition (defaults to IS_EQUAL_TO)
        List(str) value (T):
            The value or values the filter condition must match
    """

    ALL_ATTRIBS = {'field', 'value', 'condition'}
    REQUIRED_ATTRIBS = {'field', 'condition', 'value'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'field': str, 'condition': enums.Condition, 'value': List(str)}


class CallbackParams(ComplexObject):

    """FCO REST API CallbackParams complex object.

    Name.

    Attributes (type name (required): description:
        Dict(str, str) hash (F):
            A map containing parameters for a payment callback.
    """

    ALL_ATTRIBS = {'hash'}
    REQUIRED_ATTRIBS = set()
    OPTIONAL_ATTRIBS = {'hash'}
    TYPES = {'hash': Dict(str, str)}


class EmailTemplate(ComplexObject):

    """FCO REST API EmailTemplate complex object.

    Name.

    Attributes (type name (required): description:
        str body (T):
            The body for the email
        Dict(enums.BillingEntityVAR, str) billingEmailVar (T):
            A map containing the billing entity variables and strings
            for the email
        bool enable (T):
            Enables an email template
        enums.EmailType emailType (T):
            The email type for the email
        str billingEntityUUID (T):
            The billing entity ID for the email template
        str subject (T):
            The subject line for the email
    """

    ALL_ATTRIBS = {'body', 'billingEmailVar', 'enable', 'emailType',
                   'billingEntityUUID', 'subject'}
    REQUIRED_ATTRIBS = {'body', 'billingEmailVar', 'enable', 'emailType',
                        'billingEntityUUID', 'subject'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'body': str, 'billingEmailVar':
             Dict(enums.BillingEntityVAR, str), 'enable': bool, 'emailType':
             enums.EmailType, 'billingEntityUUID': str, 'subject': str}


class CapabilityAction(ComplexObject):

    """FCO REST API CapabilityAction complex object.

    Name.

    Attributes (type name (required): description:
        enums.Capability capability (T):
            The Capability used by the CapabilityAction
        enums.ResourceType resourceType (T):
            The ResourceType used by the CapabilityAction
    """

    ALL_ATTRIBS = {'capability', 'resourceType'}
    REQUIRED_ATTRIBS = {'capability', 'resourceType'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'capability': enums.Capability, 'resourceType':
             enums.ResourceType}


class PurchasedUnits(ComplexObject):

    """FCO REST API PurchasedUnits complex object.

    Name.

    Attributes (type name (required): description:
        datetime date (T):
            The date of the unit purchase
        float unitsPurchased (T):
            The number of units purchased
        str billingEntityUUID (T):
            The UUID of the Billing Entity
        str customerUUID (T):
            The UUID of the customer associated with the unit purchase
    """

    ALL_ATTRIBS = {'date', 'unitsPurchased', 'billingEntityUUID',
                   'customerUUID'}
    REQUIRED_ATTRIBS = {'date', 'unitsPurchased', 'billingEntityUUID',
                        'customerUUID'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'date': datetime, 'unitsPurchased': float, 'billingEntityUUID':
             str, 'customerUUID': str}


class FirewallRule(ComplexObject):

    """FCO REST API FirewallRule complex object.

    Name.

    Attributes (type name (required): description:
        int remotePort (T):
            the remote port (i.e. the port on the other end of the
            connection)
        enums.FirewallRuleDirection direction (T):
            the direction to which the rule applies (in or out)
        enums.FirewallProtocol protocol (T):
            the IP protocol being filtered
        int localPort (T):
            the local port (i.e. the port on the server)
        enums.ICMPParam icmpParam (T):
            the ICMP type
        enums.FirewallConnectionState connState (T):
            the connection state
        str templateUUID (T):
            the UUID of the FirewallTemplate to which the FirewallRule
            belongs
        int ipCIDRMask (T):
            the remote IP address mask
        enums.FirewallRuleAction action (T):
            the firewall action
        str ipAddress (T):
            the remote IP address
        str name (T):
            the name of the rule within the FirewallTemplate
    """

    ALL_ATTRIBS = {'remotePort', 'direction', 'protocol', 'localPort',
                   'icmpParam', 'connState', 'templateUUID', 'ipCIDRMask',
                   'action', 'ipAddress', 'name'}
    REQUIRED_ATTRIBS = {'remotePort', 'direction', 'protocol', 'localPort',
                        'icmpParam', 'connState', 'templateUUID', 'ipCIDRMask',
                        'action', 'ipAddress', 'name'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'remotePort': int, 'direction': enums.FirewallRuleDirection,
             'protocol': enums.FirewallProtocol, 'localPort': int, 'icmpParam':
             enums.ICMPParam, 'connState': enums.FirewallConnectionState,
             'templateUUID': str, 'ipCIDRMask': int, 'action':
             enums.FirewallRuleAction, 'ipAddress': str, 'name': str}


class SimpleResource(ComplexObject):

    """FCO REST API SimpleResource complex object.

    Name.

    Attributes (type name (required): description:
        enums.ResourceType resourceType (T):
            the type of the resource
        str resourceName (T):
            the name of the resource
        str resourceUUID (T):
            the UUID of the resource
    """

    ALL_ATTRIBS = {'resourceType', 'resourceName', 'resourceUUID'}
    REQUIRED_ATTRIBS = {'resourceType', 'resourceName', 'resourceUUID'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'resourceType': enums.ResourceType, 'resourceName': str,
             'resourceUUID': str}


class Tax(ComplexObject):

    """FCO REST API Tax complex object.

    Name.

    Attributes (type name (required): description:
        enums.TaxType taxType (T):
            The type of tax that is to be applied.
        float taxRate (T):
            The percentage of the total which is to be added as tax, as
            a value between 0.0 and 1.0.
        str taxName (T):
            The name of the tax that is to be applied.
    """

    ALL_ATTRIBS = {'taxType', 'taxRate', 'taxName'}
    REQUIRED_ATTRIBS = {'taxType', 'taxRate', 'taxName'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'taxType': enums.TaxType, 'taxRate': float, 'taxName': str}


class LicenceInformation(ComplexObject):

    """FCO REST API LicenceInformation complex object.

    Name.

    Attributes (type name (required): description:
        int activeClusters (T):
            The number of active clusters.
        str licenceXML (T):
            The licence XML
        int activeCores (T):
            The number of active CPU cores.
        Dict(str, str) versions (T):
            Software versions
        int permittedCPUCores (T):
            The number of permitted CPU cores.
        str luuid (T):
            The licence identifier UUID
        int permittedClusters (T):
            The number of permitted clusters.
        str licenceObject (T):
            The licence object.
    """

    ALL_ATTRIBS = {'activeClusters', 'licenceXML', 'activeCores', 'versions',
                   'permittedCPUCores', 'luuid', 'permittedClusters',
                   'licenceObject'}
    REQUIRED_ATTRIBS = {'activeClusters', 'licenceXML', 'activeCores',
                        'versions', 'permittedCPUCores', 'luuid',
                        'permittedClusters', 'licenceObject'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'activeClusters': int, 'licenceXML': str, 'activeCores': int,
             'versions': Dict(str, str), 'permittedCPUCores': int, 'luuid':
             str, 'permittedClusters': int, 'licenceObject': str}


class Currency(ComplexObject):

    """FCO REST API Currency complex object.

    Name.

    Attributes (type name (required): description:
        str symbol (F):
            The currency symbol
        str code (T):
            The currency code
        str description (F):
            The currency description
        int decimalPlace (F):
            The number of decimal places used by the currency
        int id (F):
            The numeric ID of the currency
    """

    ALL_ATTRIBS = {'symbol', 'code', 'description', 'decimalPlace', 'id'}
    REQUIRED_ATTRIBS = {'code'}
    OPTIONAL_ATTRIBS = {'symbol', 'description', 'decimalPlace', 'id'}
    TYPES = {'symbol': str, 'code': str, 'description': str, 'decimalPlace':
             int, 'id': int}


class AggregationField(ComplexObject):

    """FCO REST API AggregationField complex object.

    Name.

    Attributes (type name (required): description:
        enums.Aggregation aggregationFunction (T):
            The aggregation function to use
        str fieldName (T):
            The name of the field to be aggregated in FQL dot notation
    """

    ALL_ATTRIBS = {'aggregationFunction', 'fieldName'}
    REQUIRED_ATTRIBS = {'aggregationFunction', 'fieldName'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'aggregationFunction': enums.Aggregation, 'fieldName': str}


class HypervisorSetting(ComplexObject):

    """FCO REST API HypervisorSetting complex object.

    Name.

    Attributes (type name (required): description:
        bool locked (T):
            State if the setting is locked
        str key (T):
            The key use for the setting
        str value (T):
            The value used for the setting
    """

    ALL_ATTRIBS = {'locked', 'value', 'key'}
    REQUIRED_ATTRIBS = {'locked', 'key', 'value'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'locked': bool, 'key': str, 'value': str}


class SystemCapabilitySet(ComplexObject):

    """FCO REST API SystemCapabilitySet complex object.

    Name.

    Attributes (type name (required): description:
        List(enums.Networking) networking (T):
            Networking system capability
        enums.Invoicing invoicing (T):
            Invoicing capability
        enums.MultitierStorage multitierStorage (T):
            Multitier Storage capability
        enums.BentoBox bentoBox (T):
            Bentobox capability
        enums.Branding branding (T):
            Branding capability
        List(enums.Signup) signup (T):
            Signup system capability
        Dict(str, int) clusterHypervisor (T):
            Cluster hypervisor limits capability
        List(enums.Publish) publish (T):
            Image publication system capability
        enums.Email email (T):
            Email capability
        List(enums.EmulatedDevices) emulatedDevices (T):
            Disabling emulated device capability
        List(enums.Snapshotting) snapshotting (T):
            Snapshotting system capability
        List(enums.Cloning) cloning (T):
            Cloning system capability
        Dict(enums.MaxLimit, int) maxLimit (T):
            System limits capability
        List(enums.Vnc) vnc (T):
            VNC handler capability
        List(enums.Payment) payment (T):
            Payment system capability
    """

    ALL_ATTRIBS = {'networking', 'invoicing', 'multitierStorage', 'bentoBox',
                   'branding', 'signup', 'clusterHypervisor', 'publish',
                   'emulatedDevices', 'snapshotting', 'cloning', 'payment',
                   'maxLimit', 'vnc', 'email'}
    REQUIRED_ATTRIBS = {'networking', 'invoicing', 'multitierStorage',
                        'bentoBox', 'branding', 'signup', 'clusterHypervisor',
                        'publish', 'payment', 'email', 'snapshotting',
                        'cloning', 'maxLimit', 'vnc', 'emulatedDevices'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'networking': List(enums.Networking), 'invoicing':
             enums.Invoicing, 'multitierStorage': enums.MultitierStorage,
             'bentoBox': enums.BentoBox, 'branding': enums.Branding, 'signup':
             List(enums.Signup), 'clusterHypervisor': Dict(str, int),
             'publish': List(enums.Publish), 'payment': List(enums.Payment),
             'email': enums.Email, 'snapshotting': List(enums.Snapshotting),
             'cloning': List(enums.Cloning), 'maxLimit':
             Dict(enums.MaxLimit, int), 'vnc': List(enums.Vnc),
             'emulatedDevices': List(enums.EmulatedDevices)}


class EmailBlock(ComplexObject):

    """FCO REST API EmailBlock complex object.

    Name.

    Attributes (type name (required): description:
        bool enable (T):
            A flag to indicate whether the email block is enabled
        str name (T):
            The name of the email block
    """

    ALL_ATTRIBS = {'enable', 'name'}
    REQUIRED_ATTRIBS = {'enable', 'name'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'enable': bool, 'name': str}


class FetchParameters(ComplexObject):

    """FCO REST API FetchParameters complex object.

    Name.

    Attributes (type name (required): description:
        bool genPassword (F):
            A flag to indicate whether a default password should be
            generated for an image built with a fetched object
        enums.ResourceType resourceType (T):
            The type of the resource
        str checkSum (F):
            the checksum of the object to be fetched
        bool makeImage (F):
            A flag to indicate whether a disk image or server image (as
            opposed to a disk or server) should be built with the
            fetched object
        str url (T):
            the URL from which the fetched object is to be retrieved
        str authUserName (F):
            the user name to use when authenticating to retrieve the
            fetched object
        str defaultUserName (F):
            the default username to be supplied via the metadata service
            to an disk or server image built with a fetched object
        List(str) networkUUIDs (F):
            A list of networks to create NICs on (for fetching servers
            only)
        bool vmSupport (T):
            Indicate if the resource supports virtual machines
        str authPassword (F):
            the password to use when authenticating to retrieve the
            fetched object
        bool ctSupport (T):
            Indicate if the resource supports containers
    """

    ALL_ATTRIBS = {'genPassword', 'resourceType', 'checkSum', 'makeImage',
                   'url', 'authUserName', 'defaultUserName', 'networkUUIDs',
                   'vmSupport', 'authPassword', 'ctSupport'}
    REQUIRED_ATTRIBS = {'resourceType', 'url', 'ctSupport', 'vmSupport'}
    OPTIONAL_ATTRIBS = {'genPassword', 'checkSum', 'makeImage', 'authUserName',
                        'defaultUserName', 'networkUUIDs', 'authPassword'}
    TYPES = {'genPassword': bool, 'resourceType': enums.ResourceType,
             'checkSum': str, 'makeImage': bool, 'url': str, 'authUserName':
             str, 'defaultUserName': str, 'networkUUIDs': List(str),
             'vmSupport': bool, 'authPassword': str, 'ctSupport': bool}


class VNCConnection(ComplexObject):

    """FCO REST API VNCConnection complex object.

    Name.

    Attributes (type name (required): description:
        str serverName (T):
            The server name associated with this connection to display
            in the VNC window
        str vncPassword (T):
            The VNC password associated with this connection
        str webSocketPath (T):
            The websocket URL to use to connect
        str vncToken (T):
            The one-time token associated with this connection
        enums.VNCHandler vncHandler (T):
            The handler type
    """

    ALL_ATTRIBS = {'serverName', 'vncPassword', 'webSocketPath', 'vncToken',
                   'vncHandler'}
    REQUIRED_ATTRIBS = {'serverName', 'vncPassword', 'webSocketPath',
                        'vncToken', 'vncHandler'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'serverName': str, 'vncPassword': str, 'webSocketPath': str,
             'vncToken': str, 'vncHandler': enums.VNCHandler}


class Subnet(ComplexObject):

    """FCO REST API Subnet complex object.

    Name.

    Attributes (type name (required): description:
        str firstUsableAddress (F):
            The first usable address within the subnet
        str customerName (F):
            The name of the customer that owns the resource
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str broadcastAddress (F):
            The broadcast address (i.e. last, or all ones address)
            within the subnet
        str vdcUUID (T):
            The UUID of the VDC in which the resource is contained
        str productOfferUUID (F):
            The UUID of the product offer associated with the resource
        str resourceName (T):
            The name of the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
        str productOfferName (F):
            The name of the product offer associated with the resource
        str clusterUUID (T):
            The UUID of the cluster in which the resource is located
        bool systemAllocated (F):
            Indicates whether the subnet is allocated by the system or
            imported
        str networkUUID (T):
            The UUID of the network on which the subnet resides
        str deploymentInstanceName (F):
            The name of the deployment instance the resource is created
            from
        int sortOrder (T):
            The sort order value for the given resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        str customerUUID (F):
            The UUID of the customer that owns the resource
        str defaultGatewayAddress (F):
            The default gateway
        str clusterName (F):
            The name of the cluster in which the resource is located
        str vdcName (F):
            The name of the VDC in which the resource is contained
        enums.IPType subnetType (F):
            The type of the subnet (i.e. IPv4 or IPv6)
        enums.NetworkType networkType (F):
            The type of network on which the subnet resides
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str networkName (F):
            The name of the network on which the subnet resides
        str networkAddress (F):
            The network address (i.e. first, or all zeroes address)
            within the subnet
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        int mask (F):
            The CIDR length of the subnet mask
        str deploymentInstanceUUID (F):
            The uuid of the deployment instance the resource is created
            from
        List(str) useableIps (F):
            The usable IPs remaining on the subnet
    """

    ALL_ATTRIBS = {'firstUsableAddress', 'customerName', 'providers',
                   'resourceMetadata', 'billingEntityName', 'resourceState',
                   'broadcastAddress', 'vdcUUID', 'productOfferUUID',
                   'resourceName', 'resourceCreateDate', 'productOfferName',
                   'clusterUUID', 'systemAllocated', 'networkUUID',
                   'deploymentInstanceName', 'customerUUID', 'resourceUUID',
                   'billingEntityUUID', 'sortOrder', 'defaultGatewayAddress',
                   'clusterName', 'vdcName', 'subnetType', 'networkType',
                   'lastModifiedTime', 'networkName', 'networkAddress',
                   'resourceType', 'resourceKey', 'mask',
                   'deploymentInstanceUUID', 'useableIps'}
    REQUIRED_ATTRIBS = {'clusterUUID', 'networkUUID', 'resourceType',
                        'sortOrder', 'vdcUUID', 'resourceName'}
    OPTIONAL_ATTRIBS = {'firstUsableAddress', 'customerName', 'providers',
                        'resourceMetadata', 'billingEntityName',
                        'resourceState', 'broadcastAddress',
                        'productOfferUUID', 'resourceCreateDate',
                        'productOfferName', 'systemAllocated',
                        'deploymentInstanceName', 'customerUUID',
                        'resourceUUID', 'billingEntityUUID',
                        'defaultGatewayAddress', 'clusterName', 'vdcName',
                        'subnetType', 'networkType', 'lastModifiedTime',
                        'networkName', 'networkAddress', 'resourceKey', 'mask',
                        'deploymentInstanceUUID', 'useableIps'}
    TYPES = {'firstUsableAddress': str, 'customerName': str, 'providers':
             Dict(str, Dict(str, str)), 'resourceMetadata': ResourceMetadata,
             'billingEntityName': str, 'resourceState': enums.ResourceState,
             'broadcastAddress': str, 'vdcUUID': str, 'productOfferUUID': str,
             'resourceName': str, 'resourceCreateDate': datetime,
             'productOfferName': str, 'clusterUUID': str, 'systemAllocated':
             bool, 'networkUUID': str, 'deploymentInstanceName': str,
             'sortOrder': int, 'resourceUUID': str, 'billingEntityUUID': str,
             'customerUUID': str, 'defaultGatewayAddress': str, 'clusterName':
             str, 'vdcName': str, 'subnetType': enums.IPType, 'networkType':
             enums.NetworkType, 'lastModifiedTime': int, 'networkName': str,
             'networkAddress': str, 'resourceType': enums.ResourceType,
             'resourceKey': List(ResourceKey), 'mask': int,
             'deploymentInstanceUUID': str, 'useableIps': List(str)}


class VirtualResource(ComplexObject):

    """FCO REST API VirtualResource complex object.

    Name.

    Attributes (type name (required): description:
        str customerName (F):
            The name of the customer that owns the resource
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str deploymentInstanceUUID (F):
            The uuid of the deployment instance the resource is created
            from
        str vdcUUID (T):
            The UUID of the VDC in which the resource is contained
        str productOfferUUID (F):
            The UUID of the product offer associated with the resource
        str resourceName (T):
            The name of the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
        str productOfferName (F):
            The name of the product offer associated with the resource
        str clusterUUID (T):
            The UUID of the cluster in which the resource is located
        str deploymentInstanceName (F):
            The name of the deployment instance the resource is created
            from
        str customerUUID (F):
            The UUID of the customer that owns the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        int sortOrder (T):
            The sort order value for the given resource
        str clusterName (F):
            The name of the cluster in which the resource is located
        str vdcName (F):
            The name of the VDC in which the resource is contained
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
    """

    ALL_ATTRIBS = {'customerName', 'providers', 'resourceMetadata',
                   'billingEntityName', 'resourceState',
                   'deploymentInstanceUUID', 'vdcUUID', 'productOfferUUID',
                   'resourceName', 'resourceCreateDate', 'productOfferName',
                   'clusterUUID', 'deploymentInstanceName', 'customerUUID',
                   'resourceUUID', 'billingEntityUUID', 'sortOrder',
                   'clusterName', 'vdcName', 'lastModifiedTime',
                   'resourceType', 'resourceKey'}
    REQUIRED_ATTRIBS = {'resourceType', 'resourceName', 'clusterUUID',
                        'sortOrder', 'vdcUUID'}
    OPTIONAL_ATTRIBS = {'productOfferName', 'customerName', 'providers',
                        'clusterName', 'resourceKey', 'resourceMetadata',
                        'billingEntityName', 'resourceState', 'vdcName',
                        'deploymentInstanceUUID', 'customerUUID',
                        'resourceUUID', 'productOfferUUID',
                        'deploymentInstanceName', 'lastModifiedTime',
                        'billingEntityUUID', 'resourceCreateDate'}
    TYPES = {'customerName': str, 'providers': Dict(str, Dict(str, str)),
             'resourceMetadata': ResourceMetadata, 'billingEntityName': str,
             'resourceState': enums.ResourceState, 'deploymentInstanceUUID':
             str, 'vdcUUID': str, 'productOfferUUID': str, 'resourceName': str,
             'resourceCreateDate': datetime, 'productOfferName': str,
             'clusterUUID': str, 'deploymentInstanceName': str, 'customerUUID':
             str, 'resourceUUID': str, 'billingEntityUUID': str, 'sortOrder':
             int, 'clusterName': str, 'vdcName': str, 'lastModifiedTime': int,
             'resourceType': enums.ResourceType, 'resourceKey':
             List(ResourceKey)}


class Group(ComplexObject):

    """FCO REST API Group complex object.

    Name.

    Attributes (type name (required): description:
        str customerName (F):
            The name of the customer that owns the resource
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str deploymentInstanceUUID (F):
            The uuid of the deployment instance the resource is created
            from
        str vdcUUID (T):
            The UUID of the VDC in which the resource is contained
        str productOfferUUID (F):
            The UUID of the product offer associated with the resource
        str resourceName (T):
            The name of the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
        str productOfferName (F):
            The name of the product offer associated with the resource
        str clusterUUID (T):
            The UUID of the cluster in which the resource is located
        str deploymentInstanceName (F):
            The name of the deployment instance the resource is created
            from
        str customerUUID (F):
            The UUID of the customer that owns the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        enums.GroupType type (T):
            The type of the group concerned
        int sortOrder (T):
            The sort order value for the given resource
        List(str) users (F):
            A collection of UUIDs of users that are members of this
            group
        str clusterName (F):
            The name of the cluster in which the resource is located
        str vdcName (F):
            The name of the VDC in which the resource is contained
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        enums.ResourceType resourceType (T):
            The type of the resource
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
    """

    ALL_ATTRIBS = {'customerName', 'providers', 'resourceMetadata',
                   'billingEntityName', 'resourceState',
                   'deploymentInstanceUUID', 'vdcUUID', 'productOfferUUID',
                   'resourceName', 'resourceCreateDate', 'productOfferName',
                   'clusterUUID', 'deploymentInstanceName', 'customerUUID',
                   'resourceUUID', 'type', 'sortOrder', 'users', 'clusterName',
                   'vdcName', 'lastModifiedTime', 'resourceType',
                   'billingEntityUUID', 'resourceKey'}
    REQUIRED_ATTRIBS = {'clusterUUID', 'resourceType', 'sortOrder', 'vdcUUID',
                        'resourceName', 'type'}
    OPTIONAL_ATTRIBS = {'productOfferName', 'customerName', 'providers',
                        'clusterName', 'resourceKey', 'resourceMetadata',
                        'billingEntityName', 'resourceState', 'vdcName',
                        'deploymentInstanceUUID', 'customerUUID',
                        'resourceUUID', 'productOfferUUID',
                        'deploymentInstanceName', 'lastModifiedTime',
                        'billingEntityUUID', 'resourceCreateDate', 'users'}
    TYPES = {'customerName': str, 'providers': Dict(str, Dict(str, str)),
             'resourceMetadata': ResourceMetadata, 'billingEntityName': str,
             'resourceState': enums.ResourceState, 'deploymentInstanceUUID':
             str, 'vdcUUID': str, 'productOfferUUID': str, 'resourceName': str,
             'resourceCreateDate': datetime, 'productOfferName': str,
             'clusterUUID': str, 'deploymentInstanceName': str, 'customerUUID':
             str, 'resourceUUID': str, 'type': enums.GroupType, 'sortOrder':
             int, 'users': List(str), 'clusterName': str, 'vdcName': str,
             'lastModifiedTime': int, 'resourceType': enums.ResourceType,
             'billingEntityUUID': str, 'resourceKey': List(ResourceKey)}


class VDC(ComplexObject):

    """FCO REST API VDC complex object.

    Name.

    Attributes (type name (required): description:
        str customerName (F):
            The name of the customer that owns the resource
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str deploymentInstanceUUID (F):
            The uuid of the deployment instance the resource is created
            from
        str vdcUUID (T):
            The UUID of the VDC in which the resource is contained
        str productOfferUUID (F):
            The UUID of the product offer associated with the resource
        str resourceName (T):
            The name of the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
        str productOfferName (F):
            The name of the product offer associated with the resource
        str clusterUUID (T):
            The UUID of the cluster in which the resource is located
        str deploymentInstanceName (F):
            The name of the deployment instance the resource is created
            from
        str customerUUID (F):
            The UUID of the customer that owns the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        int sortOrder (T):
            The sort order value for the given resource
        str clusterName (F):
            The name of the cluster in which the resource is located
        str vdcName (F):
            The name of the VDC in which the resource is contained
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
    """

    ALL_ATTRIBS = {'customerName', 'providers', 'resourceMetadata',
                   'billingEntityName', 'resourceState',
                   'deploymentInstanceUUID', 'vdcUUID', 'productOfferUUID',
                   'resourceName', 'resourceCreateDate', 'productOfferName',
                   'clusterUUID', 'deploymentInstanceName', 'customerUUID',
                   'resourceUUID', 'billingEntityUUID', 'sortOrder',
                   'clusterName', 'vdcName', 'lastModifiedTime',
                   'resourceType', 'resourceKey'}
    REQUIRED_ATTRIBS = {'resourceType', 'resourceName', 'clusterUUID',
                        'sortOrder', 'vdcUUID'}
    OPTIONAL_ATTRIBS = {'productOfferName', 'customerName', 'providers',
                        'clusterName', 'resourceKey', 'resourceMetadata',
                        'billingEntityName', 'resourceState', 'vdcName',
                        'deploymentInstanceUUID', 'customerUUID',
                        'resourceUUID', 'productOfferUUID',
                        'deploymentInstanceName', 'lastModifiedTime',
                        'billingEntityUUID', 'resourceCreateDate'}
    TYPES = {'customerName': str, 'providers': Dict(str, Dict(str, str)),
             'resourceMetadata': ResourceMetadata, 'billingEntityName': str,
             'resourceState': enums.ResourceState, 'deploymentInstanceUUID':
             str, 'vdcUUID': str, 'productOfferUUID': str, 'resourceName': str,
             'resourceCreateDate': datetime, 'productOfferName': str,
             'clusterUUID': str, 'deploymentInstanceName': str, 'customerUUID':
             str, 'resourceUUID': str, 'billingEntityUUID': str, 'sortOrder':
             int, 'clusterName': str, 'vdcName': str, 'lastModifiedTime': int,
             'resourceType': enums.ResourceType, 'resourceKey':
             List(ResourceKey)}


class ReferralPromotion(ComplexObject):

    """FCO REST API ReferralPromotion complex object.

    Name.

    Attributes (type name (required): description:
        datetime startDate (T):
            The start date of the promotion code type
        str invitorProductOfferUUID (T):
            The number of units the invitor receives on successful
            completion
        datetime endDate (T):
            The end date of the promotion code type
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        int inviteeMinimumPurchase (F):
            The minimum unit purchase by the invitee to achieve
            successful completion
        str productOfferUUID (T):
            The numeric product offer ID associated with the promotion
            code
        str resourceName (T):
            The name of the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
        int maxOutStanding (F):
            The maximum number of outstanding instances of this referral
            promotion
        int priority (T):
            The priority of the referral scheme
        int sortOrder (T):
            The sort order value for the given resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        str productOfferName (F):
            The name of the product offer associated with the resource
        bool noCardCheck (T):
            A flag to indicate whether a card check can be skipped with
            the promotion code
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        float unitCost (F):
            The cost to the invitor's outstanding invitation balance
    """

    ALL_ATTRIBS = {'startDate', 'invitorProductOfferUUID', 'endDate',
                   'providers', 'resourceMetadata', 'billingEntityName',
                   'resourceState', 'inviteeMinimumPurchase',
                   'productOfferUUID', 'resourceName', 'resourceCreateDate',
                   'maxOutStanding', 'priority', 'sortOrder', 'resourceUUID',
                   'billingEntityUUID', 'productOfferName', 'noCardCheck',
                   'lastModifiedTime', 'resourceType', 'resourceKey',
                   'unitCost'}
    REQUIRED_ATTRIBS = {'startDate', 'invitorProductOfferUUID', 'endDate',
                        'resourceType', 'priority', 'noCardCheck', 'sortOrder',
                        'productOfferUUID', 'resourceName'}
    OPTIONAL_ATTRIBS = {'maxOutStanding', 'productOfferName', 'providers',
                        'resourceKey', 'resourceMetadata', 'billingEntityName',
                        'resourceState', 'inviteeMinimumPurchase',
                        'resourceUUID', 'lastModifiedTime',
                        'billingEntityUUID', 'unitCost', 'resourceCreateDate'}
    TYPES = {'startDate': datetime, 'invitorProductOfferUUID': str, 'endDate':
             datetime, 'providers': Dict(str, Dict(str, str)),
             'resourceMetadata': ResourceMetadata, 'billingEntityName': str,
             'resourceState': enums.ResourceState, 'inviteeMinimumPurchase':
             int, 'productOfferUUID': str, 'resourceName': str,
             'resourceCreateDate': datetime, 'maxOutStanding': int, 'priority':
             int, 'sortOrder': int, 'resourceUUID': str, 'billingEntityUUID':
             str, 'productOfferName': str, 'noCardCheck': bool,
             'lastModifiedTime': int, 'resourceType': enums.ResourceType,
             'resourceKey': List(ResourceKey), 'unitCost': float}


class StorageGroup(ComplexObject):

    """FCO REST API StorageGroup complex object.

    Name.

    Attributes (type name (required): description:
        bool isLocalGroup (T):
            State if this is a local storage group
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        bool isImageGroup (T):
            State if this is an image storage group
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        bool hasStorageUnit (T):
            State if this storage group has an assigned stoage unit
        enums.ResourceType resourceType (T):
            The type of the resource
        int sortOrder (T):
            The sort order value for the given resource
        str resourceName (T):
            The name of the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        bool isDefaultGroup (T):
            State if this is the default storage group
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        datetime resourceCreateDate (F):
            The creation date of the resource
    """

    ALL_ATTRIBS = {'isLocalGroup', 'providers', 'isImageGroup', 'resourceKey',
                   'resourceMetadata', 'billingEntityName', 'resourceState',
                   'hasStorageUnit', 'resourceType', 'sortOrder',
                   'resourceUUID', 'resourceName', 'isDefaultGroup',
                   'billingEntityUUID', 'lastModifiedTime',
                   'resourceCreateDate'}
    REQUIRED_ATTRIBS = {'isLocalGroup', 'isImageGroup', 'hasStorageUnit',
                        'resourceType', 'sortOrder', 'resourceName',
                        'isDefaultGroup'}
    OPTIONAL_ATTRIBS = {'providers', 'resourceKey', 'resourceMetadata',
                        'billingEntityName', 'resourceState', 'resourceUUID',
                        'lastModifiedTime', 'billingEntityUUID',
                        'resourceCreateDate'}
    TYPES = {'isLocalGroup': bool, 'providers': Dict(str, Dict(str, str)),
             'isImageGroup': bool, 'resourceKey': List(ResourceKey),
             'resourceMetadata': ResourceMetadata, 'billingEntityName': str,
             'resourceState': enums.ResourceState, 'hasStorageUnit': bool,
             'resourceType': enums.ResourceType, 'sortOrder': int,
             'resourceName': str, 'resourceUUID': str, 'isDefaultGroup': bool,
             'billingEntityUUID': str, 'lastModifiedTime': int,
             'resourceCreateDate': datetime}


class Blob(ComplexObject):

    """FCO REST API Blob complex object.

    Name.

    Attributes (type name (required): description:
        str value (T):
            The value of the resource to which the blob relates
        str customerName (F):
            The name of the customer that owns the resource
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        int sortOrder (T):
            The sort order value for the given resource
        bool publicResource (F):
            State if the Blob is a public resource, and availabel to the
            Open API services
        str resourceName (T):
            The name of the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str sha256 (F):
            The SHA_256 of the value to which the blob relates
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        datetime resourceCreateDate (F):
            The creation date of the resource
        str customerUUID (F):
            The UUID of the customer that owns the resource
    """

    ALL_ATTRIBS = {'customerName', 'providers', 'resourceType', 'customerUUID',
                   'resourceKey', 'resourceMetadata', 'billingEntityName',
                   'value', 'resourceUUID', 'resourceState', 'publicResource',
                   'resourceName', 'lastModifiedTime', 'sha256',
                   'billingEntityUUID', 'resourceCreateDate', 'sortOrder'}
    REQUIRED_ATTRIBS = {'resourceType', 'resourceName', 'sortOrder', 'value'}
    OPTIONAL_ATTRIBS = {'customerName', 'providers', 'resourceKey',
                        'resourceMetadata', 'billingEntityName',
                        'resourceState', 'customerUUID', 'resourceUUID',
                        'lastModifiedTime', 'sha256', 'billingEntityUUID',
                        'resourceCreateDate', 'publicResource'}
    TYPES = {'sortOrder': int, 'customerName': str, 'providers':
             Dict(str, Dict(str, str)), 'resourceType': enums.ResourceType,
             'resourceKey': List(ResourceKey), 'resourceMetadata':
             ResourceMetadata, 'billingEntityName': str, 'value': str,
             'customerUUID': str, 'resourceName': str, 'resourceUUID': str,
             'lastModifiedTime': int, 'sha256': str, 'billingEntityUUID': str,
             'resourceState': enums.ResourceState, 'resourceCreateDate':
             datetime, 'publicResource': bool}


class QueryResult(ComplexObject):

    """FCO REST API QueryResult complex object.

    Name.

    Attributes (type name (required): description:
        int listFrom (T):
            The index of the first result returned within this result
            set
        int totalCount (T):
            The total number of results available
        List(ResultRow) resultRow (T):
            An array of rows of the result, each being a hash of the
            output field or aggregation field, and the value of that
            field or aggregated field, in all cases returned as strings.
        int listTo (T):
            The index of the last result returned within this result set
    """

    ALL_ATTRIBS = {'listFrom', 'totalCount', 'resultRow', 'listTo'}
    REQUIRED_ATTRIBS = {'listFrom', 'totalCount', 'resultRow', 'listTo'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'listFrom': int, 'totalCount': int, 'resultRow': List(ResultRow),
             'listTo': int}


class TriggerMethod(ComplexObject):

    """FCO REST API TriggerMethod complex object.

    Name.

    Attributes (type name (required): description:
        enums.TriggerType fdlTriggerType (T):
            The type of trigger this trigger method represents.
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        enums.ResourceType resourceType (T):
            The type of the resource
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        str fdlDescription (T):
            Longform description of the trigger method, populated by the
            FDL code block.
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        List(str) fdlTriggerOptions (T):
            The trigger type option that the trigger method will be
            invoked for. Example: for a POST_MODIFY trigger type with
            the option ANYwill be invoked by any resource which is
            modified, if resource type was set to CUSTOMER only Customer
            objects would invoke the trigger method.
        enums.ResourceState resourceState (F):
            The state of the resource
        int instanceKey (T):
            A field used by scheduled triggers to manage multiple jade
            instances.
        str fdlUUID (T):
            UUID of the FDL code block to which the trigger method is
            linked.
        int fdlPriority (T):
            Order in which the trigger method will be executed. Triggers
            are called in ascending order of priority.
        str resourceName (T):
            The name of the resource
        int sortOrder (T):
            The sort order value for the given resource
        int scheduledRepeatFrequency (T):
            The frequency at which a scheduled invoke will occur. Only
            valid for a SCHEDULED TriggerType TriggerMethod
        int nextScheduledInvoke (T):
            The next scheduled invoke of this trigger method. Only valid
            for a SCHEDULED TriggerType TriggerMethod
        str resourceUUID (F):
            The UUID of the resource (read-only)
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str fdlName (T):
            The name of the FDL Code Block that contains the function
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
    """

    ALL_ATTRIBS = {'fdlTriggerType', 'resourceKey', 'resourceUUID',
                   'providers', 'resourceType', 'fdlName', 'fdlDescription',
                   'resourceMetadata', 'billingEntityName',
                   'fdlTriggerOptions', 'resourceState', 'fdlUUID',
                   'fdlPriority', 'sortOrder', 'scheduledRepeatFrequency',
                   'nextScheduledInvoke', 'resourceName', 'lastModifiedTime',
                   'billingEntityUUID', 'instanceKey', 'resourceCreateDate'}
    REQUIRED_ATTRIBS = {'fdlTriggerType', 'resourceType', 'fdlDescription',
                        'fdlTriggerOptions', 'fdlUUID', 'fdlPriority',
                        'sortOrder', 'scheduledRepeatFrequency',
                        'nextScheduledInvoke', 'resourceName', 'fdlName',
                        'instanceKey'}
    OPTIONAL_ATTRIBS = {'providers', 'resourceKey', 'resourceMetadata',
                        'billingEntityName', 'resourceState', 'resourceUUID',
                        'lastModifiedTime', 'billingEntityUUID',
                        'resourceCreateDate'}
    TYPES = {'fdlTriggerType': enums.TriggerType, 'providers':
             Dict(str, Dict(str, str)), 'resourceType': enums.ResourceType,
             'billingEntityUUID': str, 'resourceKey': List(ResourceKey),
             'resourceMetadata': ResourceMetadata, 'billingEntityName': str,
             'fdlTriggerOptions': List(str), 'resourceState':
             enums.ResourceState, 'instanceKey': int, 'fdlUUID': str,
             'fdlPriority': int, 'resourceName': str, 'sortOrder': int,
             'scheduledRepeatFrequency': int, 'nextScheduledInvoke': int,
             'resourceUUID': str, 'lastModifiedTime': int, 'fdlName': str,
             'fdlDescription': str, 'resourceCreateDate': datetime}


class MapHolder(ComplexObject):

    """FCO REST API MapHolder complex object.

    Name.

    Attributes (type name (required): description:
        Dict(GenericContainer, GenericContainer) content (T):
            The map
    """

    ALL_ATTRIBS = {'content'}
    REQUIRED_ATTRIBS = {'content'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'content': Dict(GenericContainer, GenericContainer)}


class ListResult(ComplexObject):

    """FCO REST API ListResult complex object.

    Name.

    Attributes (type name (required): description:
        int listFrom (T):
            The index of the first result returned within this result
            set
        int totalCount (T):
            The total number of results available
        List(GenericContainer) list (T):
            The result set
        int listTo (T):
            The index of the last result returned within this result set
    """

    ALL_ATTRIBS = {'listFrom', 'totalCount', 'list', 'listTo'}
    REQUIRED_ATTRIBS = {'listFrom', 'totalCount', 'list', 'listTo'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'listFrom': int, 'totalCount': int,
             'list': List(GenericContainer), 'listTo': int}


class FirewallTemplate(ComplexObject):

    """FCO REST API FirewallTemplate complex object.

    Name.

    Attributes (type name (required): description:
        List(FirewallRule) firewallOutRuleList (F):
            A list of outbound firewall rules
        str customerName (F):
            The name of the customer that owns the resource
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        str serviceNetworkUUID (F):
            The UUID of the associated service network, if applicable
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        enums.FirewallRuleAction defaultOutAction (F):
            The default outbound firewall policy when no rules are
            matched
        str deploymentInstanceUUID (F):
            The uuid of the deployment instance the resource is created
            from
        str vdcUUID (T):
            The UUID of the VDC in which the resource is contained
        str productOfferUUID (F):
            The UUID of the product offer associated with the resource
        str resourceName (T):
            The name of the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
        str productOfferName (F):
            The name of the product offer associated with the resource
        str clusterUUID (T):
            The UUID of the cluster in which the resource is located
        List(FirewallRule) firewallInRuleList (F):
            A list of inbound firewall rules
        str deploymentInstanceName (F):
            The name of the deployment instance the resource is created
            from
        str customerUUID (F):
            The UUID of the customer that owns the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        int sortOrder (T):
            The sort order value for the given resource
        str clusterName (F):
            The name of the cluster in which the resource is located
        enums.FirewallRuleAction defaultInAction (F):
            The default inbound firewall policy when no rules are
            matched
        str vdcName (F):
            The name of the VDC in which the resource is contained
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        enums.ResourceType resourceType (T):
            The type of the resource
        enums.IPType type (F):
            Whether the firewall is IPv4 or IPv6
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
    """

    ALL_ATTRIBS = {'firewallOutRuleList', 'customerName', 'providers',
                   'serviceNetworkUUID', 'resourceMetadata',
                   'billingEntityName', 'resourceState', 'defaultOutAction',
                   'deploymentInstanceUUID', 'vdcUUID', 'productOfferUUID',
                   'resourceName', 'resourceCreateDate', 'productOfferName',
                   'clusterUUID', 'firewallInRuleList',
                   'deploymentInstanceName', 'customerUUID', 'resourceUUID',
                   'billingEntityUUID', 'sortOrder', 'clusterName',
                   'defaultInAction', 'vdcName', 'lastModifiedTime',
                   'resourceType', 'type', 'resourceKey'}
    REQUIRED_ATTRIBS = {'resourceType', 'resourceName', 'clusterUUID',
                        'sortOrder', 'vdcUUID'}
    OPTIONAL_ATTRIBS = {'firewallOutRuleList', 'customerName', 'providers',
                        'serviceNetworkUUID', 'resourceMetadata',
                        'billingEntityName', 'resourceState',
                        'defaultOutAction', 'deploymentInstanceUUID',
                        'productOfferUUID', 'resourceCreateDate',
                        'productOfferName', 'firewallInRuleList',
                        'deploymentInstanceName', 'customerUUID',
                        'resourceUUID', 'type', 'clusterName',
                        'defaultInAction', 'vdcName', 'lastModifiedTime',
                        'billingEntityUUID', 'resourceKey'}
    TYPES = {'firewallOutRuleList': List(FirewallRule), 'customerName': str,
             'providers': Dict(str, Dict(str, str)), 'serviceNetworkUUID':
             str, 'resourceMetadata': ResourceMetadata, 'billingEntityName':
             str, 'resourceState': enums.ResourceState, 'defaultOutAction':
             enums.FirewallRuleAction, 'deploymentInstanceUUID': str,
             'vdcUUID': str, 'productOfferUUID': str, 'resourceName': str,
             'resourceCreateDate': datetime, 'productOfferName': str,
             'clusterUUID': str, 'firewallInRuleList': List(FirewallRule),
             'deploymentInstanceName': str, 'customerUUID': str,
             'resourceUUID': str, 'billingEntityUUID': str, 'sortOrder': int,
             'clusterName': str, 'defaultInAction': enums.FirewallRuleAction,
             'vdcName': str, 'lastModifiedTime': int, 'resourceType':
             enums.ResourceType, 'type': enums.IPType, 'resourceKey':
             List(ResourceKey)}


class ExportedFunction(ComplexObject):

    """FCO REST API ExportedFunction complex object.

    Name.

    Attributes (type name (required): description:
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        enums.ResourceType resourceType (T):
            The type of the resource
        str fdlReference (T):
            The reference of the FDL function that is to be invoked
        str fdlDescription (T):
            Longform description of the exported function, populated by
            the FDL code block.
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str fdlUUID (T):
            The UUID of the FDL Code BLock that contains the function
        str fdlFunction (T):
            The FDL function that is to be invoked
        int sortOrder (T):
            The sort order value for the given resource
        str resourceName (T):
            The name of the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
    """

    ALL_ATTRIBS = {'providers', 'resourceType', 'fdlReference',
                   'fdlDescription', 'resourceMetadata', 'billingEntityName',
                   'resourceState', 'fdlUUID', 'fdlFunction', 'sortOrder',
                   'resourceUUID', 'resourceName', 'lastModifiedTime',
                   'billingEntityUUID', 'resourceKey', 'resourceCreateDate'}
    REQUIRED_ATTRIBS = {'resourceType', 'fdlReference', 'fdlDescription',
                        'fdlUUID', 'fdlFunction', 'sortOrder', 'resourceName'}
    OPTIONAL_ATTRIBS = {'providers', 'resourceKey', 'resourceMetadata',
                        'billingEntityName', 'resourceState', 'resourceUUID',
                        'lastModifiedTime', 'billingEntityUUID',
                        'resourceCreateDate'}
    TYPES = {'providers': Dict(str, Dict(str, str)), 'resourceType':
             enums.ResourceType, 'fdlReference': str, 'fdlDescription': str,
             'resourceMetadata': ResourceMetadata, 'billingEntityName': str,
             'resourceState': enums.ResourceState, 'fdlUUID': str,
             'fdlFunction': str, 'sortOrder': int, 'resourceName': str,
             'resourceUUID': str, 'lastModifiedTime': int, 'billingEntityUUID':
             str, 'resourceKey': List(ResourceKey), 'resourceCreateDate':
             datetime}


class Job(ComplexObject):

    """FCO REST API Job complex object.

    Name.

    Attributes (type name (required): description:
        bool scheduled (T):
            Whether the job is scheduled to run at a future date
        str customerName (F):
            The name of the customer that owns the resource
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str errorCode (T):
            Holds the error code of the Error which was thrown while
            processing the job or null if the job was successful or has
            not yet completed
        str deploymentInstanceUUID (F):
            The uuid of the deployment instance the resource is created
            from
        str vdcUUID (T):
            The UUID of the VDC in which the resource is contained
        str productOfferUUID (F):
            The UUID of the product offer associated with the resource
        str resourceName (T):
            The name of the resource
        str parentJobUUID (T):
            The UUID of the parent job
        enums.JobType jobType (T):
            The type of the job
        enums.ResourceType itemType (T):
            The type of the job item
        str productOfferName (F):
            The name of the product offer associated with the resource
        str clusterUUID (T):
            The UUID of the cluster in which the resource is located
        str extendedType (T):
            Pluggable resource type for jobs on pluggable resources
        str deploymentInstanceName (F):
            The name of the deployment instance the resource is created
            from
        str itemUUID (T):
            The UUID of the resource to which the job relates
        str customerUUID (F):
            The UUID of the customer that owns the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        int sortOrder (T):
            The sort order value for the given resource
        enums.JobStatus status (T):
            The current status of the job
        str info (T):
            Information concerning the job
        str clusterName (F):
            The name of the cluster in which the resource is located
        datetime resourceCreateDate (F):
            The creation date of the resource
        str vdcName (F):
            The name of the VDC in which the resource is contained
        str itemDescription (T):
            The description of the item
        datetime startTime (T):
            The start time of the job
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str userName (T):
            The name of the user that created the job
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        str userUUID (T):
            The UUID of the user that created the job
        datetime endTime (T):
            The end time of the job, required=true
        str itemName (T):
            The name of the job item
    """

    ALL_ATTRIBS = {'status', 'customerName', 'providers', 'resourceMetadata',
                   'billingEntityName', 'resourceState', 'errorCode',
                   'deploymentInstanceUUID', 'vdcUUID', 'productOfferUUID',
                   'resourceName', 'parentJobUUID', 'jobType', 'itemType',
                   'productOfferName', 'clusterUUID', 'extendedType',
                   'deploymentInstanceName', 'itemUUID', 'customerUUID',
                   'resourceUUID', 'billingEntityUUID', 'sortOrder',
                   'scheduled', 'userName', 'clusterName',
                   'resourceCreateDate', 'vdcName', 'itemDescription',
                   'startTime', 'lastModifiedTime', 'info', 'resourceType',
                   'resourceKey', 'userUUID', 'endTime', 'itemName'}
    REQUIRED_ATTRIBS = {'status', 'scheduled', 'clusterUUID', 'itemType',
                        'resourceType', 'userName', 'itemDescription',
                        'extendedType', 'errorCode', 'info', 'itemUUID',
                        'sortOrder', 'startTime', 'vdcUUID', 'userUUID',
                        'resourceName', 'endTime', 'itemName', 'parentJobUUID',
                        'jobType'}
    OPTIONAL_ATTRIBS = {'productOfferName', 'customerName', 'providers',
                        'clusterName', 'resourceKey', 'resourceMetadata',
                        'billingEntityName', 'resourceState', 'vdcName',
                        'deploymentInstanceUUID', 'customerUUID',
                        'resourceUUID', 'productOfferUUID',
                        'deploymentInstanceName', 'lastModifiedTime',
                        'billingEntityUUID', 'resourceCreateDate'}
    TYPES = {'scheduled': bool, 'customerName': str, 'providers':
             Dict(str, Dict(str, str)), 'resourceMetadata': ResourceMetadata,
             'billingEntityName': str, 'resourceState': enums.ResourceState,
             'errorCode': str, 'deploymentInstanceUUID': str, 'vdcUUID': str,
             'productOfferUUID': str, 'resourceName': str, 'parentJobUUID':
             str, 'jobType': enums.JobType, 'itemType': enums.ResourceType,
             'productOfferName': str, 'clusterUUID': str, 'extendedType': str,
             'deploymentInstanceName': str, 'itemUUID': str, 'customerUUID':
             str, 'resourceUUID': str, 'billingEntityUUID': str, 'sortOrder':
             int, 'status': enums.JobStatus, 'info': str, 'clusterName': str,
             'resourceCreateDate': datetime, 'vdcName': str, 'itemDescription':
             str, 'startTime': datetime, 'lastModifiedTime': int, 'userName':
             str, 'resourceType': enums.ResourceType, 'resourceKey':
             List(ResourceKey), 'userUUID': str, 'endTime': datetime,
             'itemName': str}


class Translation(ComplexObject):

    """FCO REST API Translation complex object.

    Name.

    Attributes (type name (required): description:
        str valuesHash (T):
            The value of the hashed TranslationItem list
        str parentTranslationUUID (T):
            The UUID of the parent translation.
        str language (T):
            The language code associated with the translation
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        enums.ResourceType resourceType (T):
            The type of the resource
        bool editable (T):
            State if the Translation is editable.
        str region (F):
            The region code associated with the translation
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str parentTranslationName (T):
            The name of the parent translation.
        Dict(str, str) values (T):
            The un-compiled translation values
        int sortOrder (T):
            The sort order value for the given resource
        str resourceName (T):
            The name of the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
    """

    ALL_ATTRIBS = {'resourceKey', 'valuesHash', 'parentTranslationUUID',
                   'language', 'providers', 'resourceType',
                   'billingEntityName', 'region', 'resourceMetadata',
                   'editable', 'resourceState', 'values', 'sortOrder',
                   'resourceUUID', 'resourceName', 'lastModifiedTime',
                   'billingEntityUUID', 'parentTranslationName',
                   'resourceCreateDate'}
    REQUIRED_ATTRIBS = {'valuesHash', 'parentTranslationUUID', 'language',
                        'resourceType', 'editable', 'values', 'sortOrder',
                        'resourceName', 'parentTranslationName'}
    OPTIONAL_ATTRIBS = {'providers', 'resourceKey', 'resourceMetadata',
                        'billingEntityName', 'resourceState', 'resourceUUID',
                        'lastModifiedTime', 'billingEntityUUID', 'region',
                        'resourceCreateDate'}
    TYPES = {'valuesHash': str, 'parentTranslationUUID': str, 'language': str,
             'providers': Dict(str, Dict(str, str)), 'resourceType':
             enums.ResourceType, 'editable': bool, 'resourceKey':
             List(ResourceKey), 'resourceMetadata': ResourceMetadata,
             'billingEntityName': str, 'resourceState': enums.ResourceState,
             'parentTranslationName': str, 'values': Dict(str, str),
             'sortOrder': int, 'resourceName': str, 'resourceUUID': str,
             'lastModifiedTime': int, 'billingEntityUUID': str, 'region': str,
             'resourceCreateDate': datetime}


class UserDetails(ComplexObject):

    """FCO REST API UserDetails complex object.

    Name.

    Attributes (type name (required): description:
        str dayTimeNumber (F):
            The daytime telephone number associated with the user /
            contact
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str faxNumber (F):
            The fax number associated with the user / contact
        enums.UserType userType (F):
            The type of user represented by this object.
        str resourceName (T):
            The name of the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
        str eveningNumber (F):
            The evening telephone number associated with the user /
            contact
        str organisation (F):
            The organisation name associated with the user / contact
        int sortOrder (T):
            The sort order value for the given resource
        datetime lastLoginTime (F):
            The last login time associated with the user / contact
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        str email (T):
            The email address associated with the user / contact
        str resourceUUID (F):
            The UUID of the resource (read-only)
        Address address (F):
            The address details associated with the user / contact
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str mobileNumber (F):
            The mobile number associated with the user / contact
        str firstName (F):
            The first name of the contact
        bool admin (T):
            State if this is an admin user
        str lastName (F):
            The last name of the contact
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        enums.ResourceType resourceType (T):
            The type of the resource
    """

    ALL_ATTRIBS = {'dayTimeNumber', 'providers', 'resourceMetadata',
                   'billingEntityName', 'resourceState', 'faxNumber',
                   'userType', 'resourceName', 'resourceCreateDate',
                   'eveningNumber', 'organisation', 'sortOrder',
                   'resourceUUID', 'billingEntityUUID', 'email',
                   'lastLoginTime', 'address', 'lastModifiedTime',
                   'mobileNumber', 'firstName', 'admin', 'lastName',
                   'resourceKey', 'resourceType'}
    REQUIRED_ATTRIBS = {'admin', 'resourceName', 'resourceType', 'sortOrder',
                        'email'}
    OPTIONAL_ATTRIBS = {'mobileNumber', 'eveningNumber', 'dayTimeNumber',
                        'firstName', 'providers', 'lastName', 'organisation',
                        'resourceMetadata', 'billingEntityName',
                        'resourceState', 'faxNumber', 'userType', 'address',
                        'lastLoginTime', 'resourceUUID', 'lastModifiedTime',
                        'billingEntityUUID', 'resourceKey',
                        'resourceCreateDate'}
    TYPES = {'dayTimeNumber': str, 'providers': Dict(str, Dict(str, str)),
             'resourceMetadata': ResourceMetadata, 'billingEntityName': str,
             'resourceState': enums.ResourceState, 'faxNumber': str,
             'userType': enums.UserType, 'resourceName': str,
             'resourceCreateDate': datetime, 'eveningNumber': str,
             'organisation': str, 'sortOrder': int, 'lastLoginTime': datetime,
             'billingEntityUUID': str, 'email': str, 'resourceUUID': str,
             'address': Address, 'lastModifiedTime': int, 'mobileNumber': str,
             'firstName': str, 'admin': bool, 'lastName': str, 'resourceKey':
             List(ResourceKey), 'resourceType': enums.ResourceType}


class Transaction(ComplexObject):

    """FCO REST API Transaction complex object.

    Name.

    Attributes (type name (required): description:
        str publicData (T):
            Public data associated with the transaction
        str customerName (F):
            The name of the customer that owns the resource
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        int startTimestamp (T):
            A timestamp that represents the time the transaction
            started.
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str errorCode (T):
            The error code associated with the transaction
        str resourceName (T):
            The name of the resource
        str interactiveURL (T):
            The interactive url used by the transaction
        bool allowInteractive (T):
            State if the transaction allows interactivity
        datetime resourceCreateDate (F):
            The creation date of the resource
        enums.PaymentFunction transactionFunction (T):
            The function that created the transaction
        str currencyCode (T):
            The currency code associated with the transaction
        float paymentAmount (T):
            The amount associated with the transaction
        str errorReason (T):
            The error reason associated with the transaction
        enums.TransactionState state (T):
            The state of the transaction
        str customerUUID (F):
            The UUID of the customer that owns the resource
        str providerReference (T):
            The transaction reference from the associated payment
            provider
        str redirectURL (T):
            The redirect url used by the transaction
        str resourceUUID (F):
            The UUID of the resource (read-only)
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        int endTimestamp (T):
            A timestamp that represents the time the transaction ended.
        int sortOrder (T):
            The sort order value for the given resource
        str linkedTransaction (T):
            The UUID of a linked transaction.
        List(str) invoiceUUIDList (T):
            A list of UUID of associated invoices or credit notes
        Dict(str, str) redirectData (T):
            A map of redirect data used by the transaction
        str paymentMethodInstanceUUID (T):
            The UUID of the associated with the transaction
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        enums.RedirectMethod redirectMethod (F):
            The redirect method used by the transaction
        str merchantDescription (T):
            A description of the transaction.
        str paymentMethodInstanceName (T):
            The name of the associated payment method instance
    """

    ALL_ATTRIBS = {'publicData', 'customerName', 'providers', 'startTimestamp',
                   'resourceMetadata', 'billingEntityName', 'resourceState',
                   'errorCode', 'resourceName', 'interactiveURL',
                   'allowInteractive', 'resourceCreateDate',
                   'transactionFunction', 'currencyCode', 'paymentAmount',
                   'errorReason', 'state', 'customerUUID', 'providerReference',
                   'redirectURL', 'resourceUUID', 'billingEntityUUID',
                   'endTimestamp', 'sortOrder', 'linkedTransaction',
                   'invoiceUUIDList', 'redirectData',
                   'paymentMethodInstanceUUID', 'lastModifiedTime',
                   'resourceType', 'resourceKey', 'redirectMethod',
                   'merchantDescription', 'paymentMethodInstanceName'}
    REQUIRED_ATTRIBS = {'publicData', 'startTimestamp', 'errorCode',
                        'interactiveURL', 'resourceName', 'allowInteractive',
                        'transactionFunction', 'currencyCode', 'paymentAmount',
                        'errorReason', 'state', 'sortOrder', 'invoiceUUIDList',
                        'redirectURL', 'endTimestamp', 'linkedTransaction',
                        'providerReference', 'redirectData',
                        'paymentMethodInstanceUUID', 'resourceType',
                        'merchantDescription', 'paymentMethodInstanceName'}
    OPTIONAL_ATTRIBS = {'customerName', 'providers', 'resourceKey',
                        'resourceMetadata', 'billingEntityName',
                        'resourceState', 'customerUUID', 'resourceUUID',
                        'lastModifiedTime', 'billingEntityUUID',
                        'redirectMethod', 'resourceCreateDate'}
    TYPES = {'publicData': str, 'customerName': str, 'providers':
             Dict(str, Dict(str, str)), 'startTimestamp': int,
             'resourceMetadata': ResourceMetadata, 'billingEntityName': str,
             'resourceState': enums.ResourceState, 'errorCode': str,
             'resourceName': str, 'interactiveURL': str, 'allowInteractive':
             bool, 'resourceCreateDate': datetime, 'transactionFunction':
             enums.PaymentFunction, 'currencyCode': str, 'paymentAmount':
             float, 'errorReason': str, 'state': enums.TransactionState,
             'customerUUID': str, 'providerReference': str, 'redirectURL': str,
             'resourceUUID': str, 'billingEntityUUID': str, 'endTimestamp':
             int, 'sortOrder': int, 'linkedTransaction': str,
             'invoiceUUIDList': List(str), 'redirectData': Dict(str, str),
             'paymentMethodInstanceUUID': str, 'lastModifiedTime': int,
             'resourceType': enums.ResourceType, 'resourceKey':
             List(ResourceKey), 'redirectMethod': enums.RedirectMethod,
             'merchantDescription': str, 'paymentMethodInstanceName': str}


class Resource(ComplexObject):

    """FCO REST API Resource complex object.

    Name.

    Attributes (type name (required): description:
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        int sortOrder (T):
            The sort order value for the given resource
        str resourceName (T):
            The name of the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        datetime resourceCreateDate (F):
            The creation date of the resource
    """

    ALL_ATTRIBS = {'providers', 'resourceType', 'resourceKey',
                   'resourceMetadata', 'billingEntityName', 'resourceState',
                   'sortOrder', 'resourceUUID', 'resourceName',
                   'lastModifiedTime', 'billingEntityUUID',
                   'resourceCreateDate'}
    REQUIRED_ATTRIBS = {'resourceType', 'resourceName', 'sortOrder'}
    OPTIONAL_ATTRIBS = {'providers', 'resourceKey', 'resourceMetadata',
                        'billingEntityName', 'resourceState', 'resourceUUID',
                        'lastModifiedTime', 'billingEntityUUID',
                        'resourceCreateDate'}
    TYPES = {'providers': Dict(str, Dict(str, str)), 'resourceType':
             enums.ResourceType, 'resourceKey': List(ResourceKey),
             'resourceMetadata': ResourceMetadata, 'billingEntityName': str,
             'resourceState': enums.ResourceState, 'sortOrder': int,
             'resourceName': str, 'resourceUUID': str, 'lastModifiedTime': int,
             'billingEntityUUID': str, 'resourceCreateDate': datetime}


class AggregationFilter(ComplexObject):

    """FCO REST API AggregationFilter complex object.

    Name.

    Attributes (type name (required): description:
        float aggregationValue (T):
            The value that need to be evaluated
        AggregationField aggregationField (T):
            The aggregation field that needs to be filtered
        enums.Condition condition (T):
            The condition that to be used on the filter
    """

    ALL_ATTRIBS = {'aggregationValue', 'aggregationField', 'condition'}
    REQUIRED_ATTRIBS = {'aggregationValue', 'aggregationField', 'condition'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'aggregationValue': float, 'aggregationField': AggregationField,
             'condition': enums.Condition}


class SearchFilter(ComplexObject):

    """FCO REST API SearchFilter complex object.

    Name.

    Attributes (type name (required): description:
        List(FilterCondition) filterConditions (T):
            an array of filter conditions applying to this filter.
    """

    ALL_ATTRIBS = {'filterConditions'}
    REQUIRED_ATTRIBS = {'filterConditions'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'filterConditions': List(FilterCondition)}


class Snapshot(ComplexObject):

    """FCO REST API Snapshot complex object.

    Name.

    Attributes (type name (required): description:
        str customerName (F):
            The name of the customer that owns the resource
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        str parentName (F):
            The name of the object which was snapshotted
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str deploymentInstanceUUID (F):
            The uuid of the deployment instance the resource is created
            from
        str vdcUUID (T):
            The UUID of the VDC in which the resource is contained
        str productOfferUUID (F):
            The UUID of the product offer associated with the resource
        str resourceName (T):
            The name of the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
        str productOfferName (F):
            The name of the product offer associated with the resource
        str clusterUUID (T):
            The UUID of the cluster in which the resource is located
        str parentUUID (T):
            The UUID of the object which was snapshotted
        str deploymentInstanceName (F):
            The name of the deployment instance the resource is created
            from
        str customerUUID (F):
            The UUID of the customer that owns the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        int sortOrder (T):
            The sort order value for the given resource
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str clusterName (F):
            The name of the cluster in which the resource is located
        str vdcName (F):
            The name of the VDC in which the resource is contained
        enums.ResourceType parentType (F):
            The type of the object which was snapshotted
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        enums.ResourceType resourceType (T):
            The type of the resource
        enums.SnapshotType type (T):
            The type of the snapshot (disk or server)
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        List(HypervisorSetting) hypervisorSettings (F):
            The settings of the server at the time of snapshot
    """

    ALL_ATTRIBS = {'customerName', 'providers', 'parentName',
                   'billingEntityName', 'resourceState',
                   'deploymentInstanceUUID', 'vdcUUID', 'productOfferUUID',
                   'resourceName', 'resourceCreateDate', 'productOfferName',
                   'clusterUUID', 'parentUUID', 'deploymentInstanceName',
                   'customerUUID', 'resourceUUID', 'billingEntityUUID',
                   'sortOrder', 'resourceMetadata', 'clusterName', 'vdcName',
                   'parentType', 'lastModifiedTime', 'resourceType', 'type',
                   'resourceKey', 'hypervisorSettings'}
    REQUIRED_ATTRIBS = {'clusterUUID', 'resourceType', 'parentUUID',
                        'sortOrder', 'vdcUUID', 'resourceName', 'type'}
    OPTIONAL_ATTRIBS = {'productOfferName', 'resourceMetadata', 'customerName',
                        'providers', 'clusterName', 'hypervisorSettings',
                        'resourceKey', 'parentName', 'billingEntityName',
                        'resourceState', 'vdcName', 'parentType',
                        'deploymentInstanceUUID', 'customerUUID',
                        'resourceUUID', 'productOfferUUID',
                        'deploymentInstanceName', 'lastModifiedTime',
                        'billingEntityUUID', 'resourceCreateDate'}
    TYPES = {'customerName': str, 'providers': Dict(str, Dict(str, str)),
             'parentName': str, 'billingEntityName': str, 'resourceState':
             enums.ResourceState, 'deploymentInstanceUUID': str, 'vdcUUID':
             str, 'productOfferUUID': str, 'resourceName': str,
             'resourceCreateDate': datetime, 'productOfferName': str,
             'clusterUUID': str, 'parentUUID': str, 'deploymentInstanceName':
             str, 'customerUUID': str, 'resourceUUID': str,
             'billingEntityUUID': str, 'sortOrder': int, 'resourceMetadata':
             ResourceMetadata, 'clusterName': str, 'vdcName': str,
             'parentType': enums.ResourceType, 'lastModifiedTime': int,
             'resourceType': enums.ResourceType, 'type': enums.SnapshotType,
             'resourceKey': List(ResourceKey), 'hypervisorSettings':
             List(HypervisorSetting)}


class QueryLimit(ComplexObject):

    """FCO REST API QueryLimit complex object.

    Name.

    Attributes (type name (required): description:
        List(OrderedField) orderBy (F):
            The fields to sort by (including the sort order)
        int to (F):
            The index of the last field to return
        int maxRecords (F):
            The maximum number of records to return
        int from (F):
            The index of the first field to return
        bool loadChildren (T):
            Indicates whether the query should return any linked
            children (defaults to true but see Remarks below)
    """

    ALL_ATTRIBS = {'orderBy', 'to', 'maxRecords', 'from', 'loadChildren'}
    REQUIRED_ATTRIBS = {'loadChildren'}
    OPTIONAL_ATTRIBS = {'orderBy', 'to', 'maxRecords', 'from'}
    TYPES = {'orderBy': List(OrderedField), 'to': int, 'maxRecords': int,
             'from': int, 'loadChildren': bool}


class Promotion(ComplexObject):

    """FCO REST API Promotion complex object.

    Name.

    Attributes (type name (required): description:
        str productOfferName (F):
            The name of the product offer associated with the resource
        datetime startDate (T):
            The start date of the promotion code type
        datetime endDate (T):
            The end date of the promotion code type
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        bool noCardCheck (T):
            A flag to indicate whether a card check can be skipped with
            the promotion code
        int sortOrder (T):
            The sort order value for the given resource
        str resourceName (T):
            The name of the resource
        str productOfferUUID (T):
            The numeric product offer ID associated with the promotion
            code
        str resourceUUID (F):
            The UUID of the resource (read-only)
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        datetime resourceCreateDate (F):
            The creation date of the resource
    """

    ALL_ATTRIBS = {'productOfferName', 'startDate', 'endDate', 'providers',
                   'resourceType', 'resourceKey', 'resourceMetadata',
                   'billingEntityName', 'resourceState', 'noCardCheck',
                   'sortOrder', 'resourceUUID', 'productOfferUUID',
                   'resourceName', 'lastModifiedTime', 'billingEntityUUID',
                   'resourceCreateDate'}
    REQUIRED_ATTRIBS = {'startDate', 'endDate', 'resourceType', 'noCardCheck',
                        'sortOrder', 'productOfferUUID', 'resourceName'}
    OPTIONAL_ATTRIBS = {'productOfferName', 'providers', 'resourceKey',
                        'resourceMetadata', 'billingEntityName',
                        'resourceState', 'resourceUUID', 'lastModifiedTime',
                        'billingEntityUUID', 'resourceCreateDate'}
    TYPES = {'productOfferName': str, 'startDate': datetime, 'endDate':
             datetime, 'providers': Dict(str, Dict(str, str)),
             'resourceType': enums.ResourceType, 'resourceKey':
             List(ResourceKey), 'resourceMetadata': ResourceMetadata,
             'billingEntityName': str, 'resourceState': enums.ResourceState,
             'noCardCheck': bool, 'sortOrder': int, 'resourceName': str,
             'productOfferUUID': str, 'resourceUUID': str, 'lastModifiedTime':
             int, 'billingEntityUUID': str, 'resourceCreateDate': datetime}


class InvoiceSetting(ComplexObject):

    """FCO REST API InvoiceSetting complex object.

    Name.

    Attributes (type name (required): description:
        bool useDefaultNumberFormat (F):
            State if the default number format is to be used
        str decimalSeparator (T):
            The character to separate the decimal places
        enums.PdfPageSize pageSize (T):
            The paper size of the PDF version of the invoice
        str dateFormat (T):
            The date format string
        Tax tax (T):
            The tax settings
        int decimalPlace (T):
            The number of decimal places to display
        Dict(enums.InvoiceHeader, str) invoiceHeaders (T):
            A map of the invoice headers to the corresponding values to
            substitute
        str groupSeparator (T):
            The character to separate group of thousand significant
            digits
        str timeZone (T):
            The time zone
    """

    ALL_ATTRIBS = {'useDefaultNumberFormat', 'decimalSeparator', 'pageSize',
                   'dateFormat', 'tax', 'decimalPlace', 'invoiceHeaders',
                   'groupSeparator', 'timeZone'}
    REQUIRED_ATTRIBS = {'decimalSeparator', 'pageSize', 'dateFormat', 'tax',
                        'decimalPlace', 'invoiceHeaders', 'groupSeparator',
                        'timeZone'}
    OPTIONAL_ATTRIBS = {'useDefaultNumberFormat'}
    TYPES = {'useDefaultNumberFormat': bool, 'decimalSeparator': str,
             'pageSize': enums.PdfPageSize, 'dateFormat': str, 'tax': Tax,
             'decimalPlace': int, 'invoiceHeaders':
             Dict(enums.InvoiceHeader, str), 'groupSeparator': str,
             'timeZone': str}


class SSHKey(ComplexObject):

    """FCO REST API SSHKey complex object.

    Name.

    Attributes (type name (required): description:
        str customerName (F):
            The name of the customer that owns the resource
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        bool globalKey (F):
            States if the SHHKey is a global key
        str vdcUUID (T):
            The UUID of the VDC in which the resource is contained
        str productOfferUUID (F):
            The UUID of the product offer associated with the resource
        str resourceName (T):
            The name of the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
        str productOfferName (F):
            The name of the product offer associated with the resource
        str clusterUUID (T):
            The UUID of the cluster in which the resource is located
        str deploymentInstanceName (F):
            The name of the deployment instance the resource is created
            from
        str customerUUID (F):
            The UUID of the customer that owns the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        int sortOrder (T):
            The sort order value for the given resource
        str clusterName (F):
            The name of the cluster in which the resource is located
        str vdcName (F):
            The name of the VDC in which the resource is contained
        str publicKey (T):
            The public key in the same format as a line from
            authorized_keys
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str userName (F):
            The username to which the ssh key applies (or none to make
            it apply to the default initial user)
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        str deploymentInstanceUUID (F):
            The uuid of the deployment instance the resource is created
            from
        str linkedServers (F):
            The UUID of the server to which the ssh key is attached
    """

    ALL_ATTRIBS = {'customerName', 'providers', 'resourceMetadata',
                   'billingEntityName', 'resourceState', 'globalKey',
                   'vdcUUID', 'productOfferUUID', 'resourceName',
                   'resourceCreateDate', 'productOfferName', 'clusterUUID',
                   'deploymentInstanceName', 'customerUUID', 'resourceUUID',
                   'billingEntityUUID', 'sortOrder', 'clusterName', 'vdcName',
                   'publicKey', 'lastModifiedTime', 'userName', 'resourceType',
                   'resourceKey', 'deploymentInstanceUUID', 'linkedServers'}
    REQUIRED_ATTRIBS = {'clusterUUID', 'resourceType', 'publicKey',
                        'sortOrder', 'vdcUUID', 'resourceName'}
    OPTIONAL_ATTRIBS = {'productOfferName', 'userName', 'customerName',
                        'deploymentInstanceUUID', 'providers', 'clusterName',
                        'resourceKey', 'resourceMetadata', 'billingEntityName',
                        'resourceState', 'vdcName', 'linkedServers',
                        'globalKey', 'customerUUID', 'resourceUUID',
                        'productOfferUUID', 'deploymentInstanceName',
                        'lastModifiedTime', 'billingEntityUUID',
                        'resourceCreateDate'}
    TYPES = {'customerName': str, 'providers': Dict(str, Dict(str, str)),
             'resourceMetadata': ResourceMetadata, 'billingEntityName': str,
             'resourceState': enums.ResourceState, 'globalKey': bool,
             'vdcUUID': str, 'productOfferUUID': str, 'resourceName': str,
             'resourceCreateDate': datetime, 'productOfferName': str,
             'clusterUUID': str, 'deploymentInstanceName': str, 'customerUUID':
             str, 'resourceUUID': str, 'billingEntityUUID': str, 'sortOrder':
             int, 'clusterName': str, 'vdcName': str, 'publicKey': str,
             'lastModifiedTime': int, 'userName': str, 'resourceType':
             enums.ResourceType, 'resourceKey': List(ResourceKey),
             'deploymentInstanceUUID': str, 'linkedServers': str}


class Firewall(ComplexObject):

    """FCO REST API Firewall complex object.

    Name.

    Attributes (type name (required): description:
        str customerName (F):
            The name of the customer that owns the resource
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str deploymentInstanceUUID (F):
            The uuid of the deployment instance the resource is created
            from
        str vdcUUID (T):
            The UUID of the VDC in which the resource is contained
        str productOfferUUID (F):
            The UUID of the product offer associated with the resource
        str resourceName (T):
            The name of the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
        str productOfferName (F):
            The name of the product offer associated with the resource
        str clusterUUID (T):
            The UUID of the cluster in which the resource is located
        str templateName (F):
            the name of the firewall template
        str deploymentInstanceName (F):
            The name of the deployment instance the resource is created
            from
        str customerUUID (F):
            The UUID of the customer that owns the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        int sortOrder (T):
            The sort order value for the given resource
        str clusterName (F):
            The name of the cluster in which the resource is located
        str templateUUID (F):
            the UUID of the firewall template
        str vdcName (F):
            The name of the VDC in which the resource is contained
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        str ipAddress (F):
            the IP address to which the firewall is attached
    """

    ALL_ATTRIBS = {'customerName', 'providers', 'resourceMetadata',
                   'billingEntityName', 'resourceState',
                   'deploymentInstanceUUID', 'vdcUUID', 'productOfferUUID',
                   'resourceName', 'resourceCreateDate', 'productOfferName',
                   'clusterUUID', 'templateName', 'deploymentInstanceName',
                   'customerUUID', 'resourceUUID', 'billingEntityUUID',
                   'sortOrder', 'clusterName', 'templateUUID', 'vdcName',
                   'lastModifiedTime', 'resourceType', 'resourceKey',
                   'ipAddress'}
    REQUIRED_ATTRIBS = {'resourceType', 'resourceName', 'clusterUUID',
                        'sortOrder', 'vdcUUID'}
    OPTIONAL_ATTRIBS = {'productOfferName', 'templateUUID', 'customerName',
                        'providers', 'clusterName', 'ipAddress', 'resourceKey',
                        'resourceMetadata', 'billingEntityName',
                        'resourceState', 'vdcName', 'templateName',
                        'deploymentInstanceUUID', 'customerUUID',
                        'resourceUUID', 'productOfferUUID',
                        'deploymentInstanceName', 'lastModifiedTime',
                        'billingEntityUUID', 'resourceCreateDate'}
    TYPES = {'customerName': str, 'providers': Dict(str, Dict(str, str)),
             'resourceMetadata': ResourceMetadata, 'billingEntityName': str,
             'resourceState': enums.ResourceState, 'deploymentInstanceUUID':
             str, 'vdcUUID': str, 'productOfferUUID': str, 'resourceName': str,
             'resourceCreateDate': datetime, 'productOfferName': str,
             'clusterUUID': str, 'templateName': str, 'deploymentInstanceName':
             str, 'customerUUID': str, 'resourceUUID': str,
             'billingEntityUUID': str, 'sortOrder': int, 'clusterName': str,
             'templateUUID': str, 'vdcName': str, 'lastModifiedTime': int,
             'resourceType': enums.ResourceType, 'resourceKey':
             List(ResourceKey), 'ipAddress': str}


class Image(ComplexObject):

    """FCO REST API Image complex object.

    Name.

    Attributes (type name (required): description:
        str customerName (F):
            The name of the customer that owns the resource
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        str snapshotUUID (F):
            The UUID of the snapshot from which the image was derived
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str customerValidString (F):
            The image's customer validation data
        str deploymentInstanceUUID (F):
            The uuid of the deployment instance the resource is created
            from
        List(HypervisorSetting) hypervisorSettings (F):
            The hypervisor settings defined for this image
        str vdcUUID (T):
            The UUID of the VDC in which the resource is contained
        str productOfferUUID (F):
            The UUID of the product offer associated with the resource
        str resourceName (T):
            The name of the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
        int size (F):
            The size of the image
        str productOfferName (F):
            The name of the product offer associated with the resource
        str clusterUUID (T):
            The UUID of the cluster in which the resource is located
        str osChargeProductOfferUUID (F):
            The UUID of the product offer used to charge for the image
        str deploymentInstanceName (F):
            The name of the deployment instance the resource is created
            from
        str customerUUID (F):
            The UUID of the customer that owns the resource
        bool vmSupport (T):
            Indicate if the image supports virtual machines
        str resourceUUID (F):
            The UUID of the resource (read-only)
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        enums.ImageType imageType (F):
            The type of image concerned (disk or server)
        int sortOrder (T):
            The sort order value for the given resource
        bool genPassword (F):
            A flag indicating whether a password should be generated
            when this image is used
        str clusterName (F):
            The name of the cluster in which the resource is located
        str vdcName (F):
            The name of the VDC in which the resource is contained
        str defaultUser (F):
            The default user for a server created using this image
        ImagePermission ownerPermission (F):
            The owner image permissions
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str osChargeProductOfferName (F):
            The name of the product offer used to charge for the image
        List(HypervisorSetting) defaultSettings (F):
            The combined hypervisor settings defined for this image and
            cluster
        enums.ResourceType resourceType (T):
            The type of the resource
        str baseName (F):
            The name of the resource from which the image was derived
        List(PublishTo) publishedTo (F):
            A list of UUIDs to whom the image is published
        ImagePermission userPermission (F):
            The user image permissions
        str baseUUID (T):
            The UUID of the resource from which the image was derived
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        bool ctSupport (T):
            Indicate if the image supports containers
    """

    ALL_ATTRIBS = {'customerName', 'providers', 'snapshotUUID',
                   'resourceMetadata', 'billingEntityName', 'resourceState',
                   'customerValidString', 'deploymentInstanceUUID',
                   'publishedTo', 'vdcUUID', 'productOfferUUID',
                   'resourceName', 'resourceCreateDate', 'size',
                   'productOfferName', 'clusterUUID', 'userPermission',
                   'deploymentInstanceName', 'customerUUID', 'vmSupport',
                   'resourceUUID', 'billingEntityUUID', 'imageType',
                   'sortOrder', 'genPassword', 'clusterName', 'vdcName',
                   'defaultUser', 'ownerPermission', 'lastModifiedTime',
                   'osChargeProductOfferName', 'defaultSettings',
                   'resourceType', 'baseName', 'hypervisorSettings',
                   'osChargeProductOfferUUID', 'baseUUID', 'resourceKey',
                   'ctSupport'}
    REQUIRED_ATTRIBS = {'clusterUUID', 'resourceType', 'vmSupport',
                        'sortOrder', 'vdcUUID', 'resourceName', 'baseUUID',
                        'ctSupport'}
    OPTIONAL_ATTRIBS = {'customerName', 'providers', 'snapshotUUID',
                        'resourceMetadata', 'billingEntityName',
                        'resourceState', 'customerValidString',
                        'deploymentInstanceUUID', 'hypervisorSettings',
                        'productOfferUUID', 'resourceCreateDate', 'size',
                        'productOfferName', 'osChargeProductOfferUUID',
                        'deploymentInstanceName', 'customerUUID',
                        'resourceUUID', 'billingEntityUUID', 'imageType',
                        'genPassword', 'clusterName', 'vdcName', 'defaultUser',
                        'ownerPermission', 'lastModifiedTime',
                        'osChargeProductOfferName', 'defaultSettings',
                        'baseName', 'publishedTo', 'userPermission',
                        'resourceKey'}
    TYPES = {'customerName': str, 'providers': Dict(str, Dict(str, str)),
             'snapshotUUID': str, 'resourceMetadata': ResourceMetadata,
             'billingEntityName': str, 'resourceState': enums.ResourceState,
             'customerValidString': str, 'deploymentInstanceUUID': str,
             'hypervisorSettings': List(HypervisorSetting), 'vdcUUID': str,
             'productOfferUUID': str, 'resourceName': str,
             'resourceCreateDate': datetime, 'size': int, 'productOfferName':
             str, 'clusterUUID': str, 'osChargeProductOfferUUID': str,
             'deploymentInstanceName': str, 'customerUUID': str, 'vmSupport':
             bool, 'resourceUUID': str, 'billingEntityUUID': str, 'imageType':
             enums.ImageType, 'sortOrder': int, 'genPassword': bool,
             'clusterName': str, 'vdcName': str, 'defaultUser': str,
             'ownerPermission': ImagePermission, 'lastModifiedTime': int,
             'osChargeProductOfferName': str, 'defaultSettings':
             List(HypervisorSetting), 'resourceType': enums.ResourceType,
             'baseName': str, 'publishedTo': List(PublishTo), 'userPermission':
             ImagePermission, 'baseUUID': str, 'resourceKey':
             List(ResourceKey), 'ctSupport': bool}


class CustomerEmail(ComplexObject):

    """FCO REST API CustomerEmail complex object.

    Name.

    Attributes (type name (required): description:
        List(str) sendToEmail (F):
            The list of email addresses to whom the email is to be sent;
            this features can only be used by MBEs
        List(EmailBlock) emailBlocks (F):
            The list of email blocks
        Dict(enums.EmailVAR, str) emailSettingDetails (F):
            The settings for the email
        enums.EmailType emailType (T):
            The type of the email
        str customerUUID (T):
            The UUID of the customer that is the recipient of the email
        List(str) sendTo (F):
            The list of user UUIDs to send email to. If no UUID is
            specified, then the email would be sent to the whole of the
            admin group of the customer concerned.
        Dict(str, str) attachments (F):
            The attachments to the email
    """

    ALL_ATTRIBS = {'sendToEmail', 'emailBlocks', 'emailSettingDetails',
                   'emailType', 'customerUUID', 'sendTo', 'attachments'}
    REQUIRED_ATTRIBS = {'emailType', 'customerUUID'}
    OPTIONAL_ATTRIBS = {'sendToEmail', 'emailBlocks', 'attachments',
                        'emailSettingDetails', 'sendTo'}
    TYPES = {'sendToEmail': List(str), 'emailBlocks': List(EmailBlock),
             'emailSettingDetails': Dict(enums.EmailVAR, str), 'emailType':
             enums.EmailType, 'customerUUID': str, 'sendTo': List(str),
             'attachments': Dict(str, str)}


class FDLCodeBlock(ComplexObject):

    """FCO REST API FDLCodeBlock complex object.

    Name.

    Attributes (type name (required): description:
        str signedCodeBlock (F):
            Holds the actual signed script data. This can not be used
            with FQL
        str signatoryUUID (F):
            Holds the UUID of the customer which initiated the signing
            of the code block
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        enums.ResourceType resourceType (T):
            The type of the resource
        bool editable (F):
            Indicates whether the code block may be modified
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        datetime signingTimestamp (F):
            Holds the timestamp at which the code was signed
        Dict(str, str) fdlProviderInfo (F):
            A map of the provider information for the FDL Code Block
        str resourceName (T):
            The name of the resource
        str unsignedCodeBlock (F):
            Holds the actual unsigned script data. This can not be used
            with FQL
        str resourceUUID (F):
            The UUID of the resource (read-only)
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        str fdlHash (F):
            A unique hash representing the current state of the FDL Code
            Block
        datetime resourceCreateDate (F):
            The creation date of the resource
        int sortOrder (T):
            The sort order value for the given resource
    """

    ALL_ATTRIBS = {'signedCodeBlock', 'signatoryUUID', 'providers',
                   'resourceType', 'billingEntityName', 'resourceKey',
                   'resourceMetadata', 'editable', 'resourceState',
                   'signingTimestamp', 'resourceCreateDate', 'resourceUUID',
                   'unsignedCodeBlock', 'resourceName', 'lastModifiedTime',
                   'billingEntityUUID', 'fdlHash', 'fdlProviderInfo',
                   'sortOrder'}
    REQUIRED_ATTRIBS = {'resourceType', 'resourceName', 'sortOrder'}
    OPTIONAL_ATTRIBS = {'signedCodeBlock', 'signatoryUUID', 'providers',
                        'editable', 'resourceKey', 'resourceMetadata',
                        'billingEntityName', 'resourceState',
                        'signingTimestamp', 'fdlProviderInfo',
                        'unsignedCodeBlock', 'resourceUUID',
                        'lastModifiedTime', 'billingEntityUUID', 'fdlHash',
                        'resourceCreateDate'}
    TYPES = {'signedCodeBlock': str, 'signatoryUUID': str, 'providers':
             Dict(str, Dict(str, str)), 'resourceType': enums.ResourceType,
             'editable': bool, 'resourceKey': List(ResourceKey),
             'resourceMetadata': ResourceMetadata, 'billingEntityName': str,
             'resourceState': enums.ResourceState, 'signingTimestamp':
             datetime, 'fdlProviderInfo': Dict(str, str), 'resourceName': str,
             'unsignedCodeBlock': str, 'resourceUUID': str, 'lastModifiedTime':
             int, 'billingEntityUUID': str, 'fdlHash': str,
             'resourceCreateDate': datetime, 'sortOrder': int}


class CreditNote(ComplexObject):

    """FCO REST API CreditNote complex object.

    Name.

    Attributes (type name (required): description:
        float taxRate (F):
            The tax rate of the invoice
        str customerName (F):
            The name associated with the invoice
        int invoiceDate (T):
            The date of the invoice as printed on the invoice
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        int cutOffDate (F):
            The invoice cut off date (UNIX TIMESTAMP)
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str customerVatNo (F):
            The VAT number or tax reference of the customer / recipient
            of the invoice
        bool testMode (F):
            The test mode
        str resourceName (T):
            The name of the resource
        int dueDate (F):
            The invoice due date (UNIX TIMESTAMP)
        datetime resourceCreateDate (F):
            The creation date of the resource
        int paidDate (F):
            The UNIX TIMESTAMP when invoice was paid
        float invoiceTaxAmt (F):
            The amount of tax associated with the invoice
        int currencyId (F):
            The currency id of the invoice
        int sortOrder (T):
            The sort order value for the given resource
        str transactionUUID (F):
            The UUID of the transaction
        str resourceUUID (F):
            The UUID of the resource (read-only)
        List(InvoiceItem) invoiceItems (F):
            The invoice items
        float invoiceTotalInc (F):
            The invoice total including tax
        str customerUUID (T):
            The UUID of the customer
        enums.InvoiceStatus status (F):
            The invoice status
        str billingEntityVatNo (F):
            The VAT number or tax reference of the billing entity /
            invoicing party
        Address customerAddress (F):
            The customer address field
        float invoiceTotalExc (F):
            The invoice total excluding tax
        str pdfRef (F):
            The PDF reference of the invoice
        Address billingAddress (F):
            The billing address of the invoice
        str paymentMethodInstanceUUID (F):
            The payment method instance uuid
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        int invoiceNo (F):
            The invoice number
        enums.ResourceType resourceType (T):
            The type of the resource
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        str paymentMethodInstanceName (F):
            The name of the associated FDL code Payment Method
        str pdf (F):
            The pdf format of the invoice
        bool creditNote (F):
            The boolean to indicate credit note
    """

    ALL_ATTRIBS = {'taxRate', 'customerName', 'invoiceDate', 'providers',
                   'cutOffDate', 'resourceMetadata', 'billingEntityName',
                   'resourceState', 'customerVatNo', 'testMode',
                   'resourceName', 'dueDate', 'resourceCreateDate', 'paidDate',
                   'invoiceTaxAmt', 'currencyId', 'customerUUID',
                   'transactionUUID', 'resourceUUID', 'invoiceItems',
                   'invoiceTotalInc', 'sortOrder', 'status',
                   'billingEntityVatNo', 'customerAddress', 'invoiceTotalExc',
                   'pdfRef', 'billingAddress', 'paymentMethodInstanceUUID',
                   'lastModifiedTime', 'invoiceNo', 'resourceType',
                   'billingEntityUUID', 'resourceKey',
                   'paymentMethodInstanceName', 'pdf', 'creditNote'}
    REQUIRED_ATTRIBS = {'resourceType', 'resourceName', 'customerUUID',
                        'invoiceDate', 'sortOrder'}
    OPTIONAL_ATTRIBS = {'taxRate', 'customerName', 'paidDate', 'providers',
                        'cutOffDate', 'resourceMetadata', 'billingEntityName',
                        'resourceState', 'customerVatNo', 'testMode',
                        'dueDate', 'resourceCreateDate', 'invoiceTaxAmt',
                        'currencyId', 'transactionUUID', 'resourceUUID',
                        'invoiceItems', 'invoiceTotalInc', 'status',
                        'billingEntityVatNo', 'customerAddress',
                        'invoiceTotalExc', 'pdfRef', 'billingAddress',
                        'paymentMethodInstanceUUID', 'lastModifiedTime',
                        'invoiceNo', 'billingEntityUUID', 'resourceKey',
                        'paymentMethodInstanceName', 'pdf', 'creditNote'}
    TYPES = {'taxRate': float, 'customerName': str, 'invoiceDate': int,
             'providers': Dict(str, Dict(str, str)), 'cutOffDate': int,
             'resourceMetadata': ResourceMetadata, 'billingEntityName': str,
             'resourceState': enums.ResourceState, 'customerVatNo': str,
             'testMode': bool, 'resourceName': str, 'dueDate': int,
             'resourceCreateDate': datetime, 'paidDate': int, 'invoiceTaxAmt':
             float, 'currencyId': int, 'sortOrder': int, 'transactionUUID':
             str, 'resourceUUID': str, 'invoiceItems': List(InvoiceItem),
             'invoiceTotalInc': float, 'customerUUID': str, 'status':
             enums.InvoiceStatus, 'billingEntityVatNo': str, 'customerAddress':
             Address, 'invoiceTotalExc': float, 'pdfRef': str,
             'billingAddress': Address, 'paymentMethodInstanceUUID': str,
             'lastModifiedTime': int, 'invoiceNo': int, 'resourceType':
             enums.ResourceType, 'billingEntityUUID': str, 'resourceKey':
             List(ResourceKey), 'paymentMethodInstanceName': str, 'pdf': str,
             'creditNote': bool}


class Invoice(ComplexObject):

    """FCO REST API Invoice complex object.

    Name.

    Attributes (type name (required): description:
        float taxRate (F):
            The tax rate of the invoice
        str customerName (F):
            The name associated with the invoice
        int invoiceDate (T):
            The date of the invoice as printed on the invoice
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        int cutOffDate (F):
            The invoice cut off date (UNIX TIMESTAMP)
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str customerVatNo (F):
            The VAT number or tax reference of the customer / recipient
            of the invoice
        bool testMode (F):
            The test mode
        str resourceName (T):
            The name of the resource
        int dueDate (F):
            The invoice due date (UNIX TIMESTAMP)
        datetime resourceCreateDate (F):
            The creation date of the resource
        int paidDate (F):
            The UNIX TIMESTAMP when invoice was paid
        float invoiceTaxAmt (F):
            The amount of tax associated with the invoice
        int currencyId (F):
            The currency id of the invoice
        int sortOrder (T):
            The sort order value for the given resource
        str transactionUUID (F):
            The UUID of the transaction
        str resourceUUID (F):
            The UUID of the resource (read-only)
        List(InvoiceItem) invoiceItems (F):
            The invoice items
        float invoiceTotalInc (F):
            The invoice total including tax
        str customerUUID (T):
            The UUID of the customer
        enums.InvoiceStatus status (F):
            The invoice status
        str billingEntityVatNo (F):
            The VAT number or tax reference of the billing entity /
            invoicing party
        Address customerAddress (F):
            The customer address field
        float invoiceTotalExc (F):
            The invoice total excluding tax
        str pdfRef (F):
            The PDF reference of the invoice
        Address billingAddress (F):
            The billing address of the invoice
        str paymentMethodInstanceUUID (F):
            The payment method instance uuid
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        int invoiceNo (F):
            The invoice number
        enums.ResourceType resourceType (T):
            The type of the resource
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        str paymentMethodInstanceName (F):
            The name of the associated FDL code Payment Method
        str pdf (F):
            The pdf format of the invoice
        bool creditNote (F):
            The boolean to indicate credit note
    """

    ALL_ATTRIBS = {'taxRate', 'customerName', 'invoiceDate', 'providers',
                   'cutOffDate', 'resourceMetadata', 'billingEntityName',
                   'resourceState', 'customerVatNo', 'testMode',
                   'resourceName', 'dueDate', 'resourceCreateDate', 'paidDate',
                   'invoiceTaxAmt', 'currencyId', 'customerUUID',
                   'transactionUUID', 'resourceUUID', 'invoiceItems',
                   'invoiceTotalInc', 'sortOrder', 'status',
                   'billingEntityVatNo', 'customerAddress', 'invoiceTotalExc',
                   'pdfRef', 'billingAddress', 'paymentMethodInstanceUUID',
                   'lastModifiedTime', 'invoiceNo', 'resourceType',
                   'billingEntityUUID', 'resourceKey',
                   'paymentMethodInstanceName', 'pdf', 'creditNote'}
    REQUIRED_ATTRIBS = {'resourceType', 'resourceName', 'customerUUID',
                        'invoiceDate', 'sortOrder'}
    OPTIONAL_ATTRIBS = {'taxRate', 'customerName', 'paidDate', 'providers',
                        'cutOffDate', 'resourceMetadata', 'billingEntityName',
                        'resourceState', 'customerVatNo', 'testMode',
                        'dueDate', 'resourceCreateDate', 'invoiceTaxAmt',
                        'currencyId', 'transactionUUID', 'resourceUUID',
                        'invoiceItems', 'invoiceTotalInc', 'status',
                        'billingEntityVatNo', 'customerAddress',
                        'invoiceTotalExc', 'pdfRef', 'billingAddress',
                        'paymentMethodInstanceUUID', 'lastModifiedTime',
                        'invoiceNo', 'billingEntityUUID', 'resourceKey',
                        'paymentMethodInstanceName', 'pdf', 'creditNote'}
    TYPES = {'taxRate': float, 'customerName': str, 'invoiceDate': int,
             'providers': Dict(str, Dict(str, str)), 'cutOffDate': int,
             'resourceMetadata': ResourceMetadata, 'billingEntityName': str,
             'resourceState': enums.ResourceState, 'customerVatNo': str,
             'testMode': bool, 'resourceName': str, 'dueDate': int,
             'resourceCreateDate': datetime, 'paidDate': int, 'invoiceTaxAmt':
             float, 'currencyId': int, 'sortOrder': int, 'transactionUUID':
             str, 'resourceUUID': str, 'invoiceItems': List(InvoiceItem),
             'invoiceTotalInc': float, 'customerUUID': str, 'status':
             enums.InvoiceStatus, 'billingEntityVatNo': str, 'customerAddress':
             Address, 'invoiceTotalExc': float, 'pdfRef': str,
             'billingAddress': Address, 'paymentMethodInstanceUUID': str,
             'lastModifiedTime': int, 'invoiceNo': int, 'resourceType':
             enums.ResourceType, 'billingEntityUUID': str, 'resourceKey':
             List(ResourceKey), 'paymentMethodInstanceName': str, 'pdf': str,
             'creditNote': bool}


class KeyList(ComplexObject):

    """FCO REST API KeyList complex object.

    Name.

    Attributes (type name (required): description:
        Dict(str, JadeList) content (F):
            The map from key name to a list of values
        List(ResourceKey) keyContent (F):
            A list of ResourceKey objects
    """

    ALL_ATTRIBS = {'content', 'keyContent'}
    REQUIRED_ATTRIBS = set()
    OPTIONAL_ATTRIBS = {'content', 'keyContent'}
    TYPES = {'content': Dict(str, JadeList), 'keyContent': List(ResourceKey)}


class Disk(ComplexObject):

    """FCO REST API Disk complex object.

    Name.

    Attributes (type name (required): description:
        str customerName (F):
            The name of the customer that owns the resource
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        str snapshotUUID (F):
            The UUID of the snapshot from which the disk was derived
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str deploymentInstanceUUID (F):
            The uuid of the deployment instance the resource is created
            from
        str storageGroupUUID (F):
            The storage group UUID
        str productOfferUUID (F):
            The UUID of the product offer associated with the resource
        str resourceName (T):
            The name of the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
        int size (T):
            The capacity of the disk
        str productOfferName (F):
            The name of the product offer associated with the resource
        int index (F):
            The index of the disk (zero-based) specifying its position
            within the server to which it is attached
        str clusterUUID (T):
            The UUID of the cluster in which the resource is located
        str snapshotName (F):
            The name of the snapshot from which the disk was derived
        str serverName (F):
            The name of the server to which the disk is attached
        str storageUnitName (F):
            The name of the storage unit, This will only be accessible
            to MBE admins
        str imageName (F):
            The name of the OS image from which the disk was derived
        str customerUUID (F):
            The UUID of the customer that owns the resource
        str imageUUID (F):
            The UUID of the OS Image from which the disk was derived
        str resourceUUID (F):
            The UUID of the resource (read-only)
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        int sortOrder (T):
            The sort order value for the given resource
        enums.DiskStatus status (F):
            The status of the disk
        str clusterName (F):
            The name of the cluster in which the resource is located
        str storageGroupName (F):
            The storage group Name
        str vdcName (F):
            The name of the VDC in which the resource is contained
        str vdcUUID (T):
            The UUID of the VDC in which the resource is contained
        str deploymentInstanceName (F):
            The name of the deployment instance the resource is created
            from
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        List(enums.StorageCapability) storageCapabilities (T):
            A set of the storage capabilities of the disk.
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        str serverUUID (F):
            The UUID of the server to which the disk is attached
        bool iso (T):
            Indicate if the disk in a iso or not
        str storageUnitUUID (F):
            The UUID of the storage unit, This will only be accessible
            to MBE admins
    """

    ALL_ATTRIBS = {'customerName', 'providers', 'snapshotUUID',
                   'resourceMetadata', 'billingEntityName', 'resourceState',
                   'deploymentInstanceUUID', 'storageGroupUUID',
                   'productOfferUUID', 'resourceName', 'resourceCreateDate',
                   'size', 'productOfferName', 'index', 'clusterUUID',
                   'snapshotName', 'serverName', 'storageUnitName',
                   'imageName', 'customerUUID', 'imageUUID', 'resourceUUID',
                   'billingEntityUUID', 'sortOrder', 'status', 'clusterName',
                   'storageGroupName', 'vdcName', 'vdcUUID',
                   'deploymentInstanceName', 'lastModifiedTime',
                   'storageCapabilities', 'resourceType', 'resourceKey',
                   'serverUUID', 'iso', 'storageUnitUUID'}
    REQUIRED_ATTRIBS = {'storageCapabilities', 'clusterUUID', 'resourceType',
                        'iso', 'sortOrder', 'vdcUUID', 'resourceName', 'size'}
    OPTIONAL_ATTRIBS = {'customerName', 'providers', 'snapshotUUID',
                        'resourceMetadata', 'billingEntityName',
                        'resourceState', 'deploymentInstanceUUID',
                        'productOfferUUID', 'storageGroupUUID',
                        'resourceCreateDate', 'productOfferName', 'index',
                        'snapshotName', 'serverName', 'storageUnitName',
                        'imageName', 'customerUUID', 'imageUUID',
                        'resourceUUID', 'billingEntityUUID', 'status',
                        'clusterName', 'storageGroupName', 'vdcName',
                        'deploymentInstanceName', 'lastModifiedTime',
                        'resourceKey', 'serverUUID', 'storageUnitUUID'}
    TYPES = {'customerName': str, 'providers': Dict(str, Dict(str, str)),
             'snapshotUUID': str, 'resourceMetadata': ResourceMetadata,
             'billingEntityName': str, 'resourceState': enums.ResourceState,
             'deploymentInstanceUUID': str, 'storageGroupUUID': str,
             'productOfferUUID': str, 'resourceName': str,
             'resourceCreateDate': datetime, 'size': int, 'productOfferName':
             str, 'index': int, 'clusterUUID': str, 'snapshotName': str,
             'serverName': str, 'storageUnitName': str, 'imageName': str,
             'customerUUID': str, 'imageUUID': str, 'resourceUUID': str,
             'billingEntityUUID': str, 'sortOrder': int, 'status':
             enums.DiskStatus, 'clusterName': str, 'storageGroupName': str,
             'vdcName': str, 'vdcUUID': str, 'deploymentInstanceName': str,
             'lastModifiedTime': int, 'storageCapabilities':
             List(enums.StorageCapability), 'resourceType': enums.ResourceType,
             'resourceKey': List(ResourceKey), 'serverUUID': str, 'iso': bool,
             'storageUnitUUID': str}


class CustomerDetails(ComplexObject):

    """FCO REST API CustomerDetails complex object.

    Name.

    Attributes (type name (required): description:
        str organisationName (F):
            The organisation name for the customer
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str productOfferUUID (T):
            The UUID of the product offer associated with the resource
        str resourceName (T):
            The name of the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
        str productOfferName (T):
            The name of the product offer associated with the resource
        str validatedString (T):
            The Validated string of the customer
        bool exceedCreditLimit (T):
            Boolean indicating if customer exceeds the credit limit
        str promotionName (F):
            The name of the promotion last associated with the resource
        float carryOverBalance (T):
            The customer's current carry-over unit balance
        str customerUUID (T):
            The UUID of the customer (which will be the same as the
            resource UUID)
        str promotionUUID (T):
            The UUID of the promotion last associated with the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        float nonCarryOverBalance (T):
            The customer's current non-carry-over unit balance
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        str email (F):
            The email address associated with the user / contact
        int sortOrder (T):
            The sort order value for the given resource
        enums.Status status (T):
            The status of the customer (determining whether it is active
            etc.)
        List(UserDetails) users (F):
            The users/contacts associated with the customer
        bool exceedCutoffLimit (T):
            Boolean indicating if customer exceeds the cuoff limit
        Dict(enums.Limits, int) limitsMap (T):
            A map containing the system limitations of the customer
        bool vatExempt (F):
            The VAT exemption status of the customer
        List(Group) groups (F):
            The groups associated with the customer
        Address address (F):
            The address details of the customer
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        bool customerCardCheck (F):
            A flag to indicate whether the customer requires credit card
            checks
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        str vatNumber (F):
            The VAT number or tax reference for the customer
        enums.PaymentType creditCustomer (T):
            A flag to indicate whether the customer has a credit account
        str timeZone (F):
            The timezone associated with the customer
        float warningLevel (F):
            The unit level below which which a low balance warning
            should be sent
        bool warningSent (F):
            A flag to indicate the low balance warning has already been
            sent
    """

    ALL_ATTRIBS = {'organisationName', 'providers', 'resourceMetadata',
                   'billingEntityName', 'resourceState', 'productOfferUUID',
                   'resourceName', 'resourceCreateDate', 'productOfferName',
                   'validatedString', 'exceedCreditLimit', 'promotionName',
                   'carryOverBalance', 'customerUUID', 'promotionUUID',
                   'resourceUUID', 'nonCarryOverBalance', 'billingEntityUUID',
                   'email', 'sortOrder', 'status', 'users', 'limitsMap',
                   'vatExempt', 'groups', 'address', 'lastModifiedTime',
                   'customerCardCheck', 'resourceType', 'resourceKey',
                   'vatNumber', 'creditCustomer', 'timeZone',
                   'exceedCutoffLimit', 'warningLevel', 'warningSent'}
    REQUIRED_ATTRIBS = {'productOfferName', 'status', 'validatedString',
                        'promotionUUID', 'resourceType', 'exceedCreditLimit',
                        'limitsMap', 'carryOverBalance', 'customerUUID',
                        'exceedCutoffLimit', 'productOfferUUID',
                        'resourceName', 'nonCarryOverBalance',
                        'creditCustomer', 'sortOrder'}
    OPTIONAL_ATTRIBS = {'organisationName', 'users', 'providers',
                        'resourceKey', 'resourceMetadata', 'billingEntityName',
                        'vatExempt', 'resourceState', 'warningSent',
                        'promotionName', 'customerCardCheck', 'warningLevel',
                        'groups', 'address', 'timeZone', 'resourceUUID',
                        'lastModifiedTime', 'billingEntityUUID', 'email',
                        'resourceCreateDate', 'vatNumber'}
    TYPES = {'organisationName': str, 'providers': Dict(str, Dict(str, str)),
             'resourceMetadata': ResourceMetadata, 'billingEntityName': str,
             'resourceState': enums.ResourceState, 'productOfferUUID': str,
             'resourceName': str, 'resourceCreateDate': datetime,
             'productOfferName': str, 'validatedString': str,
             'exceedCreditLimit': bool, 'promotionName': str,
             'carryOverBalance': float, 'customerUUID': str, 'promotionUUID':
             str, 'resourceUUID': str, 'nonCarryOverBalance': float,
             'billingEntityUUID': str, 'email': str, 'sortOrder': int,
             'status': enums.Status, 'users': List(UserDetails),
             'exceedCutoffLimit': bool, 'limitsMap': Dict(enums.Limits, int),
             'vatExempt': bool, 'groups': List(Group), 'address': Address,
             'lastModifiedTime': int, 'customerCardCheck': bool,
             'resourceType': enums.ResourceType, 'resourceKey':
             List(ResourceKey), 'vatNumber': str, 'creditCustomer':
             enums.PaymentType, 'timeZone': str, 'warningLevel': float,
             'warningSent': bool}


class Permission(ComplexObject):

    """FCO REST API Permission complex object.

    Name.

    Attributes (type name (required): description:
        enums.Capability capability (T):
            The capability concerned (i.e. the action which this
            permission tuple mediates)
        Resource permittedResource (T):
            The resource to which the permission tuple applies (read
            only)
        SimpleResource permittedTo (T):
            The User/Group to witch permission applies to
        bool permitted (T):
            Whether the action is to be permitted or denied
        enums.ResourceType resourceType (T):
            The type of the resource concerned (i.e. the type of object
            which this permission tuple mediates)
    """

    ALL_ATTRIBS = {'capability', 'permittedResource', 'permittedTo',
                   'permitted', 'resourceType'}
    REQUIRED_ATTRIBS = {'capability', 'permittedResource', 'permittedTo',
                        'permitted', 'resourceType'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'capability': enums.Capability, 'permittedResource': Resource,
             'permittedTo': SimpleResource, 'permitted': bool, 'resourceType':
             enums.ResourceType}


class IP(ComplexObject):

    """FCO REST API IP complex object.

    Name.

    Attributes (type name (required): description:
        str ipAddress (T):
            The IP address
        Firewall firewall (T):
            A firewall object to be passed when the IP address, This is
            only used at create time
        bool auto (F):
            A flag indicating whether the IP address is to be
            automatically assigned to the server (by DHCP or SLAAC)
        int prifixLegth (T):
            The prefix length of the ip
        str subnetUUID (F):
            The UUID of the subnet object in which the IP address is
            located
        enums.IPType type (T):
            The type of the IP address (IPv4 or IPv6)
        str nicUUID (F):
            The UUID of the NIC to which the IP address is attached
        str gatewayAddress (T):
            The default gateway address
    """

    ALL_ATTRIBS = {'firewall', 'auto', 'prifixLegth', 'subnetUUID', 'nicUUID',
                   'type', 'ipAddress', 'gatewayAddress'}
    REQUIRED_ATTRIBS = {'firewall', 'ipAddress', 'prifixLegth', 'type',
                        'gatewayAddress'}
    OPTIONAL_ATTRIBS = {'auto', 'subnetUUID', 'nicUUID'}
    TYPES = {'gatewayAddress': str, 'firewall': Firewall, 'auto': bool,
             'prifixLegth': int, 'subnetUUID': str, 'type': enums.IPType,
             'nicUUID': str, 'ipAddress': str}


class BillingEntityDetails(ComplexObject):

    """FCO REST API BillingEntityDetails complex object.

    Name.

    Attributes (type name (required): description:
        str parentUUID (F):
            The UUID of the immediate parent billing entity of this
            billing entity
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        str parentName (F):
            The name of the immediate parent billing entity of this
            billing entity
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        Currency currency (F):
            The currency object associated with the Billing Entity.
        str resourceName (T):
            The name of the resource
        str adminControlPanelURL (F):
            The admin control panel URL of the Billing Entity
        float no3ds28DaySpendLimit (F):
            The default monthly spend limit (in currency terms)
            associated with the Billing Entity for a non-3DS transaction
        datetime resourceCreateDate (F):
            The creation date of the resource
        str controlPanelURL (F):
            The public facing URL of the control panel for the Billing
            Entity
        int currencyId (T):
            The numeric currency ID associated with the Billing Entity
        Dict(enums.BillingEntityVAR, str) standardEmailSettings (F):
            Map of email settings for the Billing Entity
        List(enums.ResourceType) permittedPOResourceTypes (F):
            This holds lists of resource types which are allowed for a
            product offer to add/modify/delete
        int sortOrder (T):
            The sort order value for the given resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        InvoiceSetting invoiceSetting (F):
            The invoice settings used by the billing entity.
        bool enableUserEditing (F):
            Flag to enable editing of users
        enums.BillingType billingType (F):
            The type of the billing entity
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str description (F):
            The textual description of the Billing Entity
        List(str) descendants (F):
            A list of the uuids of all billing entities that descend
            from this billing entity
        int brand (F):
            The numeric ID of the brand associated with the Billing
            Entity
        Address address (F):
            The address details associated with the Billing Entity
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        Dict(enums.EmailType, EmailTemplate) emailTemplates (F):
            Map of email templates for the Billing Entity
        SystemCapabilitySet systemCapabilities (F):
            The system capabilities attached to this billing entity
            (note that it is not possible to filter by this field)
        float overall28DaySpendLimit (F):
            The default overall monthly spend limit (in currency terms)
            associated with the Billing Entity
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        str vatNumber (F):
            The VAT number / tax reference of the Billing Entity
    """

    ALL_ATTRIBS = {'standardEmailSettings', 'providers', 'parentName',
                   'billingEntityName', 'resourceState', 'currency',
                   'resourceName', 'adminControlPanelURL',
                   'no3ds28DaySpendLimit', 'resourceCreateDate', 'description',
                   'currencyId', 'parentUUID', 'permittedPOResourceTypes',
                   'sortOrder', 'resourceUUID', 'billingEntityUUID',
                   'invoiceSetting', 'enableUserEditing', 'billingType',
                   'resourceMetadata', 'controlPanelURL', 'descendants',
                   'brand', 'address', 'lastModifiedTime', 'emailTemplates',
                   'systemCapabilities', 'overall28DaySpendLimit',
                   'resourceType', 'resourceKey', 'vatNumber'}
    REQUIRED_ATTRIBS = {'currencyId', 'resourceName', 'resourceType',
                        'sortOrder'}
    OPTIONAL_ATTRIBS = {'parentUUID', 'providers', 'parentName',
                        'billingEntityName', 'resourceState', 'currency',
                        'adminControlPanelURL', 'no3ds28DaySpendLimit',
                        'resourceCreateDate', 'controlPanelURL',
                        'standardEmailSettings', 'permittedPOResourceTypes',
                        'resourceUUID', 'billingEntityUUID', 'invoiceSetting',
                        'enableUserEditing', 'billingType', 'resourceMetadata',
                        'description', 'descendants', 'brand', 'address',
                        'lastModifiedTime', 'emailTemplates',
                        'systemCapabilities', 'overall28DaySpendLimit',
                        'resourceKey', 'vatNumber'}
    TYPES = {'parentUUID': str, 'providers': Dict(str, Dict(str, str)),
             'parentName': str, 'billingEntityName': str, 'resourceState':
             enums.ResourceState, 'currency': Currency, 'resourceName': str,
             'adminControlPanelURL': str, 'no3ds28DaySpendLimit': float,
             'resourceCreateDate': datetime, 'controlPanelURL': str,
             'currencyId': int, 'standardEmailSettings':
             Dict(enums.BillingEntityVAR, str), 'permittedPOResourceTypes':
             List(enums.ResourceType), 'sortOrder': int, 'resourceUUID': str,
             'billingEntityUUID': str, 'invoiceSetting': InvoiceSetting,
             'enableUserEditing': bool, 'billingType': enums.BillingType,
             'resourceMetadata': ResourceMetadata, 'description': str,
             'descendants': List(str), 'brand': int, 'address': Address,
             'lastModifiedTime': int, 'emailTemplates':
             Dict(enums.EmailType, EmailTemplate), 'systemCapabilities':
             SystemCapabilitySet, 'overall28DaySpendLimit': float,
             'resourceType': enums.ResourceType, 'resourceKey':
             List(ResourceKey), 'vatNumber': str}


class Question(ComplexObject):

    """FCO REST API Question complex object.

    Name.

    Attributes (type name (required): description:
        Resource resource (T):
            The resource to which the question relates
        str keyName (T):
            The name of the key with which the question is associated
        str type (T):
            The type of the reply to the question
        str name (T):
            The question to be asked
    """

    ALL_ATTRIBS = {'type', 'keyName', 'resource', 'name'}
    REQUIRED_ATTRIBS = {'resource', 'keyName', 'type', 'name'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'resource': Resource, 'keyName': str, 'type': str, 'name': str}


class ValueValidator(ComplexObject):

    """FCO REST API ValueValidator complex object.

    Name.

    Attributes (type name (required): description:
        str errorMessage (F):
            A custom error message to display if the validation
            specified by the 'validatorType' and 'validateString' are
            not met
        str validateString (T):
            The validate string.
        bool allowsMultipleValues (T):
            State if the value string allows multiple, comma seperated,
            values to be specified
        SearchFilter searchFilter (F):
            A string that contains a condition used to filter results
            that match the validateString and validatorType
        enums.ValidatorType validatorType (T):
            The validator type.
    """

    ALL_ATTRIBS = {'validateString', 'errorMessage', 'allowsMultipleValues',
                   'searchFilter', 'validatorType'}
    REQUIRED_ATTRIBS = {'validateString', 'allowsMultipleValues',
                        'validatorType'}
    OPTIONAL_ATTRIBS = {'errorMessage', 'searchFilter'}
    TYPES = {'errorMessage': str, 'validateString': str,
             'allowsMultipleValues': bool, 'searchFilter': SearchFilter,
             'validatorType': enums.ValidatorType}


class ResolvableReference(ComplexObject):

    """FCO REST API ResolvableReference complex object.

    Name.

    Attributes (type name (required): description:
        List(GenericContainer) alternateReferences (T):
            List of alternate references to use
        enums.ResourceType missingType (T):
            The missing resourcetype
        str missingUUID (T):
            The missing resource uuid
        Resource referenceResource (T):
            The reference resource
    """

    ALL_ATTRIBS = {'missingType', 'alternateReferences', 'missingUUID',
                   'referenceResource'}
    REQUIRED_ATTRIBS = {'alternateReferences', 'missingType', 'missingUUID',
                        'referenceResource'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'alternateReferences': List(GenericContainer), 'missingType':
             enums.ResourceType, 'missingUUID': str, 'referenceResource':
             Resource}


class Query(ComplexObject):

    """FCO REST API Query complex object.

    Name.

    Attributes (type name (required): description:
        List(AggregationField) aggregationFields (F):
            A list of zero or more aggregation fields
        SearchFilter searchFilter (F):
            The search filter to use
        enums.ResourceType resourceType (T):
            The resource type or pseudo-resource type to query
        List(str) outputFields (F):
            An array of output field names in FQL dot notation
        List(str) groupByFields (F):
            An array of 'group by' field names in FQL dot notation
        QueryLimit limit (F):
            The query limit to use
        List(AggregationFilter) aggregationFilters (F):
            A list of 0 or more aggregation Filters
    """

    ALL_ATTRIBS = {'aggregationFields', 'searchFilter', 'resourceType',
                   'outputFields', 'groupByFields', 'limit',
                   'aggregationFilters'}
    REQUIRED_ATTRIBS = {'resourceType'}
    OPTIONAL_ATTRIBS = {'aggregationFields', 'searchFilter', 'outputFields',
                        'groupByFields', 'limit', 'aggregationFilters'}
    TYPES = {'aggregationFields': List(AggregationField), 'searchFilter':
             SearchFilter, 'resourceType': enums.ResourceType, 'outputFields':
             List(str), 'groupByFields': List(str), 'limit': QueryLimit,
             'aggregationFilters': List(AggregationFilter)}


class Network(ComplexObject):

    """FCO REST API Network complex object.

    Name.

    Attributes (type name (required): description:
        str customerName (F):
            The name of the customer that owns the resource
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        bool ipv6RoutingEnabled (F):
            A flag to indicate whether IPv6 should be routedby the
            routing element of the network (if any)
        str deploymentInstanceUUID (F):
            The uuid of the deployment instance the resource is created
            from
        str vdcUUID (T):
            The UUID of the VDC in which the resource is contained
        str productOfferUUID (F):
            The UUID of the product offer associated with the resource
        str resourceName (T):
            The name of the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
        str productOfferName (F):
            The name of the product offer associated with the resource
        str clusterUUID (T):
            The UUID of the cluster in which the resource is located
        str deploymentInstanceName (F):
            The name of the deployment instance the resource is created
            from
        str customerUUID (F):
            The UUID of the customer that owns the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        int sortOrder (T):
            The sort order value for the given resource
        List(Subnet) subnets (F):
            A list of the IP subnets associated with the network
        str clusterName (F):
            The name of the cluster in which the resource is located
        str vdcName (F):
            The name of the VDC in which the resource is contained
        enums.NetworkType networkType (T):
            The type of the network
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
    """

    ALL_ATTRIBS = {'customerName', 'providers', 'resourceMetadata',
                   'billingEntityName', 'resourceState', 'ipv6RoutingEnabled',
                   'deploymentInstanceUUID', 'vdcUUID', 'productOfferUUID',
                   'resourceName', 'resourceCreateDate', 'productOfferName',
                   'clusterUUID', 'deploymentInstanceName', 'customerUUID',
                   'resourceUUID', 'billingEntityUUID', 'sortOrder', 'subnets',
                   'clusterName', 'vdcName', 'networkType', 'lastModifiedTime',
                   'resourceType', 'resourceKey'}
    REQUIRED_ATTRIBS = {'clusterUUID', 'resourceType', 'vdcUUID', 'sortOrder',
                        'networkType', 'resourceName'}
    OPTIONAL_ATTRIBS = {'productOfferName', 'subnets', 'customerName',
                        'providers', 'clusterName', 'resourceKey',
                        'resourceMetadata', 'billingEntityName',
                        'resourceState', 'vdcName', 'ipv6RoutingEnabled',
                        'deploymentInstanceUUID', 'customerUUID',
                        'resourceUUID', 'productOfferUUID',
                        'deploymentInstanceName', 'lastModifiedTime',
                        'billingEntityUUID', 'resourceCreateDate'}
    TYPES = {'customerName': str, 'providers': Dict(str, Dict(str, str)),
             'resourceMetadata': ResourceMetadata, 'billingEntityName': str,
             'resourceState': enums.ResourceState, 'ipv6RoutingEnabled': bool,
             'deploymentInstanceUUID': str, 'vdcUUID': str, 'productOfferUUID':
             str, 'resourceName': str, 'resourceCreateDate': datetime,
             'productOfferName': str, 'clusterUUID': str,
             'deploymentInstanceName': str, 'customerUUID': str,
             'resourceUUID': str, 'billingEntityUUID': str, 'sortOrder': int,
             'subnets': List(Subnet), 'clusterName': str, 'vdcName': str,
             'networkType': enums.NetworkType, 'lastModifiedTime': int,
             'resourceType': enums.ResourceType, 'resourceKey':
             List(ResourceKey)}


class Nic(ComplexObject):

    """FCO REST API Nic complex object.

    Name.

    Attributes (type name (required): description:
        str macAddress (F):
            The MAC address of the NIC
        str customerName (F):
            The name of the customer that owns the resource
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str deploymentInstanceUUID (F):
            The uuid of the deployment instance the resource is created
            from
        List(IP) ipAddresses (F):
            The IP addresses associated with the NIC
        str vdcUUID (T):
            The UUID of the VDC in which the resource is contained
        str productOfferUUID (F):
            The UUID of the product offer associated with the resource
        str resourceName (T):
            The name of the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
        str productOfferName (F):
            The name of the product offer associated with the resource
        int index (F):
            The zero-based index of the NIC within the server to which
            the NIC is attached
        str clusterUUID (T):
            The UUID of the cluster in which the resource is located
        str serverName (F):
            The name of the server to which the NIC is attached
        str clusterName (F):
            The name of the cluster in which the resource is located
        str deploymentInstanceName (F):
            The name of the deployment instance the resource is created
            from
        str customerUUID (F):
            The UUID of the customer that owns the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        int sortOrder (T):
            The sort order value for the given resource
        str networkUUID (T):
            The UUID of the network to which the NIC is attached
        str vdcName (F):
            The name of the VDC in which the resource is contained
        enums.NetworkType networkType (T):
            The type of the network to which the Nic is attached
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str networkName (F):
            The name of the network to which the NIC is attached
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        str serverUUID (T):
            The UUID of the server to which the NIC is attached
    """

    ALL_ATTRIBS = {'macAddress', 'customerName', 'providers',
                   'resourceMetadata', 'billingEntityName', 'resourceState',
                   'deploymentInstanceUUID', 'ipAddresses', 'vdcUUID',
                   'productOfferUUID', 'resourceName', 'resourceCreateDate',
                   'productOfferName', 'index', 'clusterUUID', 'serverName',
                   'networkUUID', 'deploymentInstanceName', 'customerUUID',
                   'resourceUUID', 'billingEntityUUID', 'sortOrder',
                   'clusterName', 'vdcName', 'networkType', 'lastModifiedTime',
                   'networkName', 'resourceType', 'resourceKey', 'serverUUID'}
    REQUIRED_ATTRIBS = {'clusterUUID', 'networkUUID', 'vdcUUID',
                        'resourceType', 'serverUUID', 'sortOrder',
                        'networkType', 'resourceName'}
    OPTIONAL_ATTRIBS = {'macAddress', 'customerName', 'providers',
                        'resourceMetadata', 'billingEntityName',
                        'resourceState', 'deploymentInstanceUUID',
                        'ipAddresses', 'productOfferUUID',
                        'resourceCreateDate', 'productOfferName', 'index',
                        'serverName', 'deploymentInstanceName', 'customerUUID',
                        'resourceUUID', 'billingEntityUUID', 'clusterName',
                        'vdcName', 'lastModifiedTime', 'networkName',
                        'resourceKey'}
    TYPES = {'macAddress': str, 'customerName': str, 'providers':
             Dict(str, Dict(str, str)), 'resourceMetadata': ResourceMetadata,
             'billingEntityName': str, 'resourceState': enums.ResourceState,
             'deploymentInstanceUUID': str, 'ipAddresses': List(IP), 'vdcUUID':
             str, 'productOfferUUID': str, 'resourceName': str,
             'resourceCreateDate': datetime, 'productOfferName': str, 'index':
             int, 'clusterUUID': str, 'serverName': str, 'clusterName': str,
             'deploymentInstanceName': str, 'customerUUID': str,
             'resourceUUID': str, 'billingEntityUUID': str, 'sortOrder': int,
             'networkUUID': str, 'vdcName': str, 'networkType':
             enums.NetworkType, 'lastModifiedTime': int, 'networkName': str,
             'resourceType': enums.ResourceType, 'resourceKey':
             List(ResourceKey), 'serverUUID': str}


class DryRunResult(ComplexObject):

    """FCO REST API DryRunResult complex object.

    Name.

    Attributes (type name (required): description:
        List(ResolvableReference) resolvableReferences (F):
            The list of references
        List(Question) questions (F):
            The list of question
        bool success (F):
            success or failure
    """

    ALL_ATTRIBS = {'resolvableReferences', 'success', 'questions'}
    REQUIRED_ATTRIBS = set()
    OPTIONAL_ATTRIBS = {'resolvableReferences', 'questions', 'success'}
    TYPES = {'resolvableReferences': List(ResolvableReference), 'questions':
             List(Question), 'success': bool}


class Value(ComplexObject):

    """FCO REST API Value complex object.

    Name.

    Attributes (type name (required): description:
        enums.MeasureType measureType (F):
            The type of unit used with the value
        str dataContent (T):
            Additional data for the value, normally used for sending
            large amount of data. When the VadatorType is a RESOURCE,
            this indicate which field that you want to display to the
            user
        str description (F):
            A user-friendly description given to the value
        bool remembered (F):
            State if the value shoudl be remembered by the browser auto-
            complete fields
        str defaultText (F):
            Text that is to be displayed as a placeholder instead of the
            default value
        str defaultValue (F):
            The default value
        bool required (F):
            The value is required or not
        str value (T):
            Value that going to be measured or configured
        bool readOnly (F):
            The value is read only
        ValueValidator validator (F):
            A Validator object. Only values that match the validator can
            be set.
        str key (T):
            The name of the configured value
        bool recheckOnChange (T):
            State if the API should be queried for necessery values if
            this value is changed.
        bool hidden (F):
            The boolean used to hide
        str name (T):
            A user-friendly name given to the value
    """

    ALL_ATTRIBS = {'measureType', 'dataContent', 'description', 'remembered',
                   'defaultText', 'defaultValue', 'required', 'value',
                   'readOnly', 'validator', 'key', 'recheckOnChange', 'hidden',
                   'name'}
    REQUIRED_ATTRIBS = {'recheckOnChange', 'dataContent', 'key', 'value',
                        'name'}
    OPTIONAL_ATTRIBS = {'measureType', 'description', 'remembered',
                        'defaultText', 'defaultValue', 'required', 'readOnly',
                        'validator', 'hidden'}
    TYPES = {'measureType': enums.MeasureType, 'dataContent': str,
             'description': str, 'remembered': bool, 'defaultText': str,
             'defaultValue': str, 'required': bool, 'value': str, 'readOnly':
             bool, 'validator': ValueValidator, 'key': str, 'recheckOnChange':
             bool, 'hidden': bool, 'name': str}


class HypervisorConfig(ComplexObject):

    """FCO REST API HypervisorConfig complex object.

    Name.

    Attributes (type name (required): description:
        List(HypervisorSetting) setting (T):
            The default settings for the hypervisor
        Dict(str, ValueValidator) config (T):
            The configuration settings for the hypervisor
    """

    ALL_ATTRIBS = {'setting', 'config'}
    REQUIRED_ATTRIBS = {'setting', 'config'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'setting': List(HypervisorSetting), 'config':
             Dict(str, ValueValidator)}


class ReportMethod(ComplexObject):

    """FCO REST API ReportMethod complex object.

    Name.

    Attributes (type name (required): description:
        enums.InvocationLevel invocationLevel (T):
            The level of authentication required to access the report
            method
        List(Value) inputValues (T):
            A list of configured values which represent the required
            input for the report method
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        enums.ResourceType resourceType (T):
            The type of the resource
        str fdlReference (T):
            The unique reference of the report method entry point in the
            FDL Code Block
        str fdlDescription (T):
            The long form description of the FDL function.
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        List(enums.ReportChartType) supportedReportChartTypes (T):
            A set of report chart types whcih are supported by the
            report method.
        str fdlUUID (T):
            The UUID of the FDL Code Block that contains the report
            method.
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str resourceName (T):
            The name of the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str fdlName (T):
            The name of the FDL Code Block that contains the function
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
        int sortOrder (T):
            The sort order value for the given resource
    """

    ALL_ATTRIBS = {'invocationLevel', 'inputValues', 'providers',
                   'resourceType', 'fdlReference', 'fdlDescription',
                   'resourceMetadata', 'billingEntityName',
                   'supportedReportChartTypes', 'fdlUUID', 'fdlName',
                   'resourceState', 'resourceUUID', 'resourceName',
                   'lastModifiedTime', 'billingEntityUUID', 'resourceKey',
                   'resourceCreateDate', 'sortOrder'}
    REQUIRED_ATTRIBS = {'invocationLevel', 'inputValues', 'resourceType',
                        'fdlReference', 'fdlDescription',
                        'supportedReportChartTypes', 'fdlUUID', 'sortOrder',
                        'resourceName', 'fdlName'}
    OPTIONAL_ATTRIBS = {'providers', 'resourceKey', 'resourceMetadata',
                        'billingEntityName', 'resourceState', 'resourceUUID',
                        'lastModifiedTime', 'billingEntityUUID',
                        'resourceCreateDate'}
    TYPES = {'sortOrder': int, 'invocationLevel': enums.InvocationLevel,
             'inputValues': List(Value), 'providers':
             Dict(str, Dict(str, str)), 'resourceType': enums.ResourceType,
             'fdlReference': str, 'fdlDescription': str, 'resourceMetadata':
             ResourceMetadata, 'billingEntityName': str,
             'supportedReportChartTypes': List(enums.ReportChartType),
             'fdlUUID': str, 'resourceState': enums.ResourceState,
             'resourceName': str, 'resourceUUID': str, 'lastModifiedTime': int,
             'fdlName': str, 'resourceKey': List(ResourceKey),
             'resourceCreateDate': datetime, 'billingEntityUUID': str}


class ActionDefinition(ComplexObject):

    """FCO REST API ActionDefinition complex object.

    Name.

    Attributes (type name (required): description:
        bool available (T):
            State if the action can be invoked.  This will always be
            true unless the ActionDefinition is returned through
            describeResource.
        str description (T):
            The description of the defined action
        List(Value) parameters (T):
            The parameters of the defined action
        List(enums.InvocationLevel) invocationLevels (T):
            The API autentication levels allowed to invoke the action
        enums.InvocationType invocationType (T):
            The invocation type of the action
        str executionFunction (T):
            The FDL function reference of the defined action
        str fdlUUID (T):
            The UUID of the FDL Code Block that contains the function
        str key (T):
            The key of the defined action
        enums.FDLReturnType returnType (T):
            The return type of the defined action
        str icon (T):
            The font icon to be displayed for generated buttons.
        int order (T):
            The order the action should be displayed compared to other
            actions, used in the Skyline UI
        str name (T):
            The name of the defined action
    """

    ALL_ATTRIBS = {'available', 'description', 'parameters',
                   'invocationLevels', 'name', 'invocationType',
                   'executionFunction', 'fdlUUID', 'key', 'returnType',
                   'order', 'icon'}
    REQUIRED_ATTRIBS = {'available', 'name', 'parameters', 'invocationLevels',
                        'invocationType', 'executionFunction', 'fdlUUID',
                        'key', 'returnType', 'icon', 'order', 'description'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'available': bool, 'name': str, 'parameters': List(Value),
             'invocationLevels': List(enums.InvocationLevel), 'invocationType':
             enums.InvocationType, 'executionFunction': str, 'fdlUUID': str,
             'key': str, 'returnType': enums.FDLReturnType, 'icon': str,
             'order': int, 'description': str}


class ProductComponent(ComplexObject):

    """FCO REST API ProductComponent complex object.

    Name.

    Attributes (type name (required): description:
        List(Value) productConfiguredValues (T):
            The list of configurable values inherited from the Product
            Component Type
        int lastBillingTime (T):
            The Last billing time of this compomenet when linked with a
            purchase, this is a readonly value
        List(Value) billingConfiguredValues (T):
            The list of configurable values inherited from the Billing
            Method
        str componentTypeUUID (T):
            The UUID of the product component type linked with the
            ProductComponent
        str billingMethodUUID (T):
            The billing method which is selected for this component
    """

    ALL_ATTRIBS = {'productConfiguredValues', 'lastBillingTime',
                   'billingConfiguredValues', 'componentTypeUUID',
                   'billingMethodUUID'}
    REQUIRED_ATTRIBS = {'productConfiguredValues', 'lastBillingTime',
                        'billingConfiguredValues', 'componentTypeUUID',
                        'billingMethodUUID'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'productConfiguredValues': List(Value), 'lastBillingTime': int,
             'billingConfiguredValues': List(Value), 'componentTypeUUID': str,
             'billingMethodUUID': str}


class Server(ComplexObject):

    """FCO REST API Server complex object.

    Name.

    Attributes (type name (required): description:
        bool disableEmulatedDevices (F):
            Instruct the hypervisor running the server to disable
            emulated devices or not. This will only work if the cluster
            has the DISABLE_EMULATED_DEVICE feature set. If the emulated
            devices are set to be disabled (default setting) the the
            server will be only presenetd with the para-virtualized
            devices. Any change to this value will need a server stop
            start
        str customerName (F):
            The name of the customer that owns the resource
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        str snapshotUUID (F):
            The UUID of the snapshot from which the server was cloned
        int ram (F):
            The amount of memory assigned to the server
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str deploymentInstanceUUID (F):
            The uuid of the deployment instance the resource is created
            from
        str resourceName (T):
            The name of the resource
        str productOfferUUID (F):
            The UUID of the product offer associated with the resource
        str nodeIP (F):
            The IP of the associated node for a running server
        datetime resourceCreateDate (F):
            The creation date of the resource
        str productOfferName (F):
            The name of the product offer associated with the resource
        str clusterUUID (T):
            The UUID of the cluster in which the resource is located
        str nodeName (F):
            The Name of the associated node for a running server
        str initialPassword (F):
            The initial user name associated with the server (passed by
            metadata so a first boot process can initialise the
            operating system image)
        List(Nic) nics (F):
            A list of the virtual NICs attached to the server
        ImagePermission imagePermission (F):
            This will contain the permission of the current image which
            is been used by the server, Note that you will not be able
            to use this field in FQL
        str imageName (F):
            The name of the image from which the server was built
        str customerUUID (F):
            The UUID of the customer that owns the resource
        str imageUUID (F):
            The UUID of the image from which the server was built
        str resourceUUID (F):
            The UUID of the resource (read-only)
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        int sortOrder (T):
            The sort order value for the given resource
        enums.ServerStatus status (F):
            The status of the server (e.g. whether it is running or
            stopped)
        enums.VirtualizationType virtualizationType (T):
            The virtualization type of the server
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str clusterName (F):
            The name of the cluster in which the resource is located
        int vmId (T):
            The ID of the running server on the associated node
        str vdcName (F):
            The name of the VDC in which the resource is contained
        List(enums.ServerCapability) serverCapabilities (T):
            The list of allowed server capabilities
        str initialUser (F):
            The initial user name associated with the server (passed by
            metadata so a first boot process can initialise the
            operating system image)
        str vdcUUID (T):
            The UUID of the VDC in which the resource is contained
        str deploymentInstanceName (F):
            The name of the deployment instance the resource is created
            from
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        List(SSHKey) sshkeys (F):
            A list of the sshkeys attached to the server
        List(HypervisorSetting) defaultSettings (F):
            The combined default and cluster hypervisor settings
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        List(Disk) disks (T):
            A list of the disks attached to the server
        List(HypervisorSetting) hypervisorSettings (F):
            The hypervisor settings for this cluster
        str serverKey (F):
            The server key of the server (for image/server cryptographic
            validation)
        str nodeUUID (F):
            The UUID of the associated node for a running server
        int cpu (F):
            The number of virtual CPU cores assigned to the server
    """

    ALL_ATTRIBS = {'status', 'customerName', 'providers', 'snapshotUUID',
                   'ram', 'billingEntityName', 'resourceState',
                   'deploymentInstanceUUID', 'resourceName',
                   'productOfferUUID', 'nodeIP', 'resourceCreateDate',
                   'productOfferName', 'clusterUUID', 'nodeName',
                   'initialPassword', 'nics', 'imagePermission', 'imageName',
                   'customerUUID', 'imageUUID', 'resourceUUID',
                   'billingEntityUUID', 'sortOrder', 'disableEmulatedDevices',
                   'virtualizationType', 'resourceMetadata', 'clusterName',
                   'vmId', 'vdcName', 'serverCapabilities', 'initialUser',
                   'vdcUUID', 'deploymentInstanceName', 'lastModifiedTime',
                   'sshkeys', 'defaultSettings', 'resourceType', 'resourceKey',
                   'disks', 'hypervisorSettings', 'serverKey', 'nodeUUID',
                   'cpu'}
    REQUIRED_ATTRIBS = {'serverCapabilities', 'clusterUUID',
                        'virtualizationType', 'resourceType', 'disks', 'vmId',
                        'sortOrder', 'vdcUUID', 'resourceName'}
    OPTIONAL_ATTRIBS = {'disableEmulatedDevices', 'customerName', 'providers',
                        'snapshotUUID', 'ram', 'billingEntityName',
                        'resourceState', 'deploymentInstanceUUID',
                        'productOfferUUID', 'nodeIP', 'resourceCreateDate',
                        'productOfferName', 'nodeName', 'initialPassword',
                        'nics', 'imagePermission', 'imageName', 'customerUUID',
                        'imageUUID', 'resourceUUID', 'billingEntityUUID',
                        'status', 'resourceMetadata', 'clusterName', 'vdcName',
                        'initialUser', 'deploymentInstanceName',
                        'lastModifiedTime', 'sshkeys', 'defaultSettings',
                        'resourceKey', 'hypervisorSettings', 'serverKey',
                        'nodeUUID', 'cpu'}
    TYPES = {'disableEmulatedDevices': bool, 'customerName': str, 'providers':
             Dict(str, Dict(str, str)), 'snapshotUUID': str, 'ram': int,
             'billingEntityName': str, 'resourceState': enums.ResourceState,
             'deploymentInstanceUUID': str, 'resourceName': str,
             'productOfferUUID': str, 'nodeIP': str, 'resourceCreateDate':
             datetime, 'productOfferName': str, 'clusterUUID': str, 'nodeName':
             str, 'initialPassword': str, 'nics': List(Nic), 'imagePermission':
             ImagePermission, 'imageName': str, 'customerUUID': str,
             'imageUUID': str, 'resourceUUID': str, 'billingEntityUUID': str,
             'sortOrder': int, 'status': enums.ServerStatus,
             'virtualizationType': enums.VirtualizationType,
             'resourceMetadata': ResourceMetadata, 'clusterName': str, 'vmId':
             int, 'vdcName': str, 'serverCapabilities':
             List(enums.ServerCapability), 'initialUser': str, 'vdcUUID': str,
             'deploymentInstanceName': str, 'lastModifiedTime': int, 'sshkeys':
             List(SSHKey), 'defaultSettings': List(HypervisorSetting),
             'resourceType': enums.ResourceType, 'resourceKey':
             List(ResourceKey), 'disks': List(Disk), 'hypervisorSettings':
             List(HypervisorSetting), 'serverKey': str, 'nodeUUID': str, 'cpu':
             int}


class ResourceTypeDefinition(ComplexObject):

    """FCO REST API ResourceTypeDefinition complex object.

    Name.

    Attributes (type name (required): description:
        List(Value) measuredValues (T):
            List of available measured values for that resource type
        enums.ResourceType resourceType (T):
            The resource type
        str description (T):
            A user friendly description of the resource type
        bool billable (T):
            Indicates whether the resource type is billable
    """

    ALL_ATTRIBS = {'measuredValues', 'resourceType', 'description', 'billable'}
    REQUIRED_ATTRIBS = {'measuredValues', 'resourceType', 'description',
                        'billable'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'measuredValues': List(Value), 'resourceType': enums.ResourceType,
             'description': str, 'billable': bool}


class PaymentMethodInstance(ComplexObject):

    """FCO REST API PaymentMethodInstance complex object.

    Name.

    Attributes (type name (required): description:
        str paymentMethodUUID (T):
            The UUID of the associated payment method
        List(Value) configuredValues (T):
            A list of the configured values for the payment method
            instance
        str customerName (F):
            The name of the customer that owns the resource
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        bool nonInteractivePay (F):
            State if the payment method instance can support non-
            interactive payments
        str customerUUID (F):
            The UUID of the customer that owns the resource
        str resourceName (T):
            The name of the resource
        str paymentMethodName (F):
            The name of the associated payment method
        str resourceUUID (F):
            The UUID of the resource (read-only)
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        int sortOrder (T):
            The sort order value for the given resource
        datetime resourceCreateDate (F):
            The creation date of the resource
        bool isDefault (F):
            State if this is the default payment method instance for the
            associated customer
    """

    ALL_ATTRIBS = {'paymentMethodUUID', 'configuredValues', 'customerName',
                   'providers', 'resourceType', 'isDefault', 'resourceKey',
                   'resourceMetadata', 'billingEntityName', 'resourceState',
                   'resourceUUID', 'nonInteractivePay', 'customerUUID',
                   'paymentMethodName', 'resourceName', 'lastModifiedTime',
                   'billingEntityUUID', 'resourceCreateDate', 'sortOrder'}
    REQUIRED_ATTRIBS = {'resourceType', 'paymentMethodUUID',
                        'configuredValues', 'sortOrder', 'resourceName'}
    OPTIONAL_ATTRIBS = {'customerName', 'providers', 'resourceKey',
                        'resourceMetadata', 'billingEntityName',
                        'resourceState', 'nonInteractivePay', 'customerUUID',
                        'resourceCreateDate', 'paymentMethodName',
                        'resourceUUID', 'lastModifiedTime',
                        'billingEntityUUID', 'isDefault'}
    TYPES = {'paymentMethodUUID': str, 'configuredValues': List(Value),
             'customerName': str, 'providers': Dict(str, Dict(str, str)),
             'resourceType': enums.ResourceType, 'resourceKey':
             List(ResourceKey), 'resourceMetadata': ResourceMetadata,
             'billingEntityName': str, 'resourceState': enums.ResourceState,
             'nonInteractivePay': bool, 'resourceName': str, 'customerUUID':
             str, 'resourceCreateDate': datetime, 'paymentMethodName': str,
             'resourceUUID': str, 'lastModifiedTime': int, 'billingEntityUUID':
             str, 'isDefault': bool, 'sortOrder': int}


class PaymentProvider(ComplexObject):

    """FCO REST API PaymentProvider complex object.

    Name.

    Attributes (type name (required): description:
        List(Value) pmConfigurableList (T):
            List of Configurable Values for the payment provider
            relating to the payment method. This field cannot be
            selected using FQL
        str fdlPaymentRef (T):
            The reference for the payment provider from the FDL code
            block.
        str description (T):
            Longform description of the payment method, populated from
            the FDL code block.
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        enums.ResourceType resourceType (T):
            The type of the resource
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        List(Value) pmiConfigurableList (T):
            List of Configurable Values for the payment provider
            relating to the payment method instance. This field cannot
            be selected using FQL
        str fdlUUID (T):
            UUID of the FDL code block to which the Payment Method is
            linked.
        enums.ResourceState resourceState (F):
            The state of the resource
        str resourceName (T):
            The name of the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str fdlName (T):
            The name of the associated FDL code block
        datetime resourceCreateDate (F):
            The creation date of the resource
        int sortOrder (T):
            The sort order value for the given resource
    """

    ALL_ATTRIBS = {'pmConfigurableList', 'fdlPaymentRef', 'description',
                   'providers', 'resourceType', 'fdlName', 'resourceKey',
                   'resourceMetadata', 'billingEntityName',
                   'pmiConfigurableList', 'fdlUUID', 'resourceState',
                   'resourceUUID', 'resourceName', 'lastModifiedTime',
                   'billingEntityUUID', 'resourceCreateDate', 'sortOrder'}
    REQUIRED_ATTRIBS = {'pmConfigurableList', 'fdlPaymentRef', 'description',
                        'resourceType', 'pmiConfigurableList', 'fdlUUID',
                        'sortOrder', 'resourceName', 'fdlName'}
    OPTIONAL_ATTRIBS = {'providers', 'resourceKey', 'resourceMetadata',
                        'billingEntityName', 'resourceState', 'resourceUUID',
                        'lastModifiedTime', 'billingEntityUUID',
                        'resourceCreateDate'}
    TYPES = {'pmConfigurableList': List(Value), 'fdlPaymentRef': str,
             'description': str, 'providers': Dict(str, Dict(str, str)),
             'resourceType': enums.ResourceType, 'billingEntityUUID': str,
             'resourceKey': List(ResourceKey), 'resourceMetadata':
             ResourceMetadata, 'billingEntityName': str, 'pmiConfigurableList':
             List(Value), 'fdlUUID': str, 'resourceState': enums.ResourceState,
             'resourceName': str, 'resourceUUID': str, 'lastModifiedTime': int,
             'fdlName': str, 'resourceCreateDate': datetime, 'sortOrder': int}


class MeasurementFunction(ComplexObject):

    """FCO REST API MeasurementFunction complex object.

    Name.

    Attributes (type name (required): description:
        enums.ResourceType associatedType (T):
            The measured type
        str fdlUUID (T):
            The UUID of the FDL Code Block that contains the function.
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        enums.ResourceType resourceType (T):
            The type of the resource
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        str fdlDescription (T):
            The long form description of the FDL function.
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str extendedType (T):
            The pluggable provider type associated with Pluggable
            Resource measurement function
        int waitTime (T):
            The wait time
        int sortOrder (T):
            The sort order value for the given resource
        str resourceName (T):
            The name of the resource
        Dict(str, Value) measuredValues (T):
            A map of measured values
        str resourceUUID (F):
            The UUID of the resource (read-only)
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str fdlName (T):
            The name of the FDL Code Block that contains the function
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
    """

    ALL_ATTRIBS = {'associatedType', 'waitTime', 'providers', 'resourceType',
                   'fdlName', 'fdlDescription', 'resourceMetadata',
                   'billingEntityName', 'resourceState', 'extendedType',
                   'fdlUUID', 'sortOrder', 'resourceUUID', 'measuredValues',
                   'resourceName', 'lastModifiedTime', 'billingEntityUUID',
                   'resourceKey', 'resourceCreateDate'}
    REQUIRED_ATTRIBS = {'associatedType', 'fdlUUID', 'resourceType',
                        'fdlDescription', 'extendedType', 'waitTime',
                        'sortOrder', 'measuredValues', 'resourceName',
                        'fdlName'}
    OPTIONAL_ATTRIBS = {'providers', 'resourceKey', 'resourceMetadata',
                        'billingEntityName', 'resourceState', 'resourceUUID',
                        'lastModifiedTime', 'billingEntityUUID',
                        'resourceCreateDate'}
    TYPES = {'associatedType': enums.ResourceType, 'fdlUUID': str, 'providers':
             Dict(str, Dict(str, str)), 'resourceType': enums.ResourceType,
             'billingEntityUUID': str, 'fdlDescription': str,
             'resourceMetadata': ResourceMetadata, 'billingEntityName': str,
             'resourceState': enums.ResourceState, 'extendedType': str,
             'waitTime': int, 'sortOrder': int, 'resourceName': str,
             'measuredValues': Dict(str, Value), 'resourceUUID': str,
             'lastModifiedTime': int, 'fdlName': str, 'resourceKey':
             List(ResourceKey), 'resourceCreateDate': datetime}


class MeasuredValue(ComplexObject):

    """FCO REST API MeasuredValue complex object.

    Name.

    Attributes (type name (required): description:
        str measuredResourceName (F):
            The name of the resource from which the measurement was
            taken
        enums.ResourceType resourceType (T):
            The type of the resource
        int timestamp (T):
            The measurement timestamp (as a Unix time stamp, seconds
            from 1 Jan 1970)
        str measureKey (T):
            The unique name identifying the measurement taken and acting
            as a key
        str customerUUID (T):
            The UUID of the customer owning the resource
        float measurement (T):
            The numeric representation of the measurement value, if
            appropropriate
        str resourceUUID (T):
            The UUID of the resource from which the measurement was
            taken
        enums.MeasureType measurementType (T):
            The type of the measured value
        str billingEntityUUID (T):
            The UUID of the billing entity owning the customer
        Value measurementAsValue (T):
            The measured value
        enums.ResourceType measuredResourceType (F):
            The type of the resource from which the measurement was
            taken
    """

    ALL_ATTRIBS = {'measuredResourceName', 'resourceType', 'timestamp',
                   'measureKey', 'customerUUID', 'measurement', 'resourceUUID',
                   'measurementType', 'billingEntityUUID',
                   'measurementAsValue', 'measuredResourceType'}
    REQUIRED_ATTRIBS = {'resourceType', 'timestamp', 'measureKey',
                        'customerUUID', 'measurement', 'resourceUUID',
                        'measurementType', 'billingEntityUUID',
                        'measurementAsValue'}
    OPTIONAL_ATTRIBS = {'measuredResourceType', 'measuredResourceName'}
    TYPES = {'measuredResourceName': str, 'resourceType': enums.ResourceType,
             'timestamp': int, 'measureKey': str, 'customerUUID': str,
             'measurement': float, 'resourceUUID': str, 'measurementType':
             enums.MeasureType, 'billingEntityUUID': str, 'measurementAsValue':
             Value, 'measuredResourceType': enums.ResourceType}


class BillingMethod(ComplexObject):

    """FCO REST API BillingMethod complex object.

    Name.

    Attributes (type name (required): description:
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        str description (F):
            Longform description of the billing method, populated from
            the FDL code block.
        List(Value) configurableList (T):
            List of Configurable Values for this Billing Method. This
            field cannot be selected using FQL
        enums.ResourceType resourceType (T):
            The type of the resource
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str fdlUUID (T):
            UUID of the FDL code block to which the Billing Method is
            linked.
        int sortOrder (T):
            The sort order value for the given resource
        str resourceName (T):
            The name of the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str fdlName (T):
            The name of the FDL Code Block that contains the function
        datetime resourceCreateDate (F):
            The creation date of the resource
    """

    ALL_ATTRIBS = {'resourceMetadata', 'description', 'configurableList',
                   'resourceType', 'fdlName', 'resourceKey', 'providers',
                   'billingEntityName', 'resourceState', 'fdlUUID',
                   'sortOrder', 'resourceUUID', 'resourceName',
                   'lastModifiedTime', 'billingEntityUUID',
                   'resourceCreateDate'}
    REQUIRED_ATTRIBS = {'configurableList', 'resourceType', 'fdlUUID',
                        'sortOrder', 'resourceName', 'fdlName'}
    OPTIONAL_ATTRIBS = {'description', 'providers', 'resourceKey',
                        'resourceMetadata', 'billingEntityName',
                        'resourceState', 'resourceUUID', 'lastModifiedTime',
                        'billingEntityUUID', 'resourceCreateDate'}
    TYPES = {'providers': Dict(str, Dict(str, str)), 'description': str,
             'configurableList': List(Value), 'resourceType':
             enums.ResourceType, 'billingEntityUUID': str, 'resourceKey':
             List(ResourceKey), 'resourceMetadata': ResourceMetadata,
             'billingEntityName': str, 'resourceState': enums.ResourceState,
             'fdlUUID': str, 'sortOrder': int, 'resourceName': str,
             'resourceUUID': str, 'lastModifiedTime': int, 'fdlName': str,
             'resourceCreateDate': datetime}


class PaymentMethod(ComplexObject):

    """FCO REST API PaymentMethod complex object.

    Name.

    Attributes (type name (required): description:
        str fdlPaymentRef (F):
            The reference for the payment provider from the FDL code
            block
        str paymentProviderName (F):
            The name of the associated payment provider
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        enums.ResourceType resourceType (T):
            The type of the resource
        bool configured (F):
            State if the payment method has been successfully configured
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        List(Value) configuredValues (F):
            The list of configurable values which need to configured
            (These values are required by the specific payment provider)
        enums.ResourceState resourceState (F):
            The state of the resource
        bool consolidateInvoices (F):
            State if the collection loop will consolidate invoices if
            this is the selected payment method
        List(Value) instanceValues (F):
            The list configurable values which need to configured when
            you are creating PaymentMethodInstace from this
            PaymentMethod
        str resourceName (T):
            The name of the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str paymentProviderUUID (T):
            The UUID of the associated payment provider
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
        int sortOrder (T):
            The sort order value for the given resource
    """

    ALL_ATTRIBS = {'fdlPaymentRef', 'paymentProviderName', 'providers',
                   'resourceType', 'configured', 'resourceMetadata',
                   'billingEntityName', 'configuredValues', 'resourceState',
                   'consolidateInvoices', 'instanceValues', 'resourceUUID',
                   'resourceName', 'lastModifiedTime', 'paymentProviderUUID',
                   'billingEntityUUID', 'resourceKey', 'resourceCreateDate',
                   'sortOrder'}
    REQUIRED_ATTRIBS = {'resourceType', 'resourceName', 'paymentProviderUUID',
                        'sortOrder'}
    OPTIONAL_ATTRIBS = {'fdlPaymentRef', 'paymentProviderName', 'providers',
                        'configured', 'resourceMetadata', 'billingEntityName',
                        'configuredValues', 'resourceState',
                        'consolidateInvoices', 'instanceValues',
                        'resourceUUID', 'lastModifiedTime',
                        'billingEntityUUID', 'resourceKey',
                        'resourceCreateDate'}
    TYPES = {'fdlPaymentRef': str, 'paymentProviderName': str, 'providers':
             Dict(str, Dict(str, str)), 'resourceType': enums.ResourceType,
             'configured': bool, 'resourceMetadata': ResourceMetadata,
             'billingEntityName': str, 'configuredValues': List(Value),
             'resourceState': enums.ResourceState, 'consolidateInvoices': bool,
             'instanceValues': List(Value), 'resourceName': str,
             'resourceUUID': str, 'lastModifiedTime': int,
             'paymentProviderUUID': str, 'billingEntityUUID': str,
             'resourceKey': List(ResourceKey), 'resourceCreateDate': datetime,
             'sortOrder': int}


class Cluster(ComplexObject):

    """FCO REST API Cluster complex object.

    Name.

    Attributes (type name (required): description:
        bool diskDetachSupport (F):
            Indicate if a disk can be detached from a server
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        str vlanRestrictedInnerTags (T):
            The tags which are restricted - a comma seperated list
        bool vmSupport (F):
            Indicate if the cluster supports virtual machines
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        bool fetchDiskSupport (F):
            Indicate if the cluster supports fetching disks
        str macAddressPrefix (T):
            The mac address prefix for the cluster
        int clusterPort (T):
            The port for the service
        str resourceName (T):
            The name of the resource
        HypervisorConfig hypervisorConfig (T):
            The hypervisor specific configuration definitions for this
            cluster
        datetime resourceCreateDate (F):
            The creation date of the resource
        bool vlanQinQmode (T):
            Indicates if QinQ mode is active
        int sortOrder (T):
            The sort order value for the given resource
        str clusterIP (T):
            The endpoint of the XVP service
        str resourceUUID (F):
            The UUID of the resource (read-only)
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        str username (T):
            The usename for the XVP service
        bool ucsIntegration (T):
            The type of integration used by the cluster - 0 - none, 1 -
            UCS
        bool isoDetachSupport (F):
            Indicate if an ISO disk can be detached from a server
        int vlanStartOuterTag (T):
            When VLAN allocation is runing in the QinQ mode this will be
            used as the start tag
        bool createDefaultVDC (T):
            To create a default VDC on creation of a customer
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str password (T):
            The password for the XVP service
        List(HypervisorSetting) defaultSettings (T):
            The combined default and cluster hypervisor settings
        str vlanRestrictedOuterTags (T):
            The tags which are restricted in QinQ mode - a comma
            seperated list
        SystemCapabilitySet systemCapabilities (T):
            The capabilities of the cluster
        enums.ResourceType resourceType (T):
            The type of the resource
        int vlanStartInnerTag (T):
            The minimum VLAN tag to be allocated
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        List(HypervisorSetting) hypervisorSettings (T):
            The hypervisor settings for this cluster
        int vlanEndInnerTag (T):
            The maximum VLAN tag to be allocated
        int vlanEndOuterTag (T):
            In the QinQ mode maximum outer tag which can be allocated
        enums.HypervisorType hypervisor (T):
            The hypervisor of the cluster
        bool fetchServerSupport (F):
            Indicate if the cluster supports fetching servers
        bool fetchISOSupport (F):
            Indicate if the cluster supports fetching ISO
        bool ctSupport (F):
            Indicate if the cluster supports containers
    """

    ALL_ATTRIBS = {'diskDetachSupport', 'providers', 'vlanRestrictedInnerTags',
                   'vmSupport', 'resourceMetadata', 'billingEntityName',
                   'resourceState', 'createDefaultVDC', 'clusterPort',
                   'resourceName', 'hypervisorConfig', 'hypervisor',
                   'resourceCreateDate', 'vlanQinQmode', 'sortOrder',
                   'clusterIP', 'resourceUUID', 'billingEntityUUID',
                   'username', 'vlanRestrictedOuterTags', 'isoDetachSupport',
                   'vlanStartOuterTag', 'fetchDiskSupport', 'lastModifiedTime',
                   'password', 'defaultSettings', 'ucsIntegration',
                   'systemCapabilities', 'resourceType', 'vlanStartInnerTag',
                   'resourceKey', 'hypervisorSettings', 'vlanEndInnerTag',
                   'vlanEndOuterTag', 'macAddressPrefix', 'fetchServerSupport',
                   'ctSupport', 'fetchISOSupport'}
    REQUIRED_ATTRIBS = {'vlanRestrictedInnerTags', 'clusterPort',
                        'hypervisorConfig', 'resourceName', 'vlanQinQmode',
                        'sortOrder', 'clusterIP', 'vlanStartInnerTag',
                        'username', 'ucsIntegration', 'vlanStartOuterTag',
                        'createDefaultVDC', 'password', 'defaultSettings',
                        'vlanRestrictedOuterTags', 'systemCapabilities',
                        'resourceType', 'hypervisor', 'hypervisorSettings',
                        'vlanEndInnerTag', 'vlanEndOuterTag',
                        'macAddressPrefix'}
    OPTIONAL_ATTRIBS = {'diskDetachSupport', 'isoDetachSupport', 'providers',
                        'vmSupport', 'resourceKey', 'resourceMetadata',
                        'billingEntityName', 'resourceState',
                        'fetchServerSupport', 'fetchDiskSupport',
                        'resourceUUID', 'lastModifiedTime', 'fetchISOSupport',
                        'billingEntityUUID', 'resourceCreateDate', 'ctSupport'}
    TYPES = {'diskDetachSupport': bool, 'providers':
             Dict(str, Dict(str, str)), 'vlanRestrictedInnerTags': str,
             'vmSupport': bool, 'resourceMetadata': ResourceMetadata,
             'billingEntityName': str, 'resourceState': enums.ResourceState,
             'fetchDiskSupport': bool, 'clusterPort': int, 'resourceName': str,
             'hypervisorConfig': HypervisorConfig, 'resourceCreateDate':
             datetime, 'vlanQinQmode': bool, 'sortOrder': int, 'clusterIP':
             str, 'resourceUUID': str, 'billingEntityUUID': str, 'username':
             str, 'ucsIntegration': bool, 'isoDetachSupport': bool,
             'vlanStartOuterTag': int, 'createDefaultVDC': bool,
             'lastModifiedTime': int, 'password': str, 'defaultSettings':
             List(HypervisorSetting), 'vlanRestrictedOuterTags': str,
             'systemCapabilities': SystemCapabilitySet, 'resourceType':
             enums.ResourceType, 'hypervisor': enums.HypervisorType,
             'resourceKey': List(ResourceKey), 'hypervisorSettings':
             List(HypervisorSetting), 'fetchISOSupport': bool,
             'vlanEndInnerTag': int, 'vlanEndOuterTag': int,
             'macAddressPrefix': str, 'fetchServerSupport': bool, 'ctSupport':
             bool, 'vlanStartInnerTag': int}


class ProductComponentType(ComplexObject):

    """FCO REST API ProductComponentType complex object.

    Name.

    Attributes (type name (required): description:
        Dict(str, ActionDefinition) actionFunctions (F):
            Action definitions for use of resources configured by this
            product component type
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        bool isOptional (F):
            State if the PCT is optional, and if a Product Offer must
            complete it's required fields.
        List(Value) configurableList (T):
            A list of Configurable Values for the PCT
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        List(Value) measuredList (T):
            A list of Measured Values for the PCT
        int sortOrder (T):
            The sort order value for the given resource
        str resourceName (T):
            The name of the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str referenceField (T):
            The user friendly unique refernce given to the PCT
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        datetime resourceCreateDate (F):
            The creation date of the resource
    """

    ALL_ATTRIBS = {'actionFunctions', 'resourceMetadata', 'isOptional',
                   'configurableList', 'resourceType', 'resourceKey',
                   'providers', 'billingEntityName', 'resourceState',
                   'measuredList', 'sortOrder', 'resourceUUID', 'resourceName',
                   'lastModifiedTime', 'referenceField', 'billingEntityUUID',
                   'resourceCreateDate'}
    REQUIRED_ATTRIBS = {'configurableList', 'resourceType', 'measuredList',
                        'sortOrder', 'resourceName', 'referenceField'}
    OPTIONAL_ATTRIBS = {'actionFunctions', 'isOptional', 'providers',
                        'resourceKey', 'resourceMetadata', 'billingEntityName',
                        'resourceState', 'resourceUUID', 'lastModifiedTime',
                        'billingEntityUUID', 'resourceCreateDate'}
    TYPES = {'actionFunctions': Dict(str, ActionDefinition), 'providers':
             Dict(str, Dict(str, str)), 'isOptional': bool,
             'configurableList': List(Value), 'resourceType':
             enums.ResourceType, 'resourceKey': List(ResourceKey),
             'resourceMetadata': ResourceMetadata, 'billingEntityName': str,
             'resourceState': enums.ResourceState, 'measuredList': List(Value),
             'sortOrder': int, 'resourceName': str, 'resourceUUID': str,
             'lastModifiedTime': int, 'referenceField': str,
             'billingEntityUUID': str, 'resourceCreateDate': datetime}


class PluggableResource(ComplexObject):

    """FCO REST API PluggableResource complex object.

    Name.

    Attributes (type name (required): description:
        str customerName (F):
            The name of the customer that owns the resource
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        Dict(str, str) resourceValues (T):
            The value map linked to the provider PCT configured values
        str providerIcon (F):
            The icon of the Pluggable Resource Provider that defined the
            Pluggable Resource
        str productOfferUUID (F):
            The UUID of the product offer associated with the resource
        str resourceName (T):
            The name of the resource
        datetime resourceCreateDate (F):
            The creation date of the resource
        str productOfferName (F):
            The name of the product offer associated with the resource
        Dict(str, ActionDefinition) providerActionDefinitions (F):
            The actions that are available to this resource
        str providerGroup (F):
            The group of the Pluggable Resource Provider that defined
            the Pluggable Resource
        str customerUUID (F):
            The UUID of the customer that owns the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        int sortOrder (T):
            The sort order value for the given resource
        str providerType (F):
            The type of the Pluggable Resource Provider that defined the
            Pluggable Resource
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str providerUUID (T):
            The UUID of Pluggable Resource Providerk that defined the
            Pluggable Resource
        bool canDelete (F):
            State if the user can delete this resource
        str providerName (F):
            The name of the Pluggable Resource Provider that defined the
            Pluggable Resource
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        bool canModify (F):
            State if the user can modify this resource
        bool canCreate (F):
            State if the user can create this resource
    """

    ALL_ATTRIBS = {'customerName', 'providers', 'resourceMetadata',
                   'billingEntityName', 'resourceState', 'resourceValues',
                   'providerIcon', 'productOfferUUID', 'resourceName',
                   'resourceCreateDate', 'productOfferName',
                   'providerActionDefinitions', 'providerGroup',
                   'customerUUID', 'resourceUUID', 'billingEntityUUID',
                   'sortOrder', 'providerType', 'lastModifiedTime',
                   'providerUUID', 'providerName', 'canDelete', 'resourceType',
                   'resourceKey', 'canModify', 'canCreate'}
    REQUIRED_ATTRIBS = {'resourceValues', 'resourceName', 'providerUUID',
                        'resourceType', 'sortOrder'}
    OPTIONAL_ATTRIBS = {'productOfferName', 'providerType', 'customerName',
                        'providerName', 'providers', 'canDelete',
                        'resourceKey', 'resourceMetadata', 'billingEntityName',
                        'resourceState', 'providerActionDefinitions',
                        'providerGroup', 'providerIcon', 'customerUUID',
                        'canModify', 'productOfferUUID', 'resourceUUID',
                        'lastModifiedTime', 'canCreate', 'billingEntityUUID',
                        'resourceCreateDate'}
    TYPES = {'customerName': str, 'providers': Dict(str, Dict(str, str)),
             'resourceMetadata': ResourceMetadata, 'billingEntityName': str,
             'resourceState': enums.ResourceState, 'resourceValues':
             Dict(str, str), 'providerIcon': str, 'productOfferUUID': str,
             'resourceName': str, 'resourceCreateDate': datetime,
             'productOfferName': str, 'providerActionDefinitions':
             Dict(str, ActionDefinition), 'providerGroup': str,
             'customerUUID': str, 'resourceUUID': str, 'billingEntityUUID':
             str, 'sortOrder': int, 'providerType': str, 'lastModifiedTime':
             int, 'providerUUID': str, 'canDelete': bool, 'providerName': str,
             'resourceType': enums.ResourceType, 'resourceKey':
             List(ResourceKey), 'canModify': bool, 'canCreate': bool}


class DeploymentTemplate(ComplexObject):

    """FCO REST API DeploymentTemplate complex object.

    Name.

    Attributes (type name (required): description:
        str customerName (F):
            The name of the customer that owns the resource
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        List(Firewall) firewall (F):
            Holds the list of firewalls in a template
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        List(FirewallTemplate) firewallTemplate (F):
            Holds the list of firewall templates in a template
        str deploymentInstanceUUID (F):
            The uuid of the deployment instance the resource is created
            from
        List(Question) questions (F):
            Holds the List of questions in a template
        str vdcUUID (T):
            The UUID of the VDC in which the resource is contained
        str productOfferUUID (F):
            The UUID of the product offer associated with the resource
        str resourceName (T):
            The name of the resource
        List(Disk) disk (F):
            Holds the list of disks in a template
        datetime resourceCreateDate (F):
            The creation date of the resource
        str productOfferName (F):
            The name of the product offer associated with the resource
        str clusterUUID (T):
            The UUID of the cluster in which the resource is located
        List(Network) network (F):
            Holds the list of networks in a template
        TemplateProtectionPermission userPermission (F):
            The user template permissions
        str deploymentInstanceName (F):
            The name of the deployment instance the resource is created
            from
        int sortOrder (T):
            The sort order value for the given resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        str customerUUID (F):
            The UUID of the customer that owns the resource
        str clusterName (F):
            The name of the cluster in which the resource is located
        str instanceChargeProductOfferName (F):
            The name of the product offer used to charge for the
            deployment instance on deploy
        str vdcName (F):
            The name of the VDC in which the resource is contained
        enums.ResourceState resourceState (F):
            The state of the resource
        TemplateProtectionPermission ownerPermission (F):
            The owner template permissions
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        List(SSHKey) sshkey (F):
            Holds the list of sshkeys in a template
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        str instanceChargeProductOfferUUID (F):
            The UUID of the product offer used to charge for the
            deployment instance on deploy
        List(PublishTo) publishedTo (F):
            A list of PublishTo definitions for the resources this
            template has been published to
        List(Server) server (F):
            Holds the list of servers in a template
        List(VDC) vdc (F):
            Holds the list of vdcs in a template
    """

    ALL_ATTRIBS = {'customerName', 'providers', 'firewall', 'resourceMetadata',
                   'billingEntityName', 'firewallTemplate',
                   'deploymentInstanceUUID', 'questions', 'vdcUUID',
                   'productOfferUUID', 'resourceName', 'disk',
                   'resourceCreateDate', 'productOfferName', 'clusterUUID',
                   'network', 'vdc', 'deploymentInstanceName', 'customerUUID',
                   'resourceUUID', 'billingEntityUUID', 'sortOrder',
                   'clusterName', 'instanceChargeProductOfferName', 'vdcName',
                   'resourceState', 'ownerPermission', 'lastModifiedTime',
                   'sshkey', 'resourceType', 'resourceKey',
                   'instanceChargeProductOfferUUID', 'publishedTo', 'server',
                   'userPermission'}
    REQUIRED_ATTRIBS = {'resourceType', 'resourceName', 'clusterUUID',
                        'sortOrder', 'vdcUUID'}
    OPTIONAL_ATTRIBS = {'customerName', 'providers', 'firewall',
                        'resourceMetadata', 'billingEntityName',
                        'firewallTemplate', 'deploymentInstanceUUID',
                        'questions', 'productOfferUUID', 'disk',
                        'resourceCreateDate', 'productOfferName', 'network',
                        'userPermission', 'deploymentInstanceName',
                        'customerUUID', 'resourceUUID', 'billingEntityUUID',
                        'clusterName', 'instanceChargeProductOfferName',
                        'vdcName', 'resourceState', 'ownerPermission',
                        'lastModifiedTime', 'sshkey', 'resourceKey',
                        'instanceChargeProductOfferUUID', 'publishedTo',
                        'server', 'vdc'}
    TYPES = {'customerName': str, 'providers': Dict(str, Dict(str, str)),
             'firewall': List(Firewall), 'resourceMetadata': ResourceMetadata,
             'billingEntityName': str, 'firewallTemplate':
             List(FirewallTemplate), 'deploymentInstanceUUID': str,
             'questions': List(Question), 'vdcUUID': str, 'productOfferUUID':
             str, 'resourceName': str, 'disk': List(Disk),
             'resourceCreateDate': datetime, 'productOfferName': str,
             'clusterUUID': str, 'network': List(Network), 'userPermission':
             TemplateProtectionPermission, 'deploymentInstanceName': str,
             'sortOrder': int, 'resourceUUID': str, 'billingEntityUUID': str,
             'customerUUID': str, 'clusterName': str,
             'instanceChargeProductOfferName': str, 'vdcName': str,
             'resourceState': enums.ResourceState, 'ownerPermission':
             TemplateProtectionPermission, 'lastModifiedTime': int, 'sshkey':
             List(SSHKey), 'resourceType': enums.ResourceType, 'resourceKey':
             List(ResourceKey), 'instanceChargeProductOfferUUID': str,
             'publishedTo': List(PublishTo), 'server': List(Server), 'vdc':
             List(VDC)}


class DeploymentInstance(ComplexObject):

    """FCO REST API DeploymentInstance complex object.

    Name.

    Attributes (type name (required): description:
        str customerName (F):
            The name of the customer that owns the resource
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        List(Firewall) firewall (F):
            Holds the list of firewalls in a template
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        List(FirewallTemplate) firewallTemplate (F):
            Holds the list of firewall templates in a template
        str templateKey (F):
            The server key of the server (for image/server cryptographic
            validation)
        str deploymentInstanceUUID (F):
            The uuid of the deployment instance the resource is created
            from
        List(Question) questions (F):
            Holds the List of questions in a template
        str vdcUUID (T):
            The UUID of the VDC in which the resource is contained
        str productOfferUUID (F):
            The UUID of the product offer associated with the resource
        str resourceName (T):
            The name of the resource
        List(Disk) disk (F):
            Holds the list of disks in a template
        datetime resourceCreateDate (F):
            The creation date of the resource
        str deploymentTemplateUUID (F):
            The UUID of the template
        str clusterUUID (T):
            The UUID of the cluster in which the resource is located
        List(Network) network (F):
            Holds the list of networks in a template
        TemplateProtectionPermission userPermission (F):
            The user template permissions
        str deploymentInstanceName (F):
            The name of the deployment instance the resource is created
            from
        str customerUUID (F):
            The UUID of the customer that owns the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        int sortOrder (T):
            The sort order value for the given resource
        enums.DeploymentInstanceStatus status (F):
            The UUID of the deployment instance
        str productOfferName (F):
            The name of the product offer associated with the resource
        str clusterName (F):
            The name of the cluster in which the resource is located
        str instanceChargeProductOfferName (F):
            The name of the product offer used to charge for the
            deployment instance on deploy
        str vdcName (F):
            The name of the VDC in which the resource is contained
        enums.ResourceState resourceState (F):
            The state of the resource
        TemplateProtectionPermission ownerPermission (F):
            The owner template permissions
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        List(SSHKey) sshkey (F):
            Holds the list of sshkeys in a template
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        str instanceChargeProductOfferUUID (F):
            The UUID of the product offer used to charge for the
            deployment instance on deploy
        List(PublishTo) publishedTo (F):
            A list of PublishTo definitions for the resources this
            template has been published to
        List(Server) server (F):
            Holds the list of servers in a template
        List(VDC) vdc (F):
            Holds the list of vdcs in a template
        str deploymentTemplateName (F):
            The name of the template from which its been instantiated
    """

    ALL_ATTRIBS = {'customerName', 'providers', 'firewall', 'resourceMetadata',
                   'billingEntityName', 'firewallTemplate', 'templateKey',
                   'deploymentInstanceUUID', 'questions', 'vdcUUID',
                   'productOfferUUID', 'resourceName', 'disk',
                   'resourceCreateDate', 'deploymentTemplateUUID',
                   'clusterUUID', 'network', 'vdc', 'deploymentInstanceName',
                   'customerUUID', 'resourceUUID', 'billingEntityUUID',
                   'sortOrder', 'status', 'productOfferName', 'clusterName',
                   'instanceChargeProductOfferName', 'vdcName',
                   'resourceState', 'ownerPermission', 'lastModifiedTime',
                   'sshkey', 'resourceType', 'resourceKey',
                   'instanceChargeProductOfferUUID', 'publishedTo', 'server',
                   'userPermission', 'deploymentTemplateName'}
    REQUIRED_ATTRIBS = {'resourceType', 'resourceName', 'clusterUUID',
                        'sortOrder', 'vdcUUID'}
    OPTIONAL_ATTRIBS = {'customerName', 'providers', 'firewall',
                        'resourceMetadata', 'billingEntityName',
                        'firewallTemplate', 'templateKey',
                        'deploymentInstanceUUID', 'questions',
                        'productOfferUUID', 'disk', 'resourceCreateDate',
                        'deploymentTemplateUUID', 'network', 'userPermission',
                        'deploymentInstanceName', 'customerUUID',
                        'resourceUUID', 'billingEntityUUID', 'status',
                        'productOfferName', 'clusterName',
                        'instanceChargeProductOfferName', 'vdcName',
                        'resourceState', 'ownerPermission', 'lastModifiedTime',
                        'sshkey', 'resourceKey',
                        'instanceChargeProductOfferUUID', 'publishedTo',
                        'server', 'vdc', 'deploymentTemplateName'}
    TYPES = {'customerName': str, 'providers': Dict(str, Dict(str, str)),
             'firewall': List(Firewall), 'resourceMetadata': ResourceMetadata,
             'billingEntityName': str, 'firewallTemplate':
             List(FirewallTemplate), 'templateKey': str,
             'deploymentInstanceUUID': str, 'questions': List(Question),
             'vdcUUID': str, 'productOfferUUID': str, 'resourceName': str,
             'disk': List(Disk), 'resourceCreateDate': datetime,
             'deploymentTemplateUUID': str, 'clusterUUID': str, 'network':
             List(Network), 'userPermission': TemplateProtectionPermission,
             'deploymentInstanceName': str, 'customerUUID': str,
             'resourceUUID': str, 'billingEntityUUID': str, 'sortOrder': int,
             'status': enums.DeploymentInstanceStatus, 'productOfferName': str,
             'clusterName': str, 'instanceChargeProductOfferName': str,
             'vdcName': str, 'resourceState': enums.ResourceState,
             'ownerPermission': TemplateProtectionPermission,
             'lastModifiedTime': int, 'sshkey': List(SSHKey), 'resourceType':
             enums.ResourceType, 'resourceKey': List(ResourceKey),
             'instanceChargeProductOfferUUID': str, 'publishedTo':
             List(PublishTo), 'server': List(Server), 'vdc': List(VDC),
             'deploymentTemplateName': str}


class ProductPurchase(ComplexObject):

    """FCO REST API ProductPurchase complex object.

    Name.

    Attributes (type name (required): description:
        bool donotRebill (T):
            A flag to indicate billing further billing periods should
            not be run
        datetime endDate (F):
            The end date/time of the product period
        str description (F):
            A textual description of the product purchase
        datetime startDate (T):
            The start date/time of the product purchase
        datetime purchaseDate (T):
            The date/time the product purchase was made
        datetime lastBillPeriod (F):
            The end date/time of the last billing period
        int instanceKey (F):
            A field to help managing billing of products purchased
        bool active (F):
            A flag indicating whether the product purchase is currently
            active
        str referenceUUID (F):
            The UUID of the product purchase (deprecated please use
            purchaseUUID )
        str purchaseUUID (F):
            The UUID of the product purchase
        str customerUUID (T):
            The UUID of the customer associated with the product
            purchase
        str vdcUUID (F):
            The UUID of the VDC associated with the product purchase
        str productOfferUUID (T):
            The UUID of the associated product offer
        str resourceUUID (T):
            The UUID of the resource associated with the product
            purchase
        List(ProductComponent) purchasedConfig (F):
            This will holed the configuration of the resource at the
            purchased time. Note this can not be used for FQL filtering
        str billingEntityUUID (F):
            The UUID of the billing entity associated with the product
            purchase
        datetime nextBillPeriod (F):
            The start date/time of the next billing period
        int productID (F):
            The underlying productid of the product offer which linked
            with the current purchase
    """

    ALL_ATTRIBS = {'donotRebill', 'endDate', 'description', 'startDate',
                   'purchaseDate', 'lastBillPeriod', 'nextBillPeriod',
                   'productOfferUUID', 'referenceUUID', 'purchaseUUID',
                   'customerUUID', 'vdcUUID', 'active', 'resourceUUID',
                   'purchasedConfig', 'billingEntityUUID', 'instanceKey',
                   'productID'}
    REQUIRED_ATTRIBS = {'donotRebill', 'startDate', 'purchaseDate',
                        'customerUUID', 'productOfferUUID', 'resourceUUID'}
    OPTIONAL_ATTRIBS = {'endDate', 'description', 'lastBillPeriod',
                        'instanceKey', 'referenceUUID', 'purchaseUUID',
                        'vdcUUID', 'active', 'purchasedConfig',
                        'billingEntityUUID', 'nextBillPeriod', 'productID'}
    TYPES = {'donotRebill': bool, 'endDate': datetime, 'description': str,
             'startDate': datetime, 'purchaseDate': datetime, 'lastBillPeriod':
             datetime, 'instanceKey': int, 'active': bool, 'referenceUUID':
             str, 'purchaseUUID': str, 'customerUUID': str, 'vdcUUID': str,
             'productOfferUUID': str, 'resourceUUID': str, 'purchasedConfig':
             List(ProductComponent), 'billingEntityUUID': str,
             'nextBillPeriod': datetime, 'productID': int}


class UnitTransaction(ComplexObject):

    """FCO REST API UnitTransaction complex object.

    Name.

    Attributes (type name (required): description:
        str linkedResourceUUID (T):
            The UUID of the resource linked with the unit tranaction
        datetime chargedToDate (T):
            The end of the period to which the subject matter of the
            transaction relates
        ProductPurchase linkedPurchase (T):
            The Product Purchase which is linked with the Transaction
        str description (T):
            The textual description of the transaction
        str linkedServerName (T):
            The name of the server linked with the unit tranaction
        enums.ResourceType resourceType (T):
            The type of the resource
        float closingBalance (T):
            The closing balance after the unit transaction
        datetime transactionDate (T):
            The date on which the unit transaction occurred
        str linkedResourceName (T):
            The name of the resource linked with the unit tranaction
        enums.UnitType unitsType (T):
            The unit type associated with the unit transaction
        enums.ResourceType linkedResourceType (T):
            The resource type of the resource linked with the unit
            tranaction
        float openingBalance (T):
            The open balance before the unit transaction
        str linkedServerUUID (T):
            The server UUID, if the link resource was part of a server
            at that time
        int billingEntityId (T):
            The numeric ID of the Billing Entity
        str customerUUID (T):
            The UUID of the customer
        str vdcUUID (T):
            The UUID of the vdc which is linked with the transaction
        str descriptionDetail (T):
            The textual description of the detail of the transaction
        int unitTransactionId (T):
            The numeric ID of the unit transaction
        datetime chargedFromDate (T):
            The start of the period to which the subject matter of the
            transaction relates
        str billingEntityUUID (T):
            Billing Entity UUID of the customer
        float transactionAmount (T):
            The amount of the unit transaction
    """

    ALL_ATTRIBS = {'linkedResourceUUID', 'chargedToDate', 'linkedPurchase',
                   'description', 'linkedServerName', 'resourceType',
                   'closingBalance', 'transactionDate', 'linkedResourceName',
                   'unitsType', 'linkedResourceType', 'openingBalance',
                   'linkedServerUUID', 'billingEntityId', 'customerUUID',
                   'vdcUUID', 'descriptionDetail', 'unitTransactionId',
                   'chargedFromDate', 'billingEntityUUID', 'transactionAmount'}
    REQUIRED_ATTRIBS = {'linkedResourceUUID', 'chargedToDate',
                        'linkedPurchase', 'description', 'linkedServerName',
                        'resourceType', 'closingBalance', 'transactionDate',
                        'linkedResourceName', 'unitsType',
                        'linkedResourceType', 'openingBalance',
                        'linkedServerUUID', 'billingEntityId', 'customerUUID',
                        'vdcUUID', 'descriptionDetail', 'unitTransactionId',
                        'chargedFromDate', 'billingEntityUUID',
                        'transactionAmount'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'linkedResourceUUID': str, 'chargedToDate': datetime,
             'linkedPurchase': ProductPurchase, 'description': str,
             'linkedServerName': str, 'resourceType': enums.ResourceType,
             'closingBalance': float, 'transactionDate': datetime,
             'linkedResourceName': str, 'unitsType': enums.UnitType,
             'linkedResourceType': enums.ResourceType, 'openingBalance': float,
             'linkedServerUUID': str, 'billingEntityId': int, 'customerUUID':
             str, 'vdcUUID': str, 'descriptionDetail': str,
             'unitTransactionId': int, 'chargedFromDate': datetime,
             'billingEntityUUID': str, 'transactionAmount': float}


class Product(ComplexObject):

    """FCO REST API Product complex object.

    Name.

    Attributes (type name (required): description:
        enums.ResourceType associatedType (T):
            The associated resource type (or pseudo-resource type) that
            the product builds when purchased
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        bool isEditable (F):
            This indicates if the Product is editable
        bool inUse (F):
            Indicates if purchases already exists for this product offer
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str extendedType (T):
            The pluggable provider type associated with Pluggable
            Resource product
        int sortOrder (T):
            The sort order value for the given resource
        List(ProductComponentType) components (T):
            List of Product Component Types that together comprise the
            product
        str resourceName (T):
            The name of the resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        datetime resourceCreateDate (F):
            The creation date of the resource
    """

    ALL_ATTRIBS = {'associatedType', 'resourceMetadata', 'isEditable', 'inUse',
                   'resourceType', 'resourceKey', 'providers',
                   'billingEntityName', 'resourceState', 'extendedType',
                   'sortOrder', 'components', 'resourceUUID', 'resourceName',
                   'lastModifiedTime', 'billingEntityUUID',
                   'resourceCreateDate'}
    REQUIRED_ATTRIBS = {'associatedType', 'resourceType', 'extendedType',
                        'sortOrder', 'components', 'resourceName'}
    OPTIONAL_ATTRIBS = {'isEditable', 'providers', 'resourceKey',
                        'resourceMetadata', 'billingEntityName',
                        'resourceState', 'inUse', 'resourceUUID',
                        'lastModifiedTime', 'billingEntityUUID',
                        'resourceCreateDate'}
    TYPES = {'associatedType': enums.ResourceType, 'providers':
             Dict(str, Dict(str, str)), 'isEditable': bool, 'inUse': bool,
             'resourceType': enums.ResourceType, 'resourceKey':
             List(ResourceKey), 'resourceMetadata': ResourceMetadata,
             'billingEntityName': str, 'resourceState': enums.ResourceState,
             'extendedType': str, 'sortOrder': int, 'components':
             List(ProductComponentType), 'resourceName': str, 'resourceUUID':
             str, 'lastModifiedTime': int, 'billingEntityUUID': str,
             'resourceCreateDate': datetime}


class ProviderData(ComplexObject):

    """FCO REST API ProviderData complex object.

    Name.

    Attributes (type name (required): description:
        str resourceType (T):
            The associated resource type
        bool useWithBilling (T):
            State if the provider should be used with the billing system
        bool allowCustomerEdit (T):
            State if the customer should be allowed to edit the provider
            settings
        List(ProductComponentType) productComponentTypes (T):
            The product component types used with the provider
    """

    ALL_ATTRIBS = {'resourceType', 'useWithBilling', 'allowCustomerEdit',
                   'productComponentTypes'}
    REQUIRED_ATTRIBS = {'resourceType', 'useWithBilling', 'allowCustomerEdit',
                        'productComponentTypes'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'resourceType': str, 'useWithBilling': bool, 'allowCustomerEdit':
             bool, 'productComponentTypes': List(ProductComponentType)}


class ProductOffer(ComplexObject):

    """FCO REST API ProductOffer complex object.

    Name.

    Attributes (type name (required): description:
        List(str) linkedProviders (F):
            A list of the provider types of linked configuration
            providers
        bool isEditable (F):
            Indicates if this product offer is editable
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        enums.UnitType unitType (F):
            The type of units associated with the product offer
        str resourceName (T):
            The name of the resource
        Dict(str, ProductComponentType) productComponentTypes (F):
            A list of the product component types that make up this
            product offer. This can not be queried by FQL and only
            available when the resources is loaded with children
        datetime resourceCreateDate (F):
            The creation date of the resource
        str productUUID (T):
            Holds the UUID of the linked product
        int sortOrder (T):
            The sort order value for the given resource
        List(str) clusters (F):
            The list of clusters with which Product Offer can be used
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        str productExtendedType (F):
            The accociated extended type of the linked product
        str productName (F):
            Holds the name of the product
        str resourceUUID (F):
            The UUID of the resource (read-only)
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        enums.ResourceType productAssociatedType (F):
            The accociated resource type of the linked product
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        List(ProductComponent) componentConfig (T):
            Holds the compoment configuration. Note that this cannot be
            queried using FQL
        enums.BillingPeriod billingPeriod (T):
            The billing period associated with the product offer (i.e
            how often a billing line is generated)
        bool inUse (F):
            Indicates if purchases already exists for this product offer
    """

    ALL_ATTRIBS = {'linkedProviders', 'isEditable', 'providers',
                   'resourceMetadata', 'billingEntityName', 'resourceState',
                   'unitType', 'resourceName', 'productComponentTypes',
                   'resourceCreateDate', 'productUUID', 'sortOrder',
                   'resourceUUID', 'billingEntityUUID', 'productExtendedType',
                   'productName', 'clusters', 'lastModifiedTime',
                   'productAssociatedType', 'resourceType', 'resourceKey',
                   'componentConfig', 'billingPeriod', 'inUse'}
    REQUIRED_ATTRIBS = {'productUUID', 'resourceType', 'componentConfig',
                        'billingPeriod', 'sortOrder', 'resourceName'}
    OPTIONAL_ATTRIBS = {'productAssociatedType', 'linkedProviders', 'clusters',
                        'isEditable', 'providers', 'billingEntityUUID',
                        'resourceKey', 'resourceMetadata', 'billingEntityName',
                        'resourceState', 'productName', 'unitType',
                        'productExtendedType', 'inUse', 'resourceUUID',
                        'lastModifiedTime', 'productComponentTypes',
                        'resourceCreateDate'}
    TYPES = {'linkedProviders': List(str), 'isEditable': bool, 'providers':
             Dict(str, Dict(str, str)), 'resourceMetadata': ResourceMetadata,
             'billingEntityName': str, 'resourceState': enums.ResourceState,
             'unitType': enums.UnitType, 'resourceName': str,
             'productComponentTypes': Dict(str, ProductComponentType),
             'resourceCreateDate': datetime, 'productUUID': str, 'sortOrder':
             int, 'clusters': List(str), 'billingEntityUUID': str,
             'productExtendedType': str, 'productName': str, 'resourceUUID':
             str, 'lastModifiedTime': int, 'productAssociatedType':
             enums.ResourceType, 'resourceType': enums.ResourceType,
             'resourceKey': List(ResourceKey), 'componentConfig':
             List(ProductComponent), 'billingPeriod': enums.BillingPeriod,
             'inUse': bool}


class PluggableResourceProvider(ComplexObject):

    """FCO REST API PluggableResourceProvider complex object.

    Name.

    Attributes (type name (required): description:
        List(str) associatedResourceTypes (T):
            A list of associated resource types
        Dict(str, Dict(str, str)) providers (F):
            The config provider values
        str fdlDescription (T):
            The description of the function
        ResourceMetadata resourceMetadata (F):
            The metadata attached to the resource
        str billingEntityName (F):
            The Name of the Billing Entity to which the resource belongs
        enums.ResourceState resourceState (F):
            The state of the resource
        str providerIcon (T):
            The icon of the provider
        str resourceName (T):
            The name of the resource
        List(ProductComponentType) productComponentTypes (T):
            List of Product Component Types associated with pluggable
            provider
        datetime resourceCreateDate (F):
            The creation date of the resource
        Dict(str, ActionDefinition) actionDefinitions (T):
            The actions that are available to this provider
        bool inUse (T):
            State if the provider is in use
        str fdlUUID (T):
            The UUID of FDL Code Block that contains the provider
        str providerGroup (T):
            The grouping of the provider
        int sortOrder (T):
            The sort order value for the given resource
        str resourceUUID (F):
            The UUID of the resource (read-only)
        str billingEntityUUID (F):
            The UUID of the Billing Entity to which the resource belongs
        str providerType (T):
            The type of the provider
        Dict(str, ProviderData) providerData (T):
            Product Component Types sorted by associated resource type
        int lastModifiedTime (F):
            The time, in milliseconds from epoch, when the resource was
            last modified.
        str fdlName (T):
            The name of the FDL Code Block that contains the provider
        bool canDelete (T):
            State if the user can delete pluggable resources using this
            provider
        enums.ResourceType resourceType (T):
            The type of the resource
        List(ResourceKey) resourceKey (F):
            The keys attached to the resource
        bool canModify (T):
            State if the user can modify pluggable resources using this
            provider
        bool canCreate (T):
            State if the user can create pluggable resources using this
            provider
    """

    ALL_ATTRIBS = {'associatedResourceTypes', 'providers', 'fdlDescription',
                   'resourceMetadata', 'billingEntityName', 'resourceState',
                   'providerIcon', 'resourceName', 'productComponentTypes',
                   'resourceCreateDate', 'actionDefinitions', 'inUse',
                   'fdlUUID', 'providerGroup', 'sortOrder', 'resourceUUID',
                   'billingEntityUUID', 'providerType', 'providerData',
                   'lastModifiedTime', 'fdlName', 'canDelete', 'resourceType',
                   'resourceKey', 'canModify', 'canCreate'}
    REQUIRED_ATTRIBS = {'canDelete', 'canModify', 'fdlName',
                        'associatedResourceTypes', 'inUse', 'resourceType',
                        'actionDefinitions', 'fdlDescription', 'providerType',
                        'fdlUUID', 'providerGroup', 'providerData',
                        'providerIcon', 'sortOrder', 'resourceName',
                        'canCreate', 'productComponentTypes'}
    OPTIONAL_ATTRIBS = {'providers', 'resourceKey', 'resourceMetadata',
                        'billingEntityName', 'resourceState', 'resourceUUID',
                        'lastModifiedTime', 'billingEntityUUID',
                        'resourceCreateDate'}
    TYPES = {'associatedResourceTypes': List(str), 'providers':
             Dict(str, Dict(str, str)), 'fdlDescription': str,
             'resourceMetadata': ResourceMetadata, 'billingEntityName': str,
             'resourceState': enums.ResourceState, 'providerIcon': str,
             'resourceName': str, 'productComponentTypes':
             List(ProductComponentType), 'resourceCreateDate': datetime,
             'actionDefinitions': Dict(str, ActionDefinition), 'inUse': bool,
             'fdlUUID': str, 'providerGroup': str, 'sortOrder': int,
             'resourceUUID': str, 'billingEntityUUID': str, 'providerType':
             str, 'providerData': Dict(str, ProviderData), 'lastModifiedTime':
             int, 'fdlName': str, 'canDelete': bool, 'resourceType':
             enums.ResourceType, 'resourceKey': List(ResourceKey), 'canModify':
             bool, 'canCreate': bool}


class ImportVmSpec(ComplexObject):

    """FCO REST API ImportVmSpec complex object.

    Name.

    Attributes (type name (required): description:
        str externalVmXML (T):
                     No documentation is available for this field #####
        Server externalVm (T):
                     No documentation is available for this field #####
        List(ProductOffer) diskOffers (T):
                     No documentation is available for this field #####
        List(ProductOffer) networkOffers (T):
                     No documentation is available for this field #####
        List(ProductOffer) serverOffers (T):
                     No documentation is available for this field #####
        List(Network) availableNetworks (T):
                     No documentation is available for this field #####
    """

    ALL_ATTRIBS = {'serverOffers', 'externalVm', 'diskOffers', 'networkOffers',
                   'externalVmXML', 'availableNetworks'}
    REQUIRED_ATTRIBS = {'externalVmXML', 'externalVm', 'diskOffers',
                        'networkOffers', 'serverOffers', 'availableNetworks'}
    OPTIONAL_ATTRIBS = set()
    TYPES = {'externalVmXML': str, 'externalVm': Server, 'diskOffers':
             List(ProductOffer), 'networkOffers': List(ProductOffer),
             'serverOffers': List(ProductOffer), 'availableNetworks':
             List(Network)}
