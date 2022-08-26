import json, os, slurmFunctions, time
from flask import Flask, request, redirect, url_for
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './jobsDir'

app = Flask(__name__)
api = Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class JobInfo(Resource):
    def get(self, jobId):
        return slurmFunctions.getInfo(jobId)

class JobsList(Resource):
    def get(self):
        return slurmFunctions.getJobs()

class JobDebug(Resource):
    def get(self):
        return {"Debug" : "Yes"}
    
class JobSubmit(Resource):
    def post(self):
        file = request.files['file']
        filename = secure_filename(file.filename)
        milliseconds = str(round(time.time()* 1000))
        jobFile = filename.split('.')[0] + milliseconds + "." + filename.split('.')[1]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], jobFile))
        return slurmFunctions.submitJob(jobFile);
    
api.add_resource(JobInfo,"/jobInfo/<int:jobId>")
api.add_resource(JobSubmit, "/jobSubmit/")
api.add_resource(JobDebug, "/jobDebug/")
api.add_resource(JobsList, "/jobsList/")

if __name__ == "__main__":
    app.run(host="0.0.0.0")