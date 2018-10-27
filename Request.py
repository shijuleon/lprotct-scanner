import requests

#rescan: 0
#scan: 1
#report: 2
API_URLS = ['https://www.virustotal.com/vtapi/v2/file/rescan', 'https://www.virustotal.com/vtapi/v2/file/scan', 'https://www.virustotal.com/vtapi/v2/file/report']

def requestJSON(req_type, params):
    try:
        if req_type == 0:
            response = requests.post(API_URLS[req_type], params=params['params'])
            print "Status: %s" % response.status_code
            return response.json()
        elif req_type == 1:
            response = requests.post(API_URLS[req_type], files=params['files'], params=params['params'])
            print "Status: %s" % response.status_code
            if response.status_code == 204:
                print "Error: Tries exceeded"
            return response.json()
        elif req_type == 2:
            response = requests.post(API_URLS[req_type], params=params['params'])  
            return response.json()
    except requests.exceptions.RequestException as e:
        print "Error: Requesting connection"
        print e
