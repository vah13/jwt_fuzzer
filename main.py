import argparse
import base64, jwt
import json

import fuzz_module, request_sender

header = body = signature = ""


def sign_message(_header, _body, secret=''):
    _body = json.loads(_body)
    _header = json.loads((_header))

    encoded = jwt.encode(_body, secret, algorithm='HS256', headers=_header)
    return encoded


def fix_b64(__str):
    __str += "=" * ((4 - len(__str) % 4) % 4)
    return __str


# init global variables
def parse_jwt(jwt):
    global header, body, signature
    header, body, signature = jwt.split('.')
    header = base64.b64decode(fix_b64(header))
    body = base64.b64decode(fix_b64(body))


"""
function for jwt token printing
"""


def print_jwt(_header, _body, _signature):
    print "JWT Header: {0} JWT Body: {1} JWT Signature {2}".format(_header, _body, _signature)


def start_fuzz(args, _header, _body, _signature):
    global _is_header_or_body, __data
    header = _header
    body = _body
    signature = _signature
    # get inject point
    # need to add the situation when --inject_point is 'body,user|header,kid'
    _inject_argument = args.inject_point
    for _inject_point in _inject_argument.split('|'):

        if _inject_point.split(',')[0] == 'header':
            __data = header
            _is_header_or_body = 'header'
        if _inject_point.split(',')[0] == 'body':
            __data = body
            _is_header_or_body = 'body'
        _inject_param = _inject_point.split(',')[1]

        BF = fuzz_module._Fuzz(__data, _inject_param)  # inject point
        BF.mutation("string")  # payload type
        mutated_data = BF.build_mutation_parameter(_is_header_or_body)  # build json to inject in jwt

        for m_data in mutated_data:
            m_data = m_data.strip()

            if _is_header_or_body == 'body':
                if args.sign == 0:
                    _jwt = (base64.b64encode(header) + "." + (m_data) + "." + signature).replace("=",
                                                                                                 "")  # keep original signature
                else:
                    _jwt = sign_message(header, base64.b64decode(m_data), args.secret)  # sign message

                print_jwt(header, base64.b64decode(m_data), _jwt.split(".")[2])

            if _is_header_or_body == 'header':
                if args.sign == 0:
                    _jwt = (m_data + "." + base64.b64encode(body) + "." + signature).replace("=",
                                                                                             "")  # keep original signature
                else:
                    _jwt = sign_message(base64.b64decode(m_data), body, args.secret)  # sign message

                print_jwt(base64.b64decode(m_data), body, _jwt.split(".")[2])

            request_sender.send_req(_jwt)  # send request


parser = argparse.ArgumentParser(description='Type start arguments')
parser.add_argument('--jwt', type=str, help='JWT Token')
parser.add_argument('--pp', type=str, help='Parse and Print')
parser.add_argument('--sign', type=str, help='Keep original signature or nor')
parser.add_argument('--secret', type=str, help='Define encryption key, buy default the key is "" ')
parser.add_argument('--inject_point', type=str, help='Example: --inject_point header,kid or --inject_point body,user')
args = parser.parse_args()

parse_jwt(args.jwt)

if args.secret == None:
    args.secret = ""

if args.sign == None:
    args.sign = 0
else:
    args.sign = 1

if int(args.pp) == 1:
    print "init jwt", print_jwt(header, body, signature)
    start_fuzz(args, header, body, signature)
