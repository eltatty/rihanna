#!/usr/bin/python3
import json, requests

def removeKeys(jobsToRemove, observersConfList):
    jobsDict = {}
    jobsDict['jobs'] = []
    for idx, el in enumerate(jobsToRemove['jobs']):
        jobsDict['jobs'].append({})
        for key in el.keys():
            if key in observersConfList:
                jobsDict['jobs'][idx][key] = el[key]
    return json.loads(json.dumps(jobsDict))

# def singleJobUpdate(starting_jobs, updatedJobIDs):


def updateJobs(running_jobs_file, url):
    res = requests.get(url + '/jobsList/')

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

    extra_jobs = []

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
        new_jobs = removeKeys(res.json(), observersConfList)
        for new_job in new_jobs['jobs']:
            job_addition = 0
            updatedJobIDs.append(new_job['JobId'])
            for idx_old in range(len(jobs['jobs'])): 
                if jobs['jobs'][idx_old]['JobId'] == new_job['JobId']:
                    jobs['jobs'][idx_old] = new_job;
                    job_addition = 1
                    break
            if job_addition == 0:
                jobs['jobs'].append(new_job)


        # Update the jobs that did not show in squeue
        for starting_job in starting_jobs['jobs']:
            if starting_job['JobId'] not in updatedJobIDs:
                res = requests.get(url + '/jobInfo/' + starting_job['JobId'])
                if res.ok:
                    if "slurm_load_jobs error" in res.json():
                        print(starting_job['JobId'])
                        # starting_job['Reason'] = "slurm_load_jobs error: {}".format(res.json().get('slurm_load_jobs error'))
                        # print(starting_job['Reason'])

#BOOT_FAIL,DEADLINE,FAILED,NODE_FAIL,OUT_OF_MEMORY,PREEMPTED,REVOKED,TIMEOUT
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
                print(f" [{starting_jobs['jobs'][idx]['JobId']}]\t\t[{starting_jobs['jobs'][idx]['JobState']}]\t[{jobs['jobs'][idx]['JobState']}]")
            except IndexError:
                print(f" [{jobs['jobs'][idx]['JobId']}]\t\t[NULL]\t\t[{jobs['jobs'][idx]['JobState']}]")

updateJobs('jobs.json', 'http://localhost:5000')

# extra_jobs = []
# extra_jobs.append(new_job)
# jobs['jobs'].extend(extra_jobs)