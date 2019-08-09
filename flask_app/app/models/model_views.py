from flask_admin.contrib.sqla import ModelView
from wtforms.validators import DataRequired
from wtforms.fields import (
    TextField,
    PasswordField,
    DateTimeField
)

OPERATIONS_LIST = [
    ('=', '='),
    (':=', ':='),
    ('==', '=='),
    ('+=', '+='),
    ('!=', '!='),
    ('>', '>'),
    ('>=', '>='),
    ('<', '<'),
    ('<=', '<='),
    ('=~', '=~'),
    ('!~', '!~'),
    ('=*', '=*'),
    ('!*', '!*')
]

class RadAcctModelView(ModelView):
    form_overrides = {
        'acctsessionid': TextField,
        'acctuniqueid': TextField,
        'username': TextField,
        'realm': TextField,
        'nasportid': TextField,
        'nasporttype': TextField,
        'acctauthentic': TextField,
        'connectinfo_start': TextField,
        'connectinfo_stop': TextField,
        'calledstationid': TextField,
        'callingstationid': TextField,
        'acctterminatecause': TextField,
        'servicetype': TextField,
        'framedprotocol': TextField,
        'framedinterfaceid': TextField
    }

    form_args = {
        'acctsessionid': {
            'label': 'Session Id'
        },
        'acctuniqueid': {
            'label': 'Unique Id'
        },
        'nasipaddress': {
            'label': 'NAS IP Address'
        },
        'nasportid': {
            'label': 'NAS Port Id'
        },
        'nasporttype': {
            'label': 'NAS Port Type'
        },
        'acctstarttime': {
            'label': 'Start Time'
        },
        'acctupdatetime': {
            'label': 'Update Time'
        },
        'acctstoptime': {
            'label': 'Stop Time'
        },
        'acctinterval': {
            'label': 'Interval'
        },
        'acctsessiontime': {
            'label': 'Session Time'
        },
        'acctauthentic': {
            'label': 'Authentication'
        },
        'connectinfo_start': {
            'label': 'Connection Start'
        },
        'connectinfo_stop': {
            'label': 'Connection Stop'
        },
        'acctinputoctets': {
            'label': 'Input Octets'
        },
        'acctoutputoctets': {
            'label': 'Output Octets'
        },
        'calledstationid': {
            'label': 'Called Station Id'
        },
        'callingstationid': {
            'label': 'Calling Station Id'
        },
        'acctterminatecause': {
            'label': 'Terminate Cause'
        },
        'servicetype': {
            'label': 'Service Type'
        },
        'framedprotocol': {
            'label': 'Framed Protocol'
        },
        'framedipaddress': {
            'label': 'Framed IP Address'
        },
        'framedipv6addr': {
            'label': 'Framed IPv6 Address'
        },
        'framedipv6prefix': {
            'label': 'Framed IPv6 Prefix'
        },
        'framedinterfaceid': {
            'label': 'Framed Interface Id'
        },
        'delegatedipv6prefix': {
            'label': 'Delegated IPv6 Prefix'
        }
    }

class RadCheckReplyModelView(ModelView):
    form_overrides = {
        'username': TextField,
        'value': TextField
    }

    form_choices = {
        'op': OPERATIONS_LIST
    }

    form_args = {
        'username': {
            'validators': [DataRequired()]
        },
        'attribute': {
            'validators': [DataRequired()]
        },
        'op': {
            'label': 'Operation',
            'validators': [DataRequired()]
        }
    }

class RadGroupCheckReplyModelView(ModelView):
    form_overrides = {
        'groupname': TextField,
        'value': TextField
    }

    form_choices = {
        'op': OPERATIONS_LIST
    }

    form_args = {
        'groupname': {
            'validators': [DataRequired()]
        },
        'attribute': {
            'validators': [DataRequired()]
        },
        'op': {
            'label': 'Operation',
            'validators': [DataRequired()]
        }
    }

class RadGroupModelView(ModelView):
    form_overrides = {
        'username': TextField,
        'groupname': TextField,
        'priority': TextField
    }

    form_args = {
        'username': {
            'validators': [DataRequired()]
        },
        'groupname': {
            'validators': [DataRequired()]
        },
        'priority': {
            'validators': [DataRequired()]
        }
    }

class RadPostAuthModelView(ModelView):
    form_overrides = {
        'username': TextField,
        'pass': PasswordField,
        'reply': TextField,
        'calledstationid': TextField,
        'callingstationid': TextField,
        'authdate': DateTimeField
    }

    form_args = {
        'username': {
            'validators': [DataRequired()]
        },
        'pass': {
            'label': 'Password',
            'validators': [DataRequired()]
        },
        'reply': {
            'validators': [DataRequired()]
        },
        'calledstationid': {
            'label': 'Called Station Id',
            'validators': [DataRequired()]
        },
        'callingstationid': {
            'label': 'Calling Station Id',
            'validators': [DataRequired()]
        },
        'authdate': {
            'label': 'Auth Date',
            'validators': [DataRequired()]
        }
    }

class NasModelView(ModelView):
    form_overrides = {
        'nasname': TextField,
        'shortname': TextField,
        'type': TextField,
        'ports': TextField,
        'secret': TextField,
        'server': TextField,
        'community': TextField,
        'description': TextField
    }

    form_args = {
        'nasname': {
            'label': 'NAS Name'
        },
        'shortname': {
            'label': 'Short Name'
        }
    }