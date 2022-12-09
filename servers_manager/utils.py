import requests
import json
import os

def getLoggedInUsers(host, port):
    # sessionId = createSessionId(host, port)
    # url = f"http://{host}:{port}/spdrm/webresources/GetLoggedInUsers/getLoggedInUsersAsString"
    # res = requests.get(url, headers = {'authorization': sessionId} )
    # killSessionId(host, port, sessionId)
    # return res.json()
    # stringData = res.json()
    stringData =  ['[8b45e873-ce1e-4d64-b3a2-497abfece6b7, f.bouraimis, 127.0.0.1, WS, 09/12/2022 17:06:38, Administrators]', 
                    '[c24fe059-c9d3-4bf6-ad57-ab5c82ba8f39, admin, support117, SPDRM_CLIENT, 09/12/2022 17:05:43, Administrators]', 
                    '[ef56fe49-271f-462e-959f-0d51b3bfdbee, admin, 127.0.0.1, WS, 09/12/2022 17:07:32, Administrators]', 
                    '[f4a8cf30-8658-4423-9d64-0b3ef7146529, admin, 127.0.0.1, WS, 09/12/2022 17:03:36, Administrators]']
    data = []

    for item in stringData:
        data.append({
            "user": item.split(",")[1].strip(),
            "host": item.split(",")[2].strip(),
            "interface": item.split(",")[3].strip(),
            "date": item.split(",")[4].strip(),
            "group": item.split(",")[5].strip()[:-1],
        })
    return data

    


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
    upload_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")
    with open(upload_folder, 'r') as f:
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