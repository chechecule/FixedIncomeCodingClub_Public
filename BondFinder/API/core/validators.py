import json

def is_json(resp, *args, **kwargs):
    try:
        json.loads(resp.content)
        return True
    except:
        print(resp.content)
        print("is resp content is not json")
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