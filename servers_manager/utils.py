import requests
from requests.auth import HTTPDigestAuth
from threading import Thread
import json
import os

def getLoggedInUsers(host, port):
    sessionId = createSessionId(host, port)
    url = f"http://{host}:{port}/spdrm/webresources/GetLoggedInUsers/getLoggedInUsersAsString"
    res = requests.get(url, headers = {'authorization': sessionId} )
    killSessionId(host, port, sessionId)
    return res.json()

def kickAllUsers(host, port):
    sessionId = createSessionId(host, port)
    url = f"http://{host}:{port}/spdrm/webresources/CloseAllUserSessions"
    res = requests.get(url, headers = {'authorization': sessionId} )
    killSessionId(host, port, sessionId)
    # 200 on success
    return 0

def getBuildInfo(host, port):
    # sessionId = createSessionId(host, port)
    # url = f"http://{host}:{port}/spdrm/webresources/api/server/spdrm/version"
    # res = requests.get(url, headers = {'authorization': sessionId} )
    # killSessionId(host, port, sessionId)
    # return res.json()
    return {
        "version": "1.6.0",
        "built_date": "24/11/2022 20:09:17 EST",
        "process_enabled": True,
        "dm_enabled": True,
        "kb_enabled": True
    }

def killSessionId(host, port, sessionId):
    url = f"http://{host}:{port}/spdrm/webresources/api/auth/logout"
    res = requests.post(url, headers = {'authorization': sessionId} )
    return 0

def createSessionId(host, port):
    
    url = f"http://{host}:{port}/spdrm/webresources/api/auth/roleLogin"

    data = {
        'username': 'admin',
        'password': 'admin',
        'loginType': 'SPDRM'
    }
    
    res = requests.post(url, json = data, headers = {'Content-type': 'application/json'})

    return res.json()['sessionId']

def rankByVersion():
    upload_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")
    with open(upload_file, 'r') as f:
        data = json.load(f)
        f.close()
    
    for server in data:
        if server['Hostname'] != None and server['Ws Port'] != None:
            # build_info = getBuildInfo(server['Hostname'], server['Ws Port'])
            build_info = {'version': '1.8.1_RC1', 'built_date': '24/11/2022 16:48:24 EET', 'ansa_multi_output_enabled': True, 'process_enabled': False, 'dm_enabled': True, 
                        'simModel_contents_based_spinup': False, 'adaptation_key_calculation_method': 'v1', 'intermodular_connectivity_links': False, 'exportActivated': False, 
                        'kb_enabled': False, 'serverProperties': {'version': '1.8.1_RC1', 'compilationDate': 'Nov 24, 2022 4:48:24 PM', 'compilationTimeStamp': '20221124144824', 
                        'systemInfo': 'Linux version 5.10.102.1-microsoft-standard-WSL2 running on amd64; UTF-8; en_null', 'javaInfo': '1.8.0_311; Java HotSpot(TM) 64-Bit Server VM 25.311-b11', 
                        'domainInfo': 'Wildfly 14.0.1', 'changeSet': 'c27d3775eaa2'}}
            # server['version'] = build_info['version']
            server['built_date'] = build_info['built_date']
            server['process_enabled'] = build_info['process_enabled']
            server['dm_enabled'] = build_info['dm_enabled']
            server['kb_enabled'] = build_info['kb_enabled']
    
    versions = set(item['Version'] for item in data)

    group_list = [[item for item in data if item['Version'] == version] for version in versions]

    sorted_list = sorted(group_list, key=lambda x: x[0]['Version'], reverse=True)

    return sorted_list;

def deployTaxis(host, port):
    try:
        upload_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Taxis.ear")
        toUpload = open(upload_file, "rb")
    except FileNotFoundError:
        return -1, 'FileNotFound'

    # Make sure the port is the that of the management console not of SPDRM

    url = f"http://{host}:{port}/management"
    headers = {"content-Type": "application/json"}
    
    try:
        # Undeploy
        print("[+][+][+] Undeploy ")
        data = '{"operation":"undeploy", "address":[{"deployment":"Taxis.ear"}]}'
        res = requests.post(url, auth=HTTPDigestAuth('admin', 'adminadmin'), headers = headers, data = data)
        
        # Remove
        print("[+][+][+] Remove ")
        data = '{"operation":"remove", "address":[{"deployment":"Taxis.ear"}]}'
        res = requests.post(url, auth=HTTPDigestAuth('admin', 'adminadmin'), headers = headers, data = data)

        # Upload
        print("[+][+][+] Upload ")
        res = requests.post(url+'/add-content', auth=HTTPDigestAuth('admin', 'adminadmin'), files={"file": toUpload})
        bytes_value = res.json()['result']['BYTES_VALUE']

        # Deploy
        print("[+][+][+] Deploy ")
        if bytes_value != None:
            data = '{"content":[{"hash": {"BYTES_VALUE" : "' + bytes_value + '"}}], "address": [{"deployment":"Taxis.ear"}], "operation":"add", "enabled":"true"}'
            res = requests.post(url, auth=HTTPDigestAuth('admin', 'adminadmin'), headers = headers, data = data)
            returnValue = res.json()['outcome']
    except:
        return -1, 'Unreachable'

    if toUpload != None:
        toUpload.close()

    return returnValue