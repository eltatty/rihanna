import subprocess
import re
import json


def submitJob(jobFile):
    result = subprocess.run(['sbatch', f"./jobsDir/{jobFile}"], text=True, capture_output=True)
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
        if len(job_lines) > 1:
            for job_line in job_lines:
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