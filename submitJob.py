#!/usr/bin/python3
import requests
import json

url = "http://localhost:5000/jobDebug/"

#test_file = open("job.sh", "rb")

#test_response = requests.post(url, files = {"file": test_file})
test_response = requests.get(url)

if test_response.ok:
    print("Upload completed successfully!")
    print(test_response.json()['Debug'])
else:
    print("Something went wrong!")
