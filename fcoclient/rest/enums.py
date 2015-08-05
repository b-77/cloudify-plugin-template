# coding=UTF-8

"""All the REST enums used by the FCO REST API."""

from enum import Enum


class PrintableEnum(Enum):

    """Allows for easier formatting when substituting for parameters."""

    def __str__(self):
        return self.value

    def untype(self):
        return self.value


class DeploymentInstanceStatus(PrintableEnum):

    """FCO REST API DeploymentInstanceStatus enum

    The DeploymentInstanceStatus enum represents the status of a
    deployment instance.
    BUILDING:   Building
    RECOVERY:   Undergoing live recovery
    DELETING:   Deleting
    REBOOTING:  Rebooting
    INSTALLING: Installing
    RUNNING:    Running
    STOPPED:    Stopped
    ERROR:      Internal error state
    STOPPING:   Stopping
    MIGRATING:  Migrating
    STARTING:   Starting
    """

    BUILDING = 'BUILDING'
    RECOVERY = 'RECOVERY'
    DELETING = 'DELETING'
    REBOOTING = 'REBOOTING'
    INSTALLING = 'INSTALLING'
    RUNNING = 'RUNNING'
    STOPPED = 'STOPPED'
    ERROR = 'ERROR'
    STOPPING = 'STOPPING'
    MIGRATING = 'MIGRATING'
    STARTING = 'STARTING'


class Networking(PrintableEnum):

    """FCO REST API Networking enum

    The SystemCapability Networking enum enumerates the different
    networking capabilities of a system or cluster.
    VLAN: VLAN networking modes are permitted
    PVIP: PVIP networking modes are permitted
    """

    VLAN = 'VLAN'
    PVIP = 'PVIP'


class HypervisorType(PrintableEnum):

    """FCO REST API HypervisorType enum

    A enum that represents the hyper visor type.
    HYPERV: Hyper V Hypervisor Type
    KVM:    KVM Hypervisor Type
    PCS:    PCS Hypervisor Type
    XEN4:   XEN4 Hypervisor Type
    XEN3:   XEN3 Hypervisor Type
    VMWARE: VM Ware Hypervisor Type
    """

    HYPERV = 'HYPERV'
    KVM = 'KVM'
    PCS = 'PCS'
    XEN4 = 'XEN4'
    XEN3 = 'XEN3'
    VMWARE = 'VMWARE'


class BillingEntityVAR(PrintableEnum):

    """FCO REST API BillingEntityVAR enum

    The BillingEntityVAR enum specifies a variable for a BillingEntity.
    FROM_ADDRESS:      The From: address on outbound emails
    SUPPORT_URL:       The URL for technical support for the email
    BCC_ADDRESS:       The BCC: address on outbound emails
    CONTROL_PANEL_URL: The URL of the control panel
    CC_ADDRESS:        The CC: address on outbound emails
    COMPANY_NAME:      The company name of the Billing Entity
    REPLY_TO:          The Reply-To: address on outbound emails
    EMAIL_FOOTER:      The footer for the email
    """

    FROM_ADDRESS = 'FROM_ADDRESS'
    SUPPORT_URL = 'SUPPORT_URL'
    BCC_ADDRESS = 'BCC_ADDRESS'
    CONTROL_PANEL_URL = 'CONTROL_PANEL_URL'
    CC_ADDRESS = 'CC_ADDRESS'
    COMPANY_NAME = 'COMPANY_NAME'
    REPLY_TO = 'REPLY_TO'
    EMAIL_FOOTER = 'EMAIL_FOOTER'


class FirewallConnectionState(PrintableEnum):

    """FCO REST API FirewallConnectionState enum

    The FirewallConnectionState enum enumerates the possible connection
    states used within a FirewallTemplate.
    NEW:      New connections
    ALL:      Any state
    EXISTING: Existing connections
    """

    NEW = 'NEW'
    ALL = 'ALL'
    EXISTING = 'EXISTING'


class EmailType(PrintableEnum):

    """FCO REST API EmailType enum

    The EmailType enum enumerates the different types of email sent by
    the system.
    GENERAL_EMAIL:        The general email template where subject and
                          message is set by customer
    NEW_PASSWORD_DETAILS: Sent to a user with a new password after a
                          password reset
    ACCOUNT_ACTIVATION:   Sent when an account has been activated
                          automatically
    REVOKE_USER:          Sent when a user's access is revoked from a
                          customer account
    CREDIT_NOTE:          Sent with an attached credit note.
    AUTO_TOP_UP_FAIL:     Sent to inform the customer of a failed
                          autotopup
    PASSWORD_RESET_LINK:  Sent to a user who requests a password reset
    INVITE_USER:          Sent when a user is invited to join a customer
                          account
    ZERO_BALANCE:         Sent to a customer who reaches a zero unit
                          balance
    LOW_BALANCE:          Sent to a customer whose balance reaches the
                          low balance warning threshold
    PAID_INVOICE:         Email template when an invoice that has been
                          emialed to the customer has been paid.
    ACCOUNT_APPROVAL:     Sent when an account has been activated
                          manually
    AUTO_TOP_UP_SUCCESS:  Sent to inform the customer of a successful
                          autotopup
    ACCOUNT_CANCELLATION: Sent when a customer's account is cancelled
    INVOICE:              Sent with an attached invoice
    """

    GENERAL_EMAIL = 'GENERAL_EMAIL'
    NEW_PASSWORD_DETAILS = 'NEW_PASSWORD_DETAILS'
    ACCOUNT_ACTIVATION = 'ACCOUNT_ACTIVATION'
    REVOKE_USER = 'REVOKE_USER'
    CREDIT_NOTE = 'CREDIT_NOTE'
    AUTO_TOP_UP_FAIL = 'AUTO_TOP_UP_FAIL'
    PASSWORD_RESET_LINK = 'PASSWORD_RESET_LINK'
    INVITE_USER = 'INVITE_USER'
    ZERO_BALANCE = 'ZERO_BALANCE'
    LOW_BALANCE = 'LOW_BALANCE'
    PAID_INVOICE = 'PAID_INVOICE'
    ACCOUNT_APPROVAL = 'ACCOUNT_APPROVAL'
    AUTO_TOP_UP_SUCCESS = 'AUTO_TOP_UP_SUCCESS'
    ACCOUNT_CANCELLATION = 'ACCOUNT_CANCELLATION'
    INVOICE = 'INVOICE'


class InvoiceStatus(PrintableEnum):

    """FCO REST API InvoiceStatus enum

    The InvoiceStatus enum enumerates the different statuses that an
    invoice can take.
    LOCKED:  Locked, for processing
    VOID:    Void (i.e. the invoice was never finalised because its
             creation was cancelled)
    PAID:    Valid, finalised and paid
    UNPAID:  Valid, finalised but unpaid
    CLOSED:  Closed, after processing
    PENDING: Pending (i.e. under construction)
    """

    LOCKED = 'LOCKED'
    VOID = 'VOID'
    PAID = 'PAID'
    UNPAID = 'UNPAID'
    CLOSED = 'CLOSED'
    PENDING = 'PENDING'


class Publish(PrintableEnum):

    """FCO REST API Publish enum

    The SystemCapability Publish enum enumerates the different image
    publishing capabilities of a system.
    BE_ADMIN:           Billing entity admins are permitted to publish
    ANY:                Any Customer are permitted to publish
    VALIDATED_CUSTOMER: Validated customers are permitted to publish
    """

    BE_ADMIN = 'BE_ADMIN'
    ANY = 'ANY'
    VALIDATED_CUSTOMER = 'VALIDATED_CUSTOMER'


class Invoicing(PrintableEnum):

    """FCO REST API Invoicing enum

    The SystemCapability Invoicing enum enumerates the different options
    for invoicing in system.
    FALSE: Invoicing is not set
    TRUE:  Invoicing is set
    """

    FALSE = 'FALSE'
    TRUE = 'TRUE'


class BillingPeriod(PrintableEnum):

    """FCO REST API BillingPeriod enum

    The PeriodType enum enumerates the different types of billing or
    rating period.
    HOURLY:   Hourly charge
    MONTHLY:  Monthly charge
    DAILY:    Daily charge
    ANNUALLY: Annual charge
    ONE_OFF:  One off charge
    WEEKLY:   Weekly charge
    """

    HOURLY = 'HOURLY'
    MONTHLY = 'MONTHLY'
    DAILY = 'DAILY'
    ANNUALLY = 'ANNUALLY'
    ONE_OFF = 'ONE_OFF'
    WEEKLY = 'WEEKLY'


class FirewallRuleAction(PrintableEnum):

    """FCO REST API FirewallRuleAction enum

    The FirewallRuleAction enum enumerates what actions are permitted
    within a firewall rule.
    DROP:   Drop the packet
    ALLOW:  Allow the packet through
    REJECT: Reject the packet with an unreachable
    """

    DROP = 'DROP'
    ALLOW = 'ALLOW'
    REJECT = 'REJECT'


class FirewallProtocol(PrintableEnum):

    """FCO REST API FirewallProtocol enum

    The FirewallProtocol enum enumerates the permissible types of IP
    protocol within a FirewallTemplate.
    UDP:       UDP
    IPSEC_AH:  IPSEC AH
    IPSEC_ESP: IPSEC ESP
    TCP:       TCP
    GRE:       GRE
    ICMP6:     ICMPV6
    L2TP:      L2TP
    ICMP:      ICMP
    ANY:       Any protocol
    """

    UDP = 'UDP'
    IPSEC_AH = 'IPSEC_AH'
    IPSEC_ESP = 'IPSEC_ESP'
    TCP = 'TCP'
    GRE = 'GRE'
    ICMP6 = 'ICMP6'
    L2TP = 'L2TP'
    ICMP = 'ICMP'
    ANY = 'ANY'


class Email(PrintableEnum):

    """FCO REST API Email enum

    The SystemCapability Email enum enumerates the different email
    capabilities of a system.
    YES: The BE can send email
    NO:  The BE cannot send email
    """

    YES = 'YES'
    NO = 'NO'


class JobType(PrintableEnum):

    """FCO REST API JobType enum

    The JobType enum enumerates the different types of job.
    ATTACH_SSHKEY:                            Attach SSH key job
    DELETE_IMAGE_TEMPLATE:                    Delete image template job
    SUBSTITUTE_ALL_PRODUCT_PURCHASES:         Called when you substitue
                                              all product purchases for
                                              one product offer for
                                              another
    DISK_MIGRATE:                             Migrate disk job
    CREATE_PROMOTION:                         Create a Promotion
    MODIFY_SERVER:                            Modify server job
    MODIFY_PAYMENT_PROVIDER:                  Modify a Payment Provider
    DELETE_SSHKEY:                            Delete SSH key job
    MODIFY_TEMPLATE:                          Modify template job
    DELETE_SUBNET:                            Delete subnet job
    CREATE_SUBNET:                            Create subnet job
    DELETE_JOB:                               Delete job job
    CREATE_REFERRAL_PROMO_CODE:               Create a Referral Promo
                                              Code
    DEPLOY_TEMPLATE:                          Deploy deployment instance
                                              job
    MODIFY_SERVICE_NETWORK:                   Called when a service
                                              network is to be updated
    FETCH_RESOURCE:                           Fetch resource job
    CREATE_VDC:                               Create VDC job
    DELETE_CLUSTER:                           Delete a Cluster
    MODIFY_PRODUCT_OFFER:                     Modify a Product Offer
    MAKE_PAYMENT:                             Make a payment or refund
    SERVER_STOPPED:                           Server was stopped without
                                              user interaction from the
                                              API
    MODIFY_SUBNET:                            Modify subnet job
    INVOKE_PLUGGABLE_RESOURCE:                Invoke a Pluggable
                                              Resource Action
    CREATE_NETWORK:                           Create network job
    START_SERVER:                             Start server job
    FIREWALL_CREATE:                          Create firewall job
    CREATE_TEMPLATE:                          Create deployment instance
                                              job
    REMOVE_IP_FROM_NIC:                       Remove IP address from NIC
                                              job
    MODIFY_DISK:                              Modify disk job
    MODIFY_FIREWALL_TEMPLATE:                 Modify firewall template
                                              job
    ATTACH_DISK:                              Attach disk job
    CREATE_BILLING_ENTITY:                    Create a Billing Entity
    CREATE_GROUP:                             Create group job
    CREATE_INTERNETWORKING_NETWORK:           Create a INTERNETWORKING
                                              Network
    CLONE_DISK:                               Clone disk job
    DELETE_STORAGE_GROUP:                     Called when a Storage
                                              Group is deleted.
    ATTACH_SUBNET:                            Attach subnet job
    DELETE_REFERRAL_PROMO_CODE:               Delete a Referral Promo
                                              Code
    DELETE_PAYMENT_METHOD_INSTANCE:           Delete a payment method
                                              instance
    MODIFY_TEMPLATE_INSTANCE:                 Modify deployment instance
                                              job
    MODIFY_PRODUCT:                           Modify a Product
    UPDATE_INSTANCE_STATE:                    Change deployment instance
                                              state
    DELETE_GROUP:                             Delete group job
    REVOKE_TEMPLATE:                          Revoke template job
    MODIFY_TRANSLATION:                       Modify a Translation
    CONFIGURE_PAYMENT_METHOD:                 Configure a payment method
    CREATE_VLAN:                              Create VLAN job
    MODIFY_GROUP:                             Modify group job
    DELETE_SNAPSHOT:                          Delete snapshot job
    DELETE_PLUGGABLE_RESOURCE:                Delete a Pluggable
                                              Resource
    CREATE_CUSTOMER:                          Create a Customer
    MODIFY_PAYMENT_METHOD_INSTANCE:           Modify a payment method
                                              instance
    REVERT_DISK:                              Revert disk job
    PURCHASE_UNIT_PRODUCT:                    Purchase a unit product
    CREATE_FIREWALL_TEMPLATE:                 Create firewall template
                                              job
    ADD_IP_TO_NIC:                            Add IP address to NIC job
    REVOKE_IMAGE:                             Revoke image job
    PURCHASE_PRODUCT_OFFER:                   Called when you purchase a
                                              product offer through the
                                              API
    CREATE_FDL:                               Create a FDL Code Block
    MODIFY_PLUGGABLE_RESOURCE_ADVERTISE_KEYS: Called when a pluggable
                                              resource advertise keys
                                              have been modified
    MODIFY_SNAPSHOT:                          Modify snapshot job
    DELETE_PRODUCT_OFFER:                     Delete product offer job
    SIGN_FDL_CODE_BLOCK:                      Called when a FDL Code
                                              Block is signed.
    CREATE_IMAGE_TEMPLATE:                    Create image template job
    CREATE_SERVICE_NETWORK:                   Create a SERVICE Network
    FETCH_DISK:                               Fetch disk job
    NODE_STATUS_CHANGE:                       Called when a node status
                                              changes
    MODIFY_FDL:                               Modify a FDL Code Block
    REBOOT_SERVER:                            Reboot server job
    MODIFY_REFERRAL_PROMOTION:                Modify a Referral
                                              Promotion
    REVERT_SERVER:                            Revert server job
    CANCEL_TRANSACTION:                       Cancel a transaction
    IMPORT_SERVER:                            Called when import a
                                              server
    DELETE_CUSTOMER:                          Delete Customer Job
    DELETE_TEMPLATE_INSTANCE:                 Delete deployment instance
                                              job
    CREATE_USER:                              Create a User
    PUBLISH_TEMPLATE:                         Publish template job
    DELETE_FIREWALL_TEMPLATE:                 Delete firewall template
                                              job
    DELETE_VLAN:                              Delete VLAN job
    MODIFY_SSHKEY:                            Modify SSH key job
    DELETE_SERVER:                            Delete server job
    MODIFY_PLUGGABLE_RESOURCE:                Modify a Pluggable
                                              Resource
    CREATE_PAYMENT_METHOD_INSTANCE:           Create a payment method
                                              instance
    MOVE_SUBNET:                              Move subnet job
    REFUND_TRANSACTION:                       Refund a transaction.
    CREATE_NIC:                               Create NIC job
    CREATE_SSHKEY:                            Create SSH key job
    MODIFY_USER:                              Modify a User
    MODIFY_IMAGE:                             Modify image job
    MIGRATE_SERVER:                           Called when a server is
                                              migrated to a new node
    MODIFY_STORAGE_GROUP:                     Called when a Storage
                                              Group is modified.
    DETACH_DISK:                              Detach disk job
    CREATE_DISK:                              Create disk job
    FIREWALL_RULE_MODIFY:                     Modify firewall rule job
    CREATE_REFERRAL_PROMOTION:                Create a Referral
                                              Promotion
    DELETE_TEMPLATE:                          Delete template job
    CREATE_CLUSTER:                           Create a Cluster
    MODIFY_CUSTOMER:                          Modify a Customer
    CREATE_STORAGE_GROUP:                     Called when a Storage
                                              Group is created.
    RESIZE_DISK:                              Resize disk job
    DETACH_NIC:                               Detach NIC job
    MODIFY_BLOB:                              Modify a Blob
    ATTACH_NIC:                               Attach NIC job
    DELETE_NIC:                               Delete NIC job
    FETCH_IMAGE:                              Fetch image job
    MODIFY_CLUSTER:                           Modify a Cluster
    MODIFY_VDC:                               Modify VDC job
    MAKE_SERVER_VISIBLE:                      Make server visisble job
    CREATE_PRODUCT:                           Create a product
    MODIFY_NIC:                               Modify NIC job
    MODIFY_BILLING_ENTITY:                    Modify a Billing Entity
    MODIFY_FIREWALL:                          Modify firewall job
    APPLY_FIREWALL_TEMPLATE:                  Apply firewall template
                                              job
    CANCEL_JOB:                               Cancel job job
    DELETE_USER:                              Delete user job
    RENAME_DISK:                              Rename disk job
    INVOKE_PCT_ACTION:                        Invoke a Config Provider
                                              PCT action
    KILL_SERVER:                              Kill server job
    DELETE_DISK:                              Delete disk job
    CREATE_PRODUCT_OFFER:                     Create a product offer
    MODIFY_REFERRAL_PROMO_CODE:               Modify a Referral Promo
                                              Code
    CREATE_PLUGGABLE_RESOURCE:                Create a Pluggable
                                              Resource
    DELETE_FIREWALL:                          Delete firewall job
    SCHEDULED_JOB:                            Schedule job job
    DELETE_RESOURCE:                          Delete a Resource
    TEST_PAYMENT_METHOD:                      Test a payment method
    PUBLISH_IMAGE:                            Publish image job
    CREATE_PROMO_CODE:                        Create a Promo Code
    CREATE_INVOICE:                           Create an invoice
    CLONE_SERVER:                             Clone server job
    DELETE_FIREWALL_RULE:                     Delete firewall rule job
    DELETE_PROMO_CODE:                        Delete a Promo Code
    SHUTDOWN_SERVER:                          Shutdown server job
    CREATE_PAYMENT_METHOD:                    Create an Payment Method
    DELETE_VDC:                               Delete VDC job
    MODIFY_RESOURCE:                          Modify resource job
    FIREWALL_RULE_ADD:                        Add firewall rule job
    DELETE_NETWORK:                           Delete network job
    MODIFY_NETWORK:                           Modify network job
    CREATE_SERVER:                            Create server job
    MODIFY_PROMOTION:                         Modify a Promotion
    CREATE_TRANSLATION:                       Create a Translation
    CREATE_SNAPSHOT:                          Create snapshot job
    DETACH_SSHKEY:                            Detach SSH key job
    CREATE_BLOB:                              CreateBlob
    RESUME_TRANSACTION:                       Resume a transaction
    """

    ATTACH_SSHKEY = 'ATTACH_SSHKEY'
    DELETE_IMAGE_TEMPLATE = 'DELETE_IMAGE_TEMPLATE'
    SUBSTITUTE_ALL_PRODUCT_PURCHASES = 'SUBSTITUTE_ALL_PRODUCT_PURCHASES'
    DISK_MIGRATE = 'DISK_MIGRATE'
    CREATE_PROMOTION = 'CREATE_PROMOTION'
    MODIFY_SERVER = 'MODIFY_SERVER'
    MODIFY_PAYMENT_PROVIDER = 'MODIFY_PAYMENT_PROVIDER'
    DELETE_SSHKEY = 'DELETE_SSHKEY'
    MODIFY_TEMPLATE = 'MODIFY_TEMPLATE'
    DELETE_SUBNET = 'DELETE_SUBNET'
    CREATE_SUBNET = 'CREATE_SUBNET'
    DELETE_JOB = 'DELETE_JOB'
    CREATE_REFERRAL_PROMO_CODE = 'CREATE_REFERRAL_PROMO_CODE'
    DEPLOY_TEMPLATE = 'DEPLOY_TEMPLATE'
    MODIFY_SERVICE_NETWORK = 'MODIFY_SERVICE_NETWORK'
    FETCH_RESOURCE = 'FETCH_RESOURCE'
    CREATE_VDC = 'CREATE_VDC'
    DELETE_CLUSTER = 'DELETE_CLUSTER'
    MODIFY_PRODUCT_OFFER = 'MODIFY_PRODUCT_OFFER'
    MAKE_PAYMENT = 'MAKE_PAYMENT'
    SERVER_STOPPED = 'SERVER_STOPPED'
    MODIFY_SUBNET = 'MODIFY_SUBNET'
    INVOKE_PLUGGABLE_RESOURCE = 'INVOKE_PLUGGABLE_RESOURCE'
    CREATE_NETWORK = 'CREATE_NETWORK'
    START_SERVER = 'START_SERVER'
    FIREWALL_CREATE = 'FIREWALL_CREATE'
    CREATE_TEMPLATE = 'CREATE_TEMPLATE'
    REMOVE_IP_FROM_NIC = 'REMOVE_IP_FROM_NIC'
    MODIFY_DISK = 'MODIFY_DISK'
    MODIFY_FIREWALL_TEMPLATE = 'MODIFY_FIREWALL_TEMPLATE'
    ATTACH_DISK = 'ATTACH_DISK'
    CREATE_BILLING_ENTITY = 'CREATE_BILLING_ENTITY'
    CREATE_GROUP = 'CREATE_GROUP'
    CREATE_INTERNETWORKING_NETWORK = 'CREATE_INTERNETWORKING_NETWORK'
    CLONE_DISK = 'CLONE_DISK'
    DELETE_STORAGE_GROUP = 'DELETE_STORAGE_GROUP'
    ATTACH_SUBNET = 'ATTACH_SUBNET'
    DELETE_REFERRAL_PROMO_CODE = 'DELETE_REFERRAL_PROMO_CODE'
    DELETE_PAYMENT_METHOD_INSTANCE = 'DELETE_PAYMENT_METHOD_INSTANCE'
    MODIFY_TEMPLATE_INSTANCE = 'MODIFY_TEMPLATE_INSTANCE'
    MODIFY_PRODUCT = 'MODIFY_PRODUCT'
    UPDATE_INSTANCE_STATE = 'UPDATE_INSTANCE_STATE'
    DELETE_GROUP = 'DELETE_GROUP'
    REVOKE_TEMPLATE = 'REVOKE_TEMPLATE'
    MODIFY_TRANSLATION = 'MODIFY_TRANSLATION'
    CONFIGURE_PAYMENT_METHOD = 'CONFIGURE_PAYMENT_METHOD'
    CREATE_VLAN = 'CREATE_VLAN'
    MODIFY_GROUP = 'MODIFY_GROUP'
    DELETE_SNAPSHOT = 'DELETE_SNAPSHOT'
    DELETE_PLUGGABLE_RESOURCE = 'DELETE_PLUGGABLE_RESOURCE'
    CREATE_CUSTOMER = 'CREATE_CUSTOMER'
    MODIFY_PAYMENT_METHOD_INSTANCE = 'MODIFY_PAYMENT_METHOD_INSTANCE'
    REVERT_DISK = 'REVERT_DISK'
    PURCHASE_UNIT_PRODUCT = 'PURCHASE_UNIT_PRODUCT'
    CREATE_FIREWALL_TEMPLATE = 'CREATE_FIREWALL_TEMPLATE'
    ADD_IP_TO_NIC = 'ADD_IP_TO_NIC'
    REVOKE_IMAGE = 'REVOKE_IMAGE'
    PURCHASE_PRODUCT_OFFER = 'PURCHASE_PRODUCT_OFFER'
    CREATE_FDL = 'CREATE_FDL'
    MODIFY_PLUGGABLE_RESOURCE_ADVERTISE_KEYS = 'MODIFY_PLUGGABLE_RESOURCE_ADV'\
                                               'ERTISE_KEYS'
    MODIFY_SNAPSHOT = 'MODIFY_SNAPSHOT'
    DELETE_PRODUCT_OFFER = 'DELETE_PRODUCT_OFFER'
    SIGN_FDL_CODE_BLOCK = 'SIGN_FDL_CODE_BLOCK'
    CREATE_IMAGE_TEMPLATE = 'CREATE_IMAGE_TEMPLATE'
    CREATE_SERVICE_NETWORK = 'CREATE_SERVICE_NETWORK'
    FETCH_DISK = 'FETCH_DISK'
    NODE_STATUS_CHANGE = 'NODE_STATUS_CHANGE'
    MODIFY_FDL = 'MODIFY_FDL'
    REBOOT_SERVER = 'REBOOT_SERVER'
    MODIFY_REFERRAL_PROMOTION = 'MODIFY_REFERRAL_PROMOTION'
    REVERT_SERVER = 'REVERT_SERVER'
    CANCEL_TRANSACTION = 'CANCEL_TRANSACTION'
    IMPORT_SERVER = 'IMPORT_SERVER'
    DELETE_CUSTOMER = 'DELETE_CUSTOMER'
    DELETE_TEMPLATE_INSTANCE = 'DELETE_TEMPLATE_INSTANCE'
    CREATE_USER = 'CREATE_USER'
    PUBLISH_TEMPLATE = 'PUBLISH_TEMPLATE'
    DELETE_FIREWALL_TEMPLATE = 'DELETE_FIREWALL_TEMPLATE'
    DELETE_VLAN = 'DELETE_VLAN'
    MODIFY_SSHKEY = 'MODIFY_SSHKEY'
    DELETE_SERVER = 'DELETE_SERVER'
    MODIFY_PLUGGABLE_RESOURCE = 'MODIFY_PLUGGABLE_RESOURCE'
    CREATE_PAYMENT_METHOD_INSTANCE = 'CREATE_PAYMENT_METHOD_INSTANCE'
    MOVE_SUBNET = 'MOVE_SUBNET'
    REFUND_TRANSACTION = 'REFUND_TRANSACTION'
    CREATE_NIC = 'CREATE_NIC'
    CREATE_SSHKEY = 'CREATE_SSHKEY'
    MODIFY_USER = 'MODIFY_USER'
    MODIFY_IMAGE = 'MODIFY_IMAGE'
    MIGRATE_SERVER = 'MIGRATE_SERVER'
    MODIFY_STORAGE_GROUP = 'MODIFY_STORAGE_GROUP'
    DETACH_DISK = 'DETACH_DISK'
    CREATE_DISK = 'CREATE_DISK'
    FIREWALL_RULE_MODIFY = 'FIREWALL_RULE_MODIFY'
    CREATE_REFERRAL_PROMOTION = 'CREATE_REFERRAL_PROMOTION'
    DELETE_TEMPLATE = 'DELETE_TEMPLATE'
    CREATE_CLUSTER = 'CREATE_CLUSTER'
    MODIFY_CUSTOMER = 'MODIFY_CUSTOMER'
    CREATE_STORAGE_GROUP = 'CREATE_STORAGE_GROUP'
    RESIZE_DISK = 'RESIZE_DISK'
    DETACH_NIC = 'DETACH_NIC'
    MODIFY_BLOB = 'MODIFY_BLOB'
    ATTACH_NIC = 'ATTACH_NIC'
    DELETE_NIC = 'DELETE_NIC'
    FETCH_IMAGE = 'FETCH_IMAGE'
    MODIFY_CLUSTER = 'MODIFY_CLUSTER'
    MODIFY_VDC = 'MODIFY_VDC'
    MAKE_SERVER_VISIBLE = 'MAKE_SERVER_VISIBLE'
    CREATE_PRODUCT = 'CREATE_PRODUCT'
    MODIFY_NIC = 'MODIFY_NIC'
    MODIFY_BILLING_ENTITY = 'MODIFY_BILLING_ENTITY'
    MODIFY_FIREWALL = 'MODIFY_FIREWALL'
    APPLY_FIREWALL_TEMPLATE = 'APPLY_FIREWALL_TEMPLATE'
    CANCEL_JOB = 'CANCEL_JOB'
    DELETE_USER = 'DELETE_USER'
    RENAME_DISK = 'RENAME_DISK'
    INVOKE_PCT_ACTION = 'INVOKE_PCT_ACTION'
    KILL_SERVER = 'KILL_SERVER'
    DELETE_DISK = 'DELETE_DISK'
    CREATE_PRODUCT_OFFER = 'CREATE_PRODUCT_OFFER'
    MODIFY_REFERRAL_PROMO_CODE = 'MODIFY_REFERRAL_PROMO_CODE'
    CREATE_PLUGGABLE_RESOURCE = 'CREATE_PLUGGABLE_RESOURCE'
    DELETE_FIREWALL = 'DELETE_FIREWALL'
    SCHEDULED_JOB = 'SCHEDULED_JOB'
    DELETE_RESOURCE = 'DELETE_RESOURCE'
    TEST_PAYMENT_METHOD = 'TEST_PAYMENT_METHOD'
    PUBLISH_IMAGE = 'PUBLISH_IMAGE'
    CREATE_PROMO_CODE = 'CREATE_PROMO_CODE'
    CREATE_INVOICE = 'CREATE_INVOICE'
    CLONE_SERVER = 'CLONE_SERVER'
    DELETE_FIREWALL_RULE = 'DELETE_FIREWALL_RULE'
    DELETE_PROMO_CODE = 'DELETE_PROMO_CODE'
    SHUTDOWN_SERVER = 'SHUTDOWN_SERVER'
    CREATE_PAYMENT_METHOD = 'CREATE_PAYMENT_METHOD'
    DELETE_VDC = 'DELETE_VDC'
    MODIFY_RESOURCE = 'MODIFY_RESOURCE'
    FIREWALL_RULE_ADD = 'FIREWALL_RULE_ADD'
    DELETE_NETWORK = 'DELETE_NETWORK'
    MODIFY_NETWORK = 'MODIFY_NETWORK'
    CREATE_SERVER = 'CREATE_SERVER'
    MODIFY_PROMOTION = 'MODIFY_PROMOTION'
    CREATE_TRANSLATION = 'CREATE_TRANSLATION'
    CREATE_SNAPSHOT = 'CREATE_SNAPSHOT'
    DETACH_SSHKEY = 'DETACH_SSHKEY'
    CREATE_BLOB = 'CREATE_BLOB'
    RESUME_TRANSACTION = 'RESUME_TRANSACTION'


class Status(PrintableEnum):

    """FCO REST API Status enum

    The Status enum enumerates the possible statuses for a customer.
    ACTIVE:   The account is active, and a normal customer
    ADMIN:    The account is active, and an admin customer
    DISABLED: The customer has been disabled
    DELETED:  The customer has been deleted
    CLOSED:   The account has been closed
    """

    ACTIVE = 'ACTIVE'
    ADMIN = 'ADMIN'
    DISABLED = 'DISABLED'
    DELETED = 'DELETED'
    CLOSED = 'CLOSED'


class Vnc(PrintableEnum):

    """FCO REST API Vnc enum

    The SystemCapability vnc enum indicates the supported VNC handlers.
    RAW:       Supports raw handlers
    GUACAMOLE: Supports Guacamole handlers
    """

    RAW = 'RAW'
    GUACAMOLE = 'GUACAMOLE'


class IPType(PrintableEnum):

    """FCO REST API IPType enum

    The IPType enum enumerates the different types of IP addresses.
    IPV4:    IPv4 address
    INVALID: Invalid IP address
    IPV6:    IPv6 address
    """

    IPV4 = 'IPV4'
    INVALID = 'INVALID'
    IPV6 = 'IPV6'


class BentoBox(PrintableEnum):

    """FCO REST API BentoBox enum

    The SystemCapability Bentobox enum enumerates the different options
    for Bentobox in system.
    FALSE: Bentobox option is not set
    TRUE:  Bentobox option is set
    """

    FALSE = 'FALSE'
    TRUE = 'TRUE'


class PaymentFunction(PrintableEnum):

    """FCO REST API PaymentFunction enum

    Enum values representing the supported payment provider functions.
    REMOVE_PAYMENT_INSTANCE:   Remove payment instance function
    SELF_TEST:                 Test function
    UNDEF:                     Undefined
    UPDATE_PAYMENT_METHOD:     Update payment function
    REGISTER_PAYMENT_INSTANCE: Register payment instance function
    REFUND_TRANSACTION:        Refund transaction function
    MAKE_PAYMENT:              Make payment function
    REGISTER_PAYMENT_METHOD:   Register payment function
    CANCEL_TRANSACTION:        Cancel transaction function
    REFUND_PAYMENT:            Refund payment function
    """

    REMOVE_PAYMENT_INSTANCE = 'REMOVE_PAYMENT_INSTANCE'
    SELF_TEST = 'SELF_TEST'
    UNDEF = 'UNDEF'
    UPDATE_PAYMENT_METHOD = 'UPDATE_PAYMENT_METHOD'
    REGISTER_PAYMENT_INSTANCE = 'REGISTER_PAYMENT_INSTANCE'
    REFUND_TRANSACTION = 'REFUND_TRANSACTION'
    MAKE_PAYMENT = 'MAKE_PAYMENT'
    REGISTER_PAYMENT_METHOD = 'REGISTER_PAYMENT_METHOD'
    CANCEL_TRANSACTION = 'CANCEL_TRANSACTION'
    REFUND_PAYMENT = 'REFUND_PAYMENT'


class Signup(PrintableEnum):

    """FCO REST API Signup enum

    The SystemCapability Signup enum enumerates the different signup
    capabilities of a system.
    MANUAL_SIGNUP: Manual signup is permitted
    AUTO_SIGNUP:   Automatic signup is permitted
    """

    MANUAL_SIGNUP = 'MANUAL_SIGNUP'
    AUTO_SIGNUP = 'AUTO_SIGNUP'


class InvocationType(PrintableEnum):

    """FCO REST API InvocationType enum

    An enum that represents the invocation type of an action.
    INSTANCE: An action that is invoked using a resource instance
    STATIC:   An action that is invoked without a resource instance
    """

    INSTANCE = 'INSTANCE'
    STATIC = 'STATIC'


class Aggregation(PrintableEnum):

    """FCO REST API Aggregation enum

    The Aggregation enum enumerates the available types of aggregation
    function.
    COUNT:   Count the aggregated values
    MAX:     Find the maximum of the aggregated values
    AVERAGE: Find the average of the aggregated values
    SUM:     Sum the aggregated values
    MIN:     Find the minimum of the aggregated values
    """

    COUNT = 'COUNT'
    MAX = 'MAX'
    AVERAGE = 'AVERAGE'
    SUM = 'SUM'
    MIN = 'MIN'


class ResourceState(PrintableEnum):

    """FCO REST API ResourceState enum

    The ResourceState enum enumerates the different states of resources.
    TO_BE_DELETED: Deletion pending on deletion of child objects
    LOCKED:        Locked
    CREATING:      Creating
    DELETED:       Deleted
    ACTIVE:        Active
    HIDDEN:        Hidden
    """

    TO_BE_DELETED = 'TO_BE_DELETED'
    LOCKED = 'LOCKED'
    CREATING = 'CREATING'
    DELETED = 'DELETED'
    ACTIVE = 'ACTIVE'
    HIDDEN = 'HIDDEN'


class UserType(PrintableEnum):

    """FCO REST API UserType enum

    An enum that represents the type of user.
    USER:         A traditional user type, that exists across a single
                  Billing Entity
    API_KEY_USER: An API Key user type, that exists within a single
                  Customer
    """

    USER = 'USER'
    API_KEY_USER = 'API_KEY_USER'


class UnitType(PrintableEnum):

    """FCO REST API UnitType enum

    The UnitType enum enumerates the available types of unit.
    NONCARRYOVER: Non-carry-over units
    CARRYOVER:    Carry-over units
    """

    NONCARRYOVER = 'NONCARRYOVER'
    CARRYOVER = 'CARRYOVER'


class ServerCapability(PrintableEnum):

    """FCO REST API ServerCapability enum

    The ServerCapability enum enumerates the different server
    capabilities.
    CAN_ATTACH_DISK_WHEN_RUNNING:  Capability to attach disk while the
                                   server is running
    CAN_DETACH_NIC_WHEN_RUNNING:   Capability to detach NIC while the
                                   server is running
    CAN_DECREASE_CPU_WHEN_RUNNING: Capability to decrease CPU while the
                                   server is running
    CAN_SNAPSHOT_WHEN_RUNNING:     Capability to snapshot while the
                                   server is running
    CAN_DETACH_ISO_WHEN_RUNNING:   Capability to detach ISO while the
                                   server is running
    CAN_ATTACH_NIC_WHEN_RUNNING:   Capability to attach NIC while the
                                   server is running
    CAN_CLONE_WHEN_RUNNING:        Capability to clone while the server
                                   is running
    CAN_RESIZE_DISK_WHEN_RUNNING:  Capability to resize disk while the
                                   server is running
    CAN_ATTACH_ISO_WHEN_RUNNING:   Capability to attach ISO while the
                                   server is running
    CAN_INCREASE_RAM_WHEN_RUNNING: Capability to increase RAM while the
                                   server is running
    CAN_DECREASE_RAM_WHEN_RUNNING: Capability to decrease RAM while the
                                   server is running
    CAN_INCREASE_CPU_WHEN_RUNNING: Capability to increase CPU while the
                                   server is running
    CAN_DETACH_DISK_WHEN_RUNNING:  Capability to detach disk while the
                                   server is running
    CAN_REVERT_WHEN_RUNNING:       Capability to revert while the server
                                   is running
    """

    CAN_ATTACH_DISK_WHEN_RUNNING = 'CAN_ATTACH_DISK_WHEN_RUNNING'
    CAN_DETACH_NIC_WHEN_RUNNING = 'CAN_DETACH_NIC_WHEN_RUNNING'
    CAN_DECREASE_CPU_WHEN_RUNNING = 'CAN_DECREASE_CPU_WHEN_RUNNING'
    CAN_SNAPSHOT_WHEN_RUNNING = 'CAN_SNAPSHOT_WHEN_RUNNING'
    CAN_DETACH_ISO_WHEN_RUNNING = 'CAN_DETACH_ISO_WHEN_RUNNING'
    CAN_ATTACH_NIC_WHEN_RUNNING = 'CAN_ATTACH_NIC_WHEN_RUNNING'
    CAN_CLONE_WHEN_RUNNING = 'CAN_CLONE_WHEN_RUNNING'
    CAN_RESIZE_DISK_WHEN_RUNNING = 'CAN_RESIZE_DISK_WHEN_RUNNING'
    CAN_ATTACH_ISO_WHEN_RUNNING = 'CAN_ATTACH_ISO_WHEN_RUNNING'
    CAN_INCREASE_RAM_WHEN_RUNNING = 'CAN_INCREASE_RAM_WHEN_RUNNING'
    CAN_DECREASE_RAM_WHEN_RUNNING = 'CAN_DECREASE_RAM_WHEN_RUNNING'
    CAN_INCREASE_CPU_WHEN_RUNNING = 'CAN_INCREASE_CPU_WHEN_RUNNING'
    CAN_DETACH_DISK_WHEN_RUNNING = 'CAN_DETACH_DISK_WHEN_RUNNING'
    CAN_REVERT_WHEN_RUNNING = 'CAN_REVERT_WHEN_RUNNING'


class FirewallRuleDirection(PrintableEnum):

    """FCO REST API FirewallRuleDirection enum

    The FirewallRuleDirection enum enumerates the directions available
    for a FirewallTempate.
    IN:  Inbound (i.e. traffic travelling towards the server)
    OUT: Outbound (i.e. traffic travelling away from the server)
    """

    IN = 'IN'
    OUT = 'OUT'


class EmailVAR(PrintableEnum):

    """FCO REST API EmailVAR enum

    The EmailVAR enumerates the configurable variables for emails.
    CARD_NAME:         The card name used within the email concerned
    CUST_UUID:         The customer uuid used within the email concerned
    EMAIL_BODY:        The general email body
    FAILURE_REASON:    The failure reason used within the email
                       concerned
    CURRENCY:          The currency used within the email concerned
    COMPANY_NAME:      The Company name for the email concerned
    UNIT_BALANCE:      The unit balance used within the email concerned
    DATE:              The date used within the email concerned
    CARD_CHARGE:       The credit card charge used within the email
                       concerned
    INVITER:           The inviting user used within the email concerned
    UNIT_CHARGE:       The number of units charged for used within the
                       email concerned
    URL_PARAMS:        The parameters to a URL used within the email
                       concerned
    FROM_ADDRESS:      The From: address for the email concerned
    SUPPORT_URL:       The support URL used within the email concerned
    USER_LOGIN:        The user login used within the email concerned
    BCC_ADDRESS:       The BCC: address for the email concerned
    CONTROL_PANEL_URL: The Control Panel URL for the email concerned
    INVOICE_NUMBER:    The invoice number used within the email
                       concerned
    EMAIL_FOOTER:      The email footer for the email concerned
    TOTAL:             The total currency value used within the email
                       concerned
    CARD_NUMBER:       The card number used within the email concerned
    ACTIVATION_KEY:    The activation key sent within the email
                       concerned
    REPLY_TO:          The Reply-To: address for the email concerned
    PASSWORD:          The password sent within the email concerned
    UNITS:             The number of units used within the email
                       concerned
    CUST_NAME:         The customer name used within the email concerned
    CC_ADDRESS:        The CC: address for the email concerned
    EMAIL_SUBJECT:     The general email subject
    """

    CARD_NAME = 'CARD_NAME'
    CUST_UUID = 'CUST_UUID'
    EMAIL_BODY = 'EMAIL_BODY'
    FAILURE_REASON = 'FAILURE_REASON'
    CURRENCY = 'CURRENCY'
    COMPANY_NAME = 'COMPANY_NAME'
    UNIT_BALANCE = 'UNIT_BALANCE'
    DATE = 'DATE'
    CARD_CHARGE = 'CARD_CHARGE'
    INVITER = 'INVITER'
    UNIT_CHARGE = 'UNIT_CHARGE'
    URL_PARAMS = 'URL_PARAMS'
    FROM_ADDRESS = 'FROM_ADDRESS'
    SUPPORT_URL = 'SUPPORT_URL'
    USER_LOGIN = 'USER_LOGIN'
    BCC_ADDRESS = 'BCC_ADDRESS'
    CONTROL_PANEL_URL = 'CONTROL_PANEL_URL'
    INVOICE_NUMBER = 'INVOICE_NUMBER'
    EMAIL_FOOTER = 'EMAIL_FOOTER'
    TOTAL = 'TOTAL'
    CARD_NUMBER = 'CARD_NUMBER'
    ACTIVATION_KEY = 'ACTIVATION_KEY'
    REPLY_TO = 'REPLY_TO'
    PASSWORD = 'PASSWORD'
    UNITS = 'UNITS'
    CUST_NAME = 'CUST_NAME'
    CC_ADDRESS = 'CC_ADDRESS'
    EMAIL_SUBJECT = 'EMAIL_SUBJECT'


class EmulatedDevices(PrintableEnum):

    """FCO REST API EmulatedDevices enum

    The SystemCapability EmulatedDevices enum indicates if the
    underlying cluster allows user to enable/disable emullated devives
    on the server start up.
    ALLOW_DISABLED: Cluster emulated devices are set to be disabled
    ALLOW_ENABLED:  Cluster emulated devices are set to be enabled
    ALLOW_ANY:      Cluser allow both emulated devices to unabled or
                    disabled
    """

    ALLOW_DISABLED = 'ALLOW_DISABLED'
    ALLOW_ENABLED = 'ALLOW_ENABLED'
    ALLOW_ANY = 'ALLOW_ANY'


class Condition(PrintableEnum):

    """FCO REST API Condition enum

    The Condition enum specifies a condition used within a SearchFilter.
    NOT_ENDS_WITH:               True if FQL field concerned when parsed
                                 as a string does not end with the value
                                 supplied
    IS_EQUAL_TO:                 True if FQL field concerned is equal to
                                 one of the values supplied as an array
    LATER_THAN:                  True if FQL field concerned is later
                                 than the value supplied
    CONTAINS:                    True if FQL field concerned when parsed
                                 as a string contains the value supplied
    IS_GREATER_THAN:             True if FQL field concerned is greater
                                 than the value supplied
    IS_LESS_THAN_OR_EQUAL_TO:    True if FQL field concerned is less
                                 than or equal to than the value
                                 supplied
    NOT_BETWEEN:                 True if FQL field concerned does not
                                 lie between the two values supplied
                                 (i.e. is less than the first or is
                                 greater than the second)
    NOT_CONTAINS:                True if FQL field concerned when parsed
                                 as a string does contain the value
                                 supplied
    IS_LESS_THAN:                True if FQL field concerned is less
                                 than the value supplied
    EARLIER_THAN:                True if FQL field concerned is earlier
                                 than the value supplied
    BETWEEN:                     True if FQL field concerned lies
                                 between the two values supplied (i.e.
                                 is greater than or equal to the first
                                 and is less than or equal to the
                                 second)
    IS_GREATER_THAN_OR_EQUAL_TO: True if FQL field concerned is greater
                                 than or equal to than the value
                                 supplied
    NOT_STARTS_WITH:             True if FQL field concerned when parsed
                                 as a string does not start with the
                                 value supplied
    ENDS_WITH:                   True if FQL field concerned when parsed
                                 as a string ends with the value
                                 supplied
    STARTS_WITH:                 True if FQL field concerned when parsed
                                 as a string starts with the value
                                 supplied
    IS_NOT_EQUAL_TO:             True if FQL field concerned is not
                                 equal to any of the values supplied as
                                 an array
    """

    NOT_ENDS_WITH = 'NOT_ENDS_WITH'
    IS_EQUAL_TO = 'IS_EQUAL_TO'
    LATER_THAN = 'LATER_THAN'
    CONTAINS = 'CONTAINS'
    IS_GREATER_THAN = 'IS_GREATER_THAN'
    IS_LESS_THAN_OR_EQUAL_TO = 'IS_LESS_THAN_OR_EQUAL_TO'
    NOT_BETWEEN = 'NOT_BETWEEN'
    NOT_CONTAINS = 'NOT_CONTAINS'
    IS_LESS_THAN = 'IS_LESS_THAN'
    EARLIER_THAN = 'EARLIER_THAN'
    BETWEEN = 'BETWEEN'
    IS_GREATER_THAN_OR_EQUAL_TO = 'IS_GREATER_THAN_OR_EQUAL_TO'
    NOT_STARTS_WITH = 'NOT_STARTS_WITH'
    ENDS_WITH = 'ENDS_WITH'
    STARTS_WITH = 'STARTS_WITH'
    IS_NOT_EQUAL_TO = 'IS_NOT_EQUAL_TO'


class InvocationLevel(PrintableEnum):

    """FCO REST API InvocationLevel enum

    The InvocationLevel enum value represents the type of authentication
    that is required to invoke a FDL function.
    CUSTOMER: Specifies that the function can only be invoked through
              the User API
    BE:       Specifies that the function can only be invoked through
              the Admin API
    OPEN:     Specifies that the function can only be invoked through
              the Open API
    MBE:      Specifies that the function can only be invoked through
              the Admin API by the MBE
    """

    CUSTOMER = 'CUSTOMER'
    BE = 'BE'
    OPEN = 'OPEN'
    MBE = 'MBE'


class TaxType(PrintableEnum):

    """FCO REST API TaxType enum

    The different tax types applicable.
    NONE:  None
    OTHER: Other
    VAT:   Vat
    """

    NONE = 'NONE'
    OTHER = 'OTHER'
    VAT = 'VAT'


class ReportChartType(PrintableEnum):

    """FCO REST API ReportChartType enum

    An enum value representing the type of report chart.
    COLUMN: A column chart
    LINE:   A line chart
    BAR:    A bar chart
    PIE:    A pie chart
    AREA:   An area chart
    """

    COLUMN = 'COLUMN'
    LINE = 'LINE'
    BAR = 'BAR'
    PIE = 'PIE'
    AREA = 'AREA'


class Limits(PrintableEnum):

    """FCO REST API Limits enum

    The Limits enum enumerates the resource limits set on a customer.
    REFUND:                     The boolean flag which controls refund
                                generation
    MAX_IPv6_SUBNETS:           The maximum allowed IPv6 subnets for the
                                customer
    NO_3DS_28_DAY_SPEND_LIMIT:  The maximum amount billed permissible in
                                a 28 day period without 3DS security
                                checks
    MAX_SUBNETS:                The maximum number of subnets permitted
    CUTOFF_LIMIT:               The currency value at which currency
                                customers are cut off
    OVERALL_28_DAY_SPEND_LIMIT: The maximum amount billed permissible in
                                a 28 day period overall
    MAX_IPv4_ADDRESSES:         The maximum allowed IPv4 address for the
                                customer
    MAX_DISKS:                  The maximum number of disks permitted
    MAX_IMAGES:                 The maximum number of images permitted
    MAX_VDCS:                   The maximum number of VDCs permitted
    MAX_NETWORK_PRIVATE:        The maximum allowed private networks for
                                the customer
    CREDIT_LIMIT_DUE_DAYS:      The credit invoice due days limit
    CUTOFF_BALANCE:             The unit balance level at which
                                customers should be cut off
    MAX_SNAPSHOTS:              The maximum number of snapshots
                                permitted
    CREDIT_LIMIT:               The maximum outstanding credit balance
                                permitted
    MAX_SERVERS:                The maximum number of servers permitted
    MAX_CPUS:                   The maximum number of CPUs permitted
                                across all servers
    MAX_BLOBS:                  The maximum number of blobs allowed
    MAX_STORAGEGB:              The maximum amount of storage (in GB)
                                permitted across all servers
    MAX_VLANS:                  The maximum number of VLANs permitted
                                per VDC
    MAX_NETWORK_PUBLIC:         The maximum allowed public networks for
                                the customer
    MAX_BLOB_SIZE:              The maximum size of blobs allowed
    MAX_CUSTOMER_USERS:         The maximum number of contacts/users
                                permitted
    MAX_RAM:                    The maximum amount of RAM permitted
                                across all servers
    CUTOFF_DUE_DAYS:            The cut-off invoice due days limit
    """

    REFUND = 'REFUND'
    MAX_IPv6_SUBNETS = 'MAX_IPv6_SUBNETS'
    NO_3DS_28_DAY_SPEND_LIMIT = 'NO_3DS_28_DAY_SPEND_LIMIT'
    MAX_SUBNETS = 'MAX_SUBNETS'
    CUTOFF_LIMIT = 'CUTOFF_LIMIT'
    OVERALL_28_DAY_SPEND_LIMIT = 'OVERALL_28_DAY_SPEND_LIMIT'
    MAX_IPv4_ADDRESSES = 'MAX_IPv4_ADDRESSES'
    MAX_DISKS = 'MAX_DISKS'
    MAX_IMAGES = 'MAX_IMAGES'
    MAX_VDCS = 'MAX_VDCS'
    MAX_NETWORK_PRIVATE = 'MAX_NETWORK_PRIVATE'
    CREDIT_LIMIT_DUE_DAYS = 'CREDIT_LIMIT_DUE_DAYS'
    CUTOFF_BALANCE = 'CUTOFF_BALANCE'
    MAX_SNAPSHOTS = 'MAX_SNAPSHOTS'
    CREDIT_LIMIT = 'CREDIT_LIMIT'
    MAX_SERVERS = 'MAX_SERVERS'
    MAX_CPUS = 'MAX_CPUS'
    MAX_BLOBS = 'MAX_BLOBS'
    MAX_STORAGEGB = 'MAX_STORAGEGB'
    MAX_VLANS = 'MAX_VLANS'
    MAX_NETWORK_PUBLIC = 'MAX_NETWORK_PUBLIC'
    MAX_BLOB_SIZE = 'MAX_BLOB_SIZE'
    MAX_CUSTOMER_USERS = 'MAX_CUSTOMER_USERS'
    MAX_RAM = 'MAX_RAM'
    CUTOFF_DUE_DAYS = 'CUTOFF_DUE_DAYS'


class ReferralStatus(PrintableEnum):

    """FCO REST API ReferralStatus enum

    The referral status enum enumerates the possible statuses of a
    referral.
    COMPLETED:         Completed
    EXPIRED:           Expired
    LIVE:              Live
    AWAITING_PURCHASE: Awaiting purchase
    """

    COMPLETED = 'COMPLETED'
    EXPIRED = 'EXPIRED'
    LIVE = 'LIVE'
    AWAITING_PURCHASE = 'AWAITING_PURCHASE'


class JobStatus(PrintableEnum):

    """FCO REST API JobStatus enum

    The JobStatus enum enumerates the different statuses available for
    jobs.
    SUCCESSFUL:  The job completed successfully
    NOT_STARTED: The job has not yet started (for instance because it
                 has been scheduled for a future time)
    FAILED:      The job failed
    WAITING:     The job is waiting for a subsidiary action to complete
                 (e.g. a child job)
    SUSPENDED:   The job has been suspended
    CANCELLED:   The job was cancelled
    IN_PROGRESS: The job is currently in progress
    """

    SUCCESSFUL = 'SUCCESSFUL'
    NOT_STARTED = 'NOT_STARTED'
    FAILED = 'FAILED'
    WAITING = 'WAITING'
    SUSPENDED = 'SUSPENDED'
    CANCELLED = 'CANCELLED'
    IN_PROGRESS = 'IN_PROGRESS'


class NetworkType(PrintableEnum):

    """FCO REST API NetworkType enum

    The NetworkType enum specifies the type of the network.
    IP:           A public virtual IP network
    INTERWORKING: An interworking VLAN
    PUBLIC:       A public VLAN network
    SERVICE:      A service network
    PRIVATE:      A private VLAN network
    """

    IP = 'IP'
    INTERWORKING = 'INTERWORKING'
    PUBLIC = 'PUBLIC'
    SERVICE = 'SERVICE'
    PRIVATE = 'PRIVATE'


class Capability(PrintableEnum):

    """FCO REST API Capability enum

    The Capability class describes an action (verb) that is mediated by
    the permissions system.
    ALL:                Do any action with resources
    CHANGE_PERMISSIONS: Change permissions on resources
    DO_TRANSACTION:     Do a payment transaction
    CLONE:              Clone resources
    MODIFY:             Modify resources
    PUBLISH:            Publish resources
    INTERACT:           Perform interactive management
    START_STOP:         Start, stop, or change the status of resources
                        (including reboot and kill)
    DELETE:             Delete resources
    FETCH:              Fetch resources
    ATTACH_DETACH:      Attach or detach resources
    CREATE:             Create resources
    """

    ALL = 'ALL'
    CHANGE_PERMISSIONS = 'CHANGE_PERMISSIONS'
    DO_TRANSACTION = 'DO_TRANSACTION'
    CLONE = 'CLONE'
    MODIFY = 'MODIFY'
    PUBLISH = 'PUBLISH'
    INTERACT = 'INTERACT'
    START_STOP = 'START_STOP'
    DELETE = 'DELETE'
    FETCH = 'FETCH'
    ATTACH_DETACH = 'ATTACH_DETACH'
    CREATE = 'CREATE'


class ResultOrder(PrintableEnum):

    """FCO REST API ResultOrder enum

    The ResultOrder enum specifies the order in which results of a
    search are to be returned.
    ASC:  Ascending order
    DESC: Descending order
    """

    ASC = 'ASC'
    DESC = 'DESC'


class MaxLimit(PrintableEnum):

    """FCO REST API MaxLimit enum

    The SystemCapability MaxLimit enum enumerates the different limits
    for servers of a system or cluster.
    MAX_DISK_PER_SERVER:   Maximum number of disks that can be attached
                           to a server
    MAX_REFERRAL_UNIT_CAP: Maximum referral units a customer can be
                           entitled to
    MAX_NIC_PER_SERVER:    Maximum number of NICs that can be attached
                           to a server
    """

    MAX_DISK_PER_SERVER = 'MAX_DISK_PER_SERVER'
    MAX_REFERRAL_UNIT_CAP = 'MAX_REFERRAL_UNIT_CAP'
    MAX_NIC_PER_SERVER = 'MAX_NIC_PER_SERVER'


class FDLReturnType(PrintableEnum):

    """FCO REST API FDLReturnType enum

    Enum that represents the return types of a FDL function that can be
    invoked by the API.
    FUNCTION:  An action or command for the user interface to manage
    DIALOGUE:  An object containing multiple values
    STRING:    A string value
    URL:       A URL value
    URL_POPUP: A URL value that causes a popup to appear
    NUMBER:    A number value
    BOOLEAN:   A boolean value
    UUID:      A resource UUID value
    """

    FUNCTION = 'FUNCTION'
    DIALOGUE = 'DIALOGUE'
    STRING = 'STRING'
    URL = 'URL'
    URL_POPUP = 'URL_POPUP'
    NUMBER = 'NUMBER'
    BOOLEAN = 'BOOLEAN'
    UUID = 'UUID'


class ResourceType(PrintableEnum):

    """FCO REST API ResourceType enum

    The ResourceType enum enumerates the different types of resource.
    FIREWALL_TEMPLATE:        Fireall template
    BILLING_METHOD:           BillingMethod
    DEPLOYMENT_INSTANCE:      DeploymentInstance
    TRANSACTION:              Transaction
    GROUP:                    Group
    NETWORK:                  Network
    FDL:                      FDLResource
    CURRENCY:                 Currencies used with in jade (not resource
                              can only be used with the listCurrency
                              call)
    VDC:                      VDC
    REFERRAL_PROMOTION:       ReferralPromotion
    DEPLOYMENT_TEMPLATE:      Template
    PRODUCTOFFER:             Product offer
    PROMOTION:                Promotion
    DISK:                     Disk
    CUSTOMER:                 Customer
    PRODUCT_COMP_TYPE:        ProductComponentType
    SSHKEY:                   SSHKey
    PAYMENT_METHOD:           PaymentMethod
    IMAGE:                    Image
    JOB:                      Job
    SNAPSHOT:                 Snapshot of a disk or server
    INVOICE:                  Payment method
    MEASUREMENT:              An instance of a measurement taken from a
                              resource
    PLUGGABLE_RESOURCE:       An instance object created by Pluggable
                              Resource Provider.
    TRANSLATION:              An object that represents a un-compiled
                              translation.
    PAYMENT_METHOD_INSTANCE:  PaymentMethodInstance
    PLUGGABLE_PROVIDER:       An object created by FDL that defines
                              Pluggable Resources.
    REFERRAL_PROMOCODE:       Referral Promocode (not a resource, for
                              use with doQuery but cannot be used with
                              listResources etc)
    BILLING_ENTITY:           Billing Entity
    TRANSACTION_LOG:          Tranction logs created when using payment
                              gateway (not a resource can only be used
                              with the listTransactionLogs call)
    CREDIT_NOTE:              Credit Note
    PERMISSION:               Permission (not a resource, for use with
                              doQuery but cannot be used with
                              listResources etc)
    FIREWALL:                 Firewall
    PRODUCT_PURCHASE:         Product Purchased (not a resource, for use
                              with doQuery but cannot be used with
                              listResources etc)
    TRIGGER_METHOD:           TriggerMethod
    UNIT_TRANSACTION:         Unit Transaction (not a resource, for use
                              with doQuery but cannot be used with
                              listResources etc)
    PURCHASED_UNITS:          Purchased Units (not a resource, for use
                              with doQuery but cannot be used with
                              listResources etc)
    MEASUREMENT_FUNCTION:     This holds an instance of a Measurement
                              Function
    FETCH_RESOURCE:           A fetch parameter instance
    ANY:                      Any resource
    SUBNET:                   Subnet
    PRODUCT:                  Product
    PAYMENT_PROVIDER:         PaymentProvider
    UNIT_TRANSACTION_SUMMARY: Unit Transaction Summary (not a resource,
                              for use with doQuery but cannot be used
                              with listResources etc)
    NIC:                      NIC
    PROMOCODE:                PromoCode (not a resource, for use with
                              doQuery but cannot be used with
                              listResources etc)
    SERVER:                   Server
    CLUSTER:                  Cluster
    IMAGEINSTANCE:            A billable image instance
    BLOB:                     Blob
    CONFIG_PROVIDER:          An object created byFDL that enables
                              additional configuration for other
                              resources.
    STORAGE_GROUP:            This holds StorageGroup
    REPORT_METHOD:            An object created by FDL to generate
                              report and chart data.
    STATEMENT_DETAIL:         This holds an instance of currency
                              statement.
    USER:                     User
    """

    FIREWALL_TEMPLATE = 'FIREWALL_TEMPLATE'
    BILLING_METHOD = 'BILLING_METHOD'
    DEPLOYMENT_INSTANCE = 'DEPLOYMENT_INSTANCE'
    TRANSACTION = 'TRANSACTION'
    GROUP = 'GROUP'
    NETWORK = 'NETWORK'
    FDL = 'FDL'
    CURRENCY = 'CURRENCY'
    VDC = 'VDC'
    REFERRAL_PROMOTION = 'REFERRAL_PROMOTION'
    DEPLOYMENT_TEMPLATE = 'DEPLOYMENT_TEMPLATE'
    PRODUCTOFFER = 'PRODUCTOFFER'
    PROMOTION = 'PROMOTION'
    DISK = 'DISK'
    CUSTOMER = 'CUSTOMER'
    PRODUCT_COMP_TYPE = 'PRODUCT_COMP_TYPE'
    SSHKEY = 'SSHKEY'
    PAYMENT_METHOD = 'PAYMENT_METHOD'
    IMAGE = 'IMAGE'
    JOB = 'JOB'
    SNAPSHOT = 'SNAPSHOT'
    INVOICE = 'INVOICE'
    MEASUREMENT = 'MEASUREMENT'
    PLUGGABLE_RESOURCE = 'PLUGGABLE_RESOURCE'
    TRANSLATION = 'TRANSLATION'
    PAYMENT_METHOD_INSTANCE = 'PAYMENT_METHOD_INSTANCE'
    PLUGGABLE_PROVIDER = 'PLUGGABLE_PROVIDER'
    REFERRAL_PROMOCODE = 'REFERRAL_PROMOCODE'
    BILLING_ENTITY = 'BILLING_ENTITY'
    TRANSACTION_LOG = 'TRANSACTION_LOG'
    CREDIT_NOTE = 'CREDIT_NOTE'
    PERMISSION = 'PERMISSION'
    FIREWALL = 'FIREWALL'
    PRODUCT_PURCHASE = 'PRODUCT_PURCHASE'
    TRIGGER_METHOD = 'TRIGGER_METHOD'
    UNIT_TRANSACTION = 'UNIT_TRANSACTION'
    PURCHASED_UNITS = 'PURCHASED_UNITS'
    MEASUREMENT_FUNCTION = 'MEASUREMENT_FUNCTION'
    FETCH_RESOURCE = 'FETCH_RESOURCE'
    ANY = 'ANY'
    SUBNET = 'SUBNET'
    PRODUCT = 'PRODUCT'
    PAYMENT_PROVIDER = 'PAYMENT_PROVIDER'
    UNIT_TRANSACTION_SUMMARY = 'UNIT_TRANSACTION_SUMMARY'
    NIC = 'NIC'
    PROMOCODE = 'PROMOCODE'
    SERVER = 'SERVER'
    CLUSTER = 'CLUSTER'
    IMAGEINSTANCE = 'IMAGEINSTANCE'
    BLOB = 'BLOB'
    CONFIG_PROVIDER = 'CONFIG_PROVIDER'
    STORAGE_GROUP = 'STORAGE_GROUP'
    REPORT_METHOD = 'REPORT_METHOD'
    STATEMENT_DETAIL = 'STATEMENT_DETAIL'
    USER = 'USER'


class ValidatorType(PrintableEnum):

    """FCO REST API ValidatorType enum

    The ValidatorType enum represents the various types of validator.
    REGEX:          A regular expression
    RESOURCE:       A valid Resource, The Validator String will specifiy
                    which Resource and which filed requires, e.g
                    'CLUSTER.resourceUUID'
    NUMERIC_DOUBLE: A floating point value
    ENUM:           An enum, i.e. a choice of a preset list of options
    BLOB_UPLOAD:    The UUID of an uploaded blob
    BOOLEAN:        A boolean value, either true or false.
    BIG_TEXT:       A text area
    DATE:           A date
    HEX_COLOUR:     A hexadecimal colour expressed as a string i.e.
                    #000000
    PASSWORD:       A password
    NUMERIC_INT:    An integer value
    ICON:           An icon expressed as a base 64 encoded string
    """

    REGEX = 'REGEX'
    RESOURCE = 'RESOURCE'
    NUMERIC_DOUBLE = 'NUMERIC_DOUBLE'
    ENUM = 'ENUM'
    BLOB_UPLOAD = 'BLOB_UPLOAD'
    BOOLEAN = 'BOOLEAN'
    BIG_TEXT = 'BIG_TEXT'
    DATE = 'DATE'
    HEX_COLOUR = 'HEX_COLOUR'
    PASSWORD = 'PASSWORD'
    NUMERIC_INT = 'NUMERIC_INT'
    ICON = 'ICON'


class RedirectMethod(PrintableEnum):

    """FCO REST API RedirectMethod enum

    The type of redirection used by the transaction.
    REDIRECT: The redirect should be processed as a browser redirect
    POST:     The redirect should be processed as a POST request
    GET:      The redirect should be processed as a GET request
    """

    REDIRECT = 'REDIRECT'
    POST = 'POST'
    GET = 'GET'


class ImageType(PrintableEnum):

    """FCO REST API ImageType enum

    The ImageType enum enumerates the different types of image.
    DISK:   A disk image
    SERVER: A server image
    """

    DISK = 'DISK'
    SERVER = 'SERVER'


class TransactionType(PrintableEnum):

    """FCO REST API TransactionType enum

    The TransactionType enum enumerates the available types of
    transaction.
    CREDIT: A credit transaction
    DEBIT:  A debit transaction
    """

    CREDIT = 'CREDIT'
    DEBIT = 'DEBIT'


class GroupType(PrintableEnum):

    """FCO REST API GroupType enum

    The GroupType enum enumerates the different types of groups.
    ADMIN:    The admin group
    EVERYONE: The everyone group
    LOCKED:   The locked group
    NORMAL:   A normal group
    """

    ADMIN = 'ADMIN'
    EVERYONE = 'EVERYONE'
    LOCKED = 'LOCKED'
    NORMAL = 'NORMAL'


class VirtualizationType(PrintableEnum):

    """FCO REST API VirtualizationType enum

    The VirtualizationType enum enumerates the different types of
    virtualization (container or vm).
    CONTAINER:       Linux container
    VIRTUAL_MACHINE: Virtual machine
    """

    CONTAINER = 'CONTAINER'
    VIRTUAL_MACHINE = 'VIRTUAL_MACHINE'


class BillingType(PrintableEnum):

    """FCO REST API BillingType enum

    The BillingType enum describes the type of a BillingEntity.
    REGULARBILL: Regular Billing Entity
    MASTERBILL:  Master Billing Entity
    """

    REGULARBILL = 'REGULARBILL'
    MASTERBILL = 'MASTERBILL'


class MeasureType(PrintableEnum):

    """FCO REST API MeasureType enum

    The MeasureType enum specifies the measurement types for rating.
    KB:            Kilobytes
    B:             Bytes
    STRING:        String value
    HOUR:          Hour
    MB:            Megabytes
    MINUTE:        Minutes
    NUMERIC:       A numeric unitless value
    MONTH:         Month
    CURRENCY:      Currency
    SECOND:        Seconds
    GB:            Gigabytes
    YEAR:          Year
    RESOURCE_UUID: The UUID of a resource
    TB:            Terabytes
    DAY:           Day
    UNIT:          Units
    """

    KB = 'KB'
    B = 'B'
    STRING = 'STRING'
    HOUR = 'HOUR'
    MB = 'MB'
    MINUTE = 'MINUTE'
    NUMERIC = 'NUMERIC'
    MONTH = 'MONTH'
    CURRENCY = 'CURRENCY'
    SECOND = 'SECOND'
    GB = 'GB'
    YEAR = 'YEAR'
    RESOURCE_UUID = 'RESOURCE_UUID'
    TB = 'TB'
    DAY = 'DAY'
    UNIT = 'UNIT'


class MultitierStorage(PrintableEnum):

    """FCO REST API MultitierStorage enum

    The SystemCapability multitier storage enum enumerates the different
    options for using multitier storage in a system.
    FALSE: Multitier storage is not enabled
    TRUE:  Multitier storage is enabled
    """

    FALSE = 'FALSE'
    TRUE = 'TRUE'


class ResourceKeyType(PrintableEnum):

    """FCO REST API ResourceKeyType enum

    The ResourceKeyType enum enumerates the different types of resource
    key.
    PLACEMENT_KEY:      Node Placement Key
    SYSTEM_KEY:         System key
    BILLING_ENTITY_KEY: Billing Key
    ADVERTISE_KEY:      Advertise Key
    USER_KEY:           User key
    """

    PLACEMENT_KEY = 'PLACEMENT_KEY'
    SYSTEM_KEY = 'SYSTEM_KEY'
    BILLING_ENTITY_KEY = 'BILLING_ENTITY_KEY'
    ADVERTISE_KEY = 'ADVERTISE_KEY'
    USER_KEY = 'USER_KEY'


class ICMPParam(PrintableEnum):

    """FCO REST API ICMPParam enum

    The ICMP Param enum enumerates the possible types of ICMP packet
    filtered by a FirewallRule matching ICMP traffic.
    INFORMATION_REPLY:         ICMP information reply
    ROUTER_ADVERTISEMENT_IPv4: ICMP router advertisement
    ROUTER_ADVERTISEMENT_IPv6: ICMPv6 router advertisement
    ADDRESS_MASK_REPLY:        ICMP address mask reply
    INFORMATION_REQUEST:       ICMP information request
    ROUTER_SOLICITATION_IPv4:  ICMP router solicitation
    ROUTER_SOLICITATION_IPv6:  ICMPv6 router solicitation
    TIMESTAMP_REPLY:           ICMP timestamp reply
    PARAMETER_PROBLEM:         ICMP parameter problem
    MULTICAST_LISTENER_DONE:   ICMPv6 multicast listener done
    NEIGHBOR_SOLICITATION:     ICMPv6 neighbor solicitation
    TIME_EXCEEDED:             ICMP time exceeded
    MULTICAST_LISTENER_QUERY:  ICMPv6 multicast listener query
    DESTINATION_UNREACHABLE:   ICMP destination unreachable
    REDIRECT_MESSAGE_IPv6:     ICMPv6 redirect
    NEIGHBOR_ADVERTISEMENT:    ICMPv6 neighbor advertisement
    REDIRECT_MESSAGE_IPv4:     ICMP redirect
    ALTERNATE_HOST_ADDRESS:    ICMP alternate host address
    TIMESTAMP:                 ICMP timestamp
    MULTICAST_LISTENER_REPORT: ICMPv6 multicast listener report
    ECHO_REPLY_IPv6:           ICMPv6 echo reply
    ECHO_REPLY_IPv4:           ICMP echo reply
    ECHO_REQUEST_IPv4:         ICMP echo response
    ADDRESS_MASK_REQUEST:      ICMP address mask request
    ECHO_REQUEST_IPv6:         ICMPv6 echo request
    SOURCE_QUENCH:             ICMP source quench
    """

    INFORMATION_REPLY = 'INFORMATION_REPLY'
    ROUTER_ADVERTISEMENT_IPv4 = 'ROUTER_ADVERTISEMENT_IPv4'
    ROUTER_ADVERTISEMENT_IPv6 = 'ROUTER_ADVERTISEMENT_IPv6'
    ADDRESS_MASK_REPLY = 'ADDRESS_MASK_REPLY'
    INFORMATION_REQUEST = 'INFORMATION_REQUEST'
    ROUTER_SOLICITATION_IPv4 = 'ROUTER_SOLICITATION_IPv4'
    ROUTER_SOLICITATION_IPv6 = 'ROUTER_SOLICITATION_IPv6'
    TIMESTAMP_REPLY = 'TIMESTAMP_REPLY'
    PARAMETER_PROBLEM = 'PARAMETER_PROBLEM'
    MULTICAST_LISTENER_DONE = 'MULTICAST_LISTENER_DONE'
    NEIGHBOR_SOLICITATION = 'NEIGHBOR_SOLICITATION'
    TIME_EXCEEDED = 'TIME_EXCEEDED'
    MULTICAST_LISTENER_QUERY = 'MULTICAST_LISTENER_QUERY'
    DESTINATION_UNREACHABLE = 'DESTINATION_UNREACHABLE'
    REDIRECT_MESSAGE_IPv6 = 'REDIRECT_MESSAGE_IPv6'
    NEIGHBOR_ADVERTISEMENT = 'NEIGHBOR_ADVERTISEMENT'
    REDIRECT_MESSAGE_IPv4 = 'REDIRECT_MESSAGE_IPv4'
    ALTERNATE_HOST_ADDRESS = 'ALTERNATE_HOST_ADDRESS'
    TIMESTAMP = 'TIMESTAMP'
    MULTICAST_LISTENER_REPORT = 'MULTICAST_LISTENER_REPORT'
    ECHO_REPLY_IPv6 = 'ECHO_REPLY_IPv6'
    ECHO_REPLY_IPv4 = 'ECHO_REPLY_IPv4'
    ECHO_REQUEST_IPv4 = 'ECHO_REQUEST_IPv4'
    ADDRESS_MASK_REQUEST = 'ADDRESS_MASK_REQUEST'
    ECHO_REQUEST_IPv6 = 'ECHO_REQUEST_IPv6'
    SOURCE_QUENCH = 'SOURCE_QUENCH'


class Branding(PrintableEnum):

    """FCO REST API Branding enum

    The SystemCapability Branding enum enumerates the different options
    for branding in a system.
    FALSE: Branding is not set
    TRUE:  Branding is set
    """

    FALSE = 'FALSE'
    TRUE = 'TRUE'


class StatementType(PrintableEnum):

    """FCO REST API StatementType enum

    The StatementType enum enumerates the available statement detail
    types.
    UNPAID_CREDITNOTE: This balance line happen when an unpaid credit
                       note is created
    UNPAID_INVOICE:    This balance line happen when UNPAID invoice is
                       created
    PAYMENT_RECEIVED:  This balance line happen when we have received a
                       payment i.e for an unpaid invoice is paid
    PAYMENT_MADE:      This balance line happen when credit note is
                       marked as paid
    """

    UNPAID_CREDITNOTE = 'UNPAID_CREDITNOTE'
    UNPAID_INVOICE = 'UNPAID_INVOICE'
    PAYMENT_RECEIVED = 'PAYMENT_RECEIVED'
    PAYMENT_MADE = 'PAYMENT_MADE'


class InvoiceHeader(PrintableEnum):

    """FCO REST API InvoiceHeader enum

    Values which represent the headers on an invoice which can be
    edited.
    CUSTOMER_TAX_REF:   The value to use in place of the term customer
                        tax reference.
    INCLUDE:            The value to use in place of the term include.
    CREDIT_NOTE_NUMBER: The value to use in place of the term credit
                        note number.
    INVOICE_DATE:       The value to use in place of the term issue
                        date.
    BE_TAX_REF:         The value to use in place of the term BE tax
                        reference.
    ITEM:               The value to use in place of the term item.
    AMOUNT:             The value to use in place of the term amount.
    CREDITNOTE:         The value to use in place of the term credit
                        note.
    INVOICE:            The value to use in place of the term invoice.
    EXCLUDE:            The value to use in place of the term exclude.
    INVOICE_NUMBER:     The value to use in place of the term invoice
                        number.
    TOTAL:              The value to use in place of the term total.
    DUEDATE:            The value to use in place of the term due date.
    QUANTITY:           The value to use in place of the term quantity.
    """

    CUSTOMER_TAX_REF = 'CUSTOMER_TAX_REF'
    INCLUDE = 'INCLUDE'
    CREDIT_NOTE_NUMBER = 'CREDIT_NOTE_NUMBER'
    INVOICE_DATE = 'INVOICE_DATE'
    BE_TAX_REF = 'BE_TAX_REF'
    ITEM = 'ITEM'
    AMOUNT = 'AMOUNT'
    CREDITNOTE = 'CREDITNOTE'
    INVOICE = 'INVOICE'
    EXCLUDE = 'EXCLUDE'
    INVOICE_NUMBER = 'INVOICE_NUMBER'
    TOTAL = 'TOTAL'
    DUEDATE = 'DUEDATE'
    QUANTITY = 'QUANTITY'


class PdfPageSize(PrintableEnum):

    """FCO REST API PdfPageSize enum

    An enum that represents a size of a PDF page.
    A4:     A4 Page Size
    LETTER: Letter Page Size
    """

    A4 = 'A4'
    LETTER = 'LETTER'


class StorageCapability(PrintableEnum):

    """FCO REST API StorageCapability enum

    The StorageCapability enum represents the capability of a storage
    unit.
    CHILDREN_PERSIST_ON_DELETE: The child objects of a disk on a storage
                                unit persist on deletion of that disk
    CLONE:                      Storage unit is natively capable of
                                cloning
    CHILDREN_PERSIST_ON_REVERT: The child objects of a disk on a storage
                                unit persist on reversion to an earlier
                                snapshot
    SNAPSHOT:                   Storage unit is natively capable of
                                snapshotting
    """

    CHILDREN_PERSIST_ON_DELETE = 'CHILDREN_PERSIST_ON_DELETE'
    CLONE = 'CLONE'
    CHILDREN_PERSIST_ON_REVERT = 'CHILDREN_PERSIST_ON_REVERT'
    SNAPSHOT = 'SNAPSHOT'


class PaymentType(PrintableEnum):

    """FCO REST API PaymentType enum

    The PaymentType enum enumerates the different types of payment (pre-
    pay or post-pay).
    PREPAY:  Prepay
    INVOICE: Invoice / postpay
    """

    PREPAY = 'PREPAY'
    INVOICE = 'INVOICE'


class ServerStatus(PrintableEnum):

    """FCO REST API ServerStatus enum

    The ServerStatus enum enumerates the different server statuses.
    BUILDING:   Building
    RECOVERY:   Undergoing live recovery
    DELETING:   Deleting
    REBOOTING:  Rebooting
    INSTALLING: Installing
    RUNNING:    Running
    STOPPED:    Stopped
    ERROR:      Internal error state
    STOPPING:   Stopping
    MIGRATING:  Migrating
    STARTING:   Starting
    """

    BUILDING = 'BUILDING'
    RECOVERY = 'RECOVERY'
    DELETING = 'DELETING'
    REBOOTING = 'REBOOTING'
    INSTALLING = 'INSTALLING'
    RUNNING = 'RUNNING'
    STOPPED = 'STOPPED'
    ERROR = 'ERROR'
    STOPPING = 'STOPPING'
    MIGRATING = 'MIGRATING'
    STARTING = 'STARTING'


class Snapshotting(PrintableEnum):

    """FCO REST API Snapshotting enum

    The SystemCapability Snapshotting enum enumerates the different
    snapshotting capabilities of a system or cluster.
    DISK:   Disk snapshotting is permitted
    SERVER: Server snapshotting is permitted
    """

    DISK = 'DISK'
    SERVER = 'SERVER'


class Cloning(PrintableEnum):

    """FCO REST API Cloning enum

    The SystemCapability Cloning enum enumerates the different cloning
    capabilities of a system or cluster.
    DISK:   Disk cloning is permitted
    SERVER: Server cloning is permitted
    """

    DISK = 'DISK'
    SERVER = 'SERVER'


class TriggerType(PrintableEnum):

    """FCO REST API TriggerType enum

    The TriggerType enum described the type of the trigger being
    executed.
    PRE_USER_API_CALL:          Trigger which is called before a User
                                API call.
    POST_JOB_STATE_CHANGE:      Trigger which is called after a state
                                change on a job.
    PRE_SERVER_STATE_CHANGE:    Trigger which is called before a state
                                change on a server.
    PRE_MODIFY:                 Trigger which is called before a
                                resource has been modified.
    PRE_SERVER_METADATA_UPDATE: Trigger which is called before the
                                server metadata is set.
    POST_CREATE:                Trigger which is called after the
                                creation of a resource.
    PRE_CREATE:                 Trigger which is called before the
                                creation of a resource.
    POST_PURCHASE:              Trigger which is called after a purchase
                                has been made.
    POST_USER_API_CALL:         Trigger which is called after a User API
                                call.
    PRE_AUTH:                   Trigger which is called before a user is
                                authenticated.
    POST_PAYMENT:               Trigger which is called after a payment
                                or refund is attempted.
    POST_EXCEPTION:             Trigger which is called after an
                                exception is thrown.
    PRE_PURCHASE:               Trigger which is called before a
                                purchase has been made.
    PRE_PAYMENT:                Trigger which is called before a payment
                                or refund is attempted.
    POST_COLLECTION:            Trigger which is called after the VPS
                                billing collection loop.
    POST_DELETE:                Trigger which is called after the
                                deletion of a resource.
    PRE_DELETE:                 Trigger which is called before the
                                deletion of a resource.
    TAX_CALCULATION:            Trigger which is called before tax is
                                calculated for an invoice in order to
                                perform the calculation instead of the
                                default system
    POST_SERVER_STATE_CHANGE:   Trigger which is called after a state
                                change on a server.
    PRE_ADMIN_API_CALL:         Trigger which is called before an Admin
                                API call.
    PRE_JOB_STATE_CHANGE:       Trigger which is called before a state
                                change on a job.
    SCHEDULED:                  Trigger which will be called based on a
                                schedule
    POST_UNIT_TRANSACTION:      Trigger which is called after a unit
                                transaction.
    POST_BILLING:               Trigger which is called after the
                                billing loop has completed.
    POST_ADMIN_API_CALL:        Trigger which is called after an Admin
                                API call.
    POST_AUTH:                  Trigger which is called after a user is
                                authenticated.
    POST_MODIFY:                Trigger which is called after a resource
                                has been modified.
    """

    PRE_USER_API_CALL = 'PRE_USER_API_CALL'
    POST_JOB_STATE_CHANGE = 'POST_JOB_STATE_CHANGE'
    PRE_SERVER_STATE_CHANGE = 'PRE_SERVER_STATE_CHANGE'
    PRE_MODIFY = 'PRE_MODIFY'
    PRE_SERVER_METADATA_UPDATE = 'PRE_SERVER_METADATA_UPDATE'
    POST_CREATE = 'POST_CREATE'
    PRE_CREATE = 'PRE_CREATE'
    POST_PURCHASE = 'POST_PURCHASE'
    POST_USER_API_CALL = 'POST_USER_API_CALL'
    PRE_AUTH = 'PRE_AUTH'
    POST_PAYMENT = 'POST_PAYMENT'
    POST_EXCEPTION = 'POST_EXCEPTION'
    PRE_PURCHASE = 'PRE_PURCHASE'
    PRE_PAYMENT = 'PRE_PAYMENT'
    POST_COLLECTION = 'POST_COLLECTION'
    POST_DELETE = 'POST_DELETE'
    PRE_DELETE = 'PRE_DELETE'
    TAX_CALCULATION = 'TAX_CALCULATION'
    POST_SERVER_STATE_CHANGE = 'POST_SERVER_STATE_CHANGE'
    PRE_ADMIN_API_CALL = 'PRE_ADMIN_API_CALL'
    PRE_JOB_STATE_CHANGE = 'PRE_JOB_STATE_CHANGE'
    SCHEDULED = 'SCHEDULED'
    POST_UNIT_TRANSACTION = 'POST_UNIT_TRANSACTION'
    POST_BILLING = 'POST_BILLING'
    POST_ADMIN_API_CALL = 'POST_ADMIN_API_CALL'
    POST_AUTH = 'POST_AUTH'
    POST_MODIFY = 'POST_MODIFY'


class SnapshotType(PrintableEnum):

    """FCO REST API SnapshotType enum

    The SnapshotType enum enumerates the available snapshot types.
    DISK:   Disk snapshot
    SERVER: Server snapshot
    """

    DISK = 'DISK'
    SERVER = 'SERVER'


class Payment(PrintableEnum):

    """FCO REST API Payment enum

    The SystemCapability Payment enum enumerates the different payment
    capabilities of a system.
    DEBIT_CARD:  Debit card payment is permitted
    INVOICE:     Invoice payment is permitted
    CREDIT_CARD: Credit card payment is permitted
    """

    DEBIT_CARD = 'DEBIT_CARD'
    INVOICE = 'INVOICE'
    CREDIT_CARD = 'CREDIT_CARD'


class VNCHandler(PrintableEnum):

    """FCO REST API VNCHandler enum

    The VNCHandler enum enumerates the type of VNC handler requested.
    RAW:       Raw protocol (i.e. RFB)
    ANY:       Any protocol the cluster will support
    GUACAMOLE: Guacamole protocol
    """

    RAW = 'RAW'
    ANY = 'ANY'
    GUACAMOLE = 'GUACAMOLE'


class DiskStatus(PrintableEnum):

    """FCO REST API DiskStatus enum

    The DiskStatus enum represents the attachment state of a disk.
    CANNOT_BE_ATTACHED_TO_SERVER: Cannot be attached to a server (for
                                  instance during creation or deletion)
    NOT_ATTACHED_TO_SERVER:       Not attached to a server
    ATTACHED_TO_SERVER:           Attached to a server
    """

    CANNOT_BE_ATTACHED_TO_SERVER = 'CANNOT_BE_ATTACHED_TO_SERVER'
    NOT_ATTACHED_TO_SERVER = 'NOT_ATTACHED_TO_SERVER'
    ATTACHED_TO_SERVER = 'ATTACHED_TO_SERVER'


class TransactionState(PrintableEnum):

    """FCO REST API TransactionState enum

    The TransactionState enum enumerates the possible states of a
    Transaction.
    SUCCESS:                  Success
    NOT_STARTED:              Waiting
    FAILURE:                  Failure
    CANCELLED:                Cancelled
    INPROGRESS:               In progress
    AWAITINGINTERACTIVEINPUT: Awaiting interactive input
    """

    SUCCESS = 'SUCCESS'
    NOT_STARTED = 'NOT_STARTED'
    FAILURE = 'FAILURE'
    CANCELLED = 'CANCELLED'
    INPROGRESS = 'INPROGRESS'
    AWAITINGINTERACTIVEINPUT = 'AWAITINGINTERACTIVEINPUT'
