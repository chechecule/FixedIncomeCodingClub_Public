# validators.py
import json
import xml.etree.ElementTree as ET



def open_dart_base_status_code_validator(r, content_type, target_code, complain=False):
    """
    Base status code validating function for the opendart api
    """

    if content_type == "json":
        try:
            result_code = str(json.loads(r.content)["status"])
            if result_code == target_code:
                return True
            else:
                return False
        except:
            return False

    elif content_type == "xml":
        try:
            
            result_code = ET.XML(r.content).find("status").text
            if result_code == target_code: 
                return True
            else:
                print(ET.XML(r.content))
                return False
        except:
            return False

def success_code_in_header(resp, content_type):
    """
    Check if header status contains "000" <- success
    """
    return open_dart_base_status_code_validator(resp, content_type, "000", complain=True)

def api_limit_reached(resp, content_type):
    """
    Check if header status contains "020" <- api limit reached
    """
    return open_dart_base_status_code_validator(resp, content_type, "020")