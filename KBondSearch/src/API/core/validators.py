import json
import xmltodict

import xml.etree.ElementTree as elementTree

def is_json(resp, *args, **kwargs):
    try:
        json.loads(resp.content)
        return True
    except:
        print(resp.content)
        print("is resp content is not json")
        return False
    return True




def is_xml(resp, *args, **kwargs):
    #https://lindevs.com/code-snippets/check-if-string-is-valid-xml-using-python
    try:
        elementTree.fromstring(resp.content)
        return True
    except elementTree.ParseError:
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



def isolate_params(
    needed_kwargs: list,
    kwargs : dict,
):
    isolated = dict()
    for key, value in list(kwargs.items()):
        if key in needed_kwargs:
            isolated[key] = kwargs.pop(key)
    
    return isolated