from flask import Flask, render_template
import utils
app = Flask(__name__)

@app.route('/', defaults={'version': None})
@app.route('/<string:version>')
def central(version):
    versions = utils.getAllVersions()
    return render_template('index.html', versions = versions)

if __name__=="__main__":
    app.run(debug=True,port=5000,host="0.0.0.0")