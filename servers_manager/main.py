from flask import Flask, render_template
import utils
app = Flask(__name__)

@app.route('/')
def test():
    
    items = {
        'name':'cevt19x',
        'version': '1.8.0'
    }
    return render_template('index.html', data = items)
    # return return_value;

if __name__=="__main__":
    app.run(debug=True,port=5000,host="0.0.0.0")