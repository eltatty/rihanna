#!/usr/bin/python3
import json, requests

def removeKeys(jobsToRemove, observersConfList):
    if 'jobs' in jobsToRemove.keys():
        jobsDict = {}
        jobsDict['jobs'] = []
        for idx, el in enumerate(jobsToRemove['jobs']):
            jobsDict['jobs'].append({})
            for key in el.keys():
                if key in observersConfList:
                    jobsDict['jobs'][idx][key] = el[key]
        return json.loads(json.dumps(jobsDict))
    else:
        job = {}
        for key in jobsToRemove.keys():
            if key in observersConfList:
                job[key] = jobsToRemove[key]
        return json.loads(json.dumps(job))


def updateJobs(running_jobs_file, url):
    try:
        res = requests.get(url + '/jobsList/')
    except requests.exceptions.ConnectionError as e:
        print(e)
        return 1

    # Keep Only these values which are accepted in observers.conf.
    # In order to get more attributes update observers.conf as well as this list.
    observersConfList = ['JobId', 'JobName', 'UserId', 'JobState', 'Reason', 'NodeList', 
                        'NumCPUs', 'NumTasks', 'Priority','SubmitTime', 'StartTime']


    # Change here the job.json to the running_jobs_example.json path
    with open(running_jobs_file, 'r') as jobs_file:
        try:
            jobs = json.load(jobs_file)
        except ValueError:
            jobsDict = {}
            jobsDict['jobs'] = []
            jobs = json.loads(json.dumps(jobsDict))
        jobs_file.close()

    # The jobs that already exist in the file.
    starting_jobs = {}
    starting_jobs['jobs'] = []
    starting_jobs['jobs'].extend(jobs['jobs'])

    # List of JobIDs that returned in request
    updatedJobIDs = []

    # It might needs to sort the lists or at least check if the new_jobs list comes always sorted,
    # that will help to perform faster searching techniques and update the new_jobs.
    if res.ok:
        # Remove unnecessary keys (you can modify).
        incoming_jobs = removeKeys(res.json(), observersConfList)
        
        if len(jobs['jobs']) == 0:
            # If file is empty just add all the incoming jobs.
            jobs['jobs'].extend(incoming_jobs['jobs'])
        else: 
            for idx in range(len(jobs['jobs'])):
                jobUpdate = 0
                if 'jobs' in incoming_jobs.keys():
                    for inc_job in incoming_jobs['jobs']:
                        if inc_job['JobId'] == jobs['jobs'][idx]['JobId']:
                            jobs['jobs'][idx] = inc_job
                            jobUpdate = 1
                            incoming_jobs['jobs'].remove(inc_job)
                            break
                if jobUpdate == 0:
                    # Job was not in th squeue command so look for it by ID
                    res = requests.get(url + '/jobInfo/' + jobs['jobs'][idx]['JobId'])
                    if res.ok:
                        if "slurm_load_jobs error" in res.json():
                            JobId = jobs['jobs'][idx]['JobId']
                            jobs['jobs'][idx].update( (key,"Unknown") for key in jobs['jobs'][idx])
                            jobs['jobs'][idx]['JobState'] = 'REVOKED'
                            jobs['jobs'][idx]['Reason'] = "slurm_load_jobs error: {}".format(res.json().get('slurm_load_jobs error').strip())
                            jobs['jobs'][idx]['JobId'] = JobId
                        else:
                            jobs['jobs'][idx] = removeKeys(res.json(), observersConfList)

            
            # Add the newly created jobs
            if len(incoming_jobs['jobs']) > 0:
                jobs['jobs'].extend(incoming_jobs['jobs'])

        # Update the running_jobs_file.json.
        with open(running_jobs_file, 'w') as jobs_file:
            json.dump(jobs, jobs_file, indent = 2)
            jobs_file.close()
            
        # Debugging Blocks.
        print("----------------------------------------")
        print("[JobId]\t\t[Before]\t[After]")
        print("----------------------------------------")
        for idx in range(len(jobs['jobs'])):
            try:
                print("[{}]\t\t[{}]\t[{}]".format(starting_jobs['jobs'][idx]['JobId'],starting_jobs['jobs'][idx]['JobState'],jobs['jobs'][idx]['JobState']))
            except IndexError:
                print("[{}]\t\t[NULL]\t\t[{}]".format(jobs['jobs'][idx]['JobId'],jobs['jobs'][idx]['JobState']))

# Give path of the Json Running Jobs File
updateJobs('jobs.json', 'http://localhost:5000')

# Call the SPDRM process.updateObservableJobs()
