import subprocess
import re
import json
import os

def submitJob(jobFile):
    upload_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "jobsDir")
    result = subprocess.run(['sbatch', f"{upload_folder}/{jobFile}"], text=True, capture_output=True)
    objectsDict = {}
    if result.stderr:
        err_line = result.stderr.split('\n')[0]
        err = re.split(':', err_line)
        if len(err[0]) > 0:
            objectsDict[err[0]] = err[1]
    else:
        objectsDict['JobID'] = result.stdout.split()[-1]
        
    return json.loads(json.dumps(objectsDict))

def getJobs():
    result = subprocess.run(['squeue', '-h'],text=True, capture_output=True)
    objectsDict = {}
    if result.stderr:
        err_line = result.stderr.split('\n')[0]
        err = re.split(':', err_line)
        if len(err[0]) > 0:
            objectsDict[err[0]] = err[1]
    else:
        job_lines = result.stdout.strip().split('\n')
        objectsDict['jobs'] = []
        for job_line in job_lines:
            if job_line.strip() != '':
                objectsDict['jobs'].append(getInfo(job_line.split()[0]))
    return json.loads(json.dumps(objectsDict))


def getInfo(jobId):
    result = subprocess.run(['scontrol', 'show', 'job', str(jobId)], text=True, capture_output=True,)
    objectsDict = {}
   
    if result.stderr:
        err = re.split(':', result.stderr)
        if len(err[0]) > 0:
                    objectsDict[err[0]] = err[1].lstrip()
    else:
        resultLines = result.stdout.split('\n')

        for line in resultLines:
            tmp =re.split(' |,',line.strip())
            for i in tmp:
                key = re.split('=(.*)', i)
                if len(key[0]) > 0:
                    objectsDict[key[0]] = key[1]
                
    return json.loads(json.dumps(objectsDict))
