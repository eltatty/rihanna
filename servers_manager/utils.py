import requests
import json

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