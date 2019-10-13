import base64
import json
from string import lower
import pld_module


def json_replacer(_josn, inject_point, payload):
    data = json.loads(_josn)
    data[inject_point] = payload
    return json.dumps(data)


def encodeToBase64(str):
    return base64.b64encode(str)


class Header_Fuzz(object):
    def __init__(self, header, inject_point):
        self.header = header
        self.inject_point = inject_point

    def mutation(self, mut_type="string"):
        """
        :param mut_type: Mutation type
        :type  mut_type: String
        :return:
        """
        self.mut_type = lower(mut_type)

    def get_payloads(self):
        if self.mut_type == "string":
            with open("payload") as f:
                return f.readlines()
        if self.mut_type == "int":
            # TODO
            a = 1

    def build_mutation_header_parameter(self):
        mutated_payloads = []
        payloads = self.get_payloads()
        for payload in payloads:
            payload = payload.strip()
            s = json_replacer(self.header, self.inject_point, payload.replace("\"", "\\\""))
            mutated_payloads.append(encodeToBase64(s))
        return mutated_payloads


class Body_Fuzz(object):
    def __init__(self, body, inject_point):
        self.body = body
        self.inject_point = inject_point

    def mutation(self, mut_type="string"):
        self.mut_type = lower(mut_type)

    def get_payloads(self):
        if self.mut_type == "string":
            with open("payload") as f:
                return f.readlines()
        if self.mut_type == "int":
            # TODO
            a = 1

    def build_mutation_body_parameter(self):
        mutated_payloads = []
        payloads = self.get_payloads()
        for payload in payloads:
            payload = payload.strip()
            s = json_replacer(self.body, self.inject_point, payload.replace("\"", "\\\""))
            mutated_payloads.append(encodeToBase64(s))
        return mutated_payloads

