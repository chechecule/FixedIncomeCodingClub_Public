import json
import xmltodict

import xml.etree.ElementTree as elementTree



def is_xml(resp, *args, **kwargs):
    #https://lindevs.com/code-snippets/check-if-string-is-valid-xml-using-python
    try:
        elementTree.fromstring(resp.content)
        return True
    except elementTree.ParseError::
        print(resp.content)
        print("is resp content is not xml")
        return False
    return True

def response_is_200(resp, *args, **kwargs):
    try:
        if resp.status_code == 200 or resp.status_code == "200":
            return True
        else:
            print(resp)
            print("response status code is not 200")
            return False
    except:
        return False
    return False