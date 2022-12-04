import requests
import json
import os

def getLoggedInUsers(host, port):
    sessionId = createSessionId(host, port)
    url = f"http://{host}:{port}/spdrm/webresources/GetLoggedInUsers/getLoggedInUsersAsString"
    res = requests.get(url, headers = {'authorization': sessionId} )
    killSessionId(host, port, sessionId)
    return 0

def kickAllUsers(host, port):
    sessionId = createSessionId(host, port)
    url = f"http://{host}:{port}/spdrm/webresources/CloseAllUserSessions"
    res = requests.get(url, headers = {'authorization': sessionId} )
    killSessionId(host, port, sessionId)
    return 0

def getVersion(host, port):
    sessionId = createSessionId(host, port)
    url = f"http://{host}:{port}/spdrm/webresources/api/server/spdrm/version"
    res = requests.get(url, headers = {'authorization': sessionId} )
    killSessionId(host, port, sessionId)
    return res.json()

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

def getAllVersions():
    upload_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")
    with open(upload_folder, 'r') as f:
        data = json.load(f)
        f.close()

    versions = []
    
    for obj in data:
        if 'Version' in obj.keys():
            if len(versions) == 0:
                versions.append([{
                    'Branch' : obj['Version'][2],
                    'Version': obj['Version']
                }])
            else:
                stored = False
                for branch in versions:
                    if branch[0]['Branch'] == obj['Version'][2]:
                        for i in range(len(branch)):
                            if branch[i]['Version'][-1] == obj['Version'][-1]:
                                stored = True
                                break
                            elif int(branch[i]['Version'][-1]) > int(obj['Version'][-1]):
                                branch.insert(i,{
                                    'Branch' : obj['Version'][2],
                                    'Version': obj['Version']
                                })
                                stored = True
                                break
                        if stored == False:
                            branch.append({
                                'Branch' : obj['Version'][2],
                                'Version': obj['Version']    
                            })
                            stored = True
                if stored == False:
                    for i in range(len(versions)):
                        if int(versions[i][0]['Branch']) > int(obj['Version'][2]):
                            versions.insert(i,[{
                                'Branch' : obj['Version'][2],
                                'Version': obj['Version']                                
                            }])
                            stored = True
                            break
                    if stored == False:                       
                        versions.append([{
                            'Branch' : obj['Version'][2],
                            'Version': obj['Version']
                        }])

    versions_final = []
    for branch in versions:
        for item in branch:
            versions_final.append(item['Version'])

    return versions_final

def getOneVersion(version):
    upload_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")
    with open(upload_folder, 'r') as f:
        data = json.load(f)
        f.close()
    keepers = []
    for obj in data:
        if version == obj['Version']:
            keepers.append(obj)
    
    print(keepers)
    return 0;

getOneVersion('1.7.1')