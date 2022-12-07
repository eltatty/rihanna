from flask import Flask, render_template
import utils
app = Flask(__name__)

@app.route('/')
def central():
    return render_template('index.html')

@app.route('/servers')
def servers():
    servers = utils.rankByVersion()
    return servers

if __name__=="__main__":
    app.run(debug=True,port=5000,host="0.0.0.0")