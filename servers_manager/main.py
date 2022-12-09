from flask import Flask, render_template, request, jsonify
import utils
app = Flask(__name__)

@app.route('/')
def central():
    return render_template('index.html')

@app.route('/servers')
def servers():
    servers = utils.rankByVersion()
    return servers

@app.route('/refresh', methods=["POST"])
def refresh():
    try:
        if request.json["port"] == None or request.json["host"] == None:
            return 'bad request', 400
        else:
            port = request.json["port"]
            host = request.json["host"]
            return utils.getBuildInfo(host, port), 200
    except KeyError:
        return 'bad request!', 400

@app.route('/users', methods=["POST"])
def users():
    try:
        if request.json["port"] == None or request.json["host"] == None:
            return 'bad request', 400
        else:
            port = request.json["port"]
            host = request.json["host"]
            return utils.getLoggedInUsers(host, port), 200
    except KeyError:
        return 'bad request!', 400

if __name__=="__main__":
    app.run(debug=True,port=5000,host="0.0.0.0")