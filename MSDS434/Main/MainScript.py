#Libraries
from flask import Flask, render_template, request
import urllib
import json
import os

#Variables
app = Flask(__name__)
@app.route("/")
#Functions
def index():
    return render_template('index.html')

def getData(input_text):
    data = {
        "Inputs": {
            "WebServiceInput0":
            [
                {
                        'CODE_med': "0",
                        'DESCRIPTION_med': input_text,
                        'CODE': "0",
                        'DESCRIPTION': "0",
                },
            ],
        },
        "GlobalParameters":  {
        }
    }
    body = str.encode(json.dumps(data))
#testing
    url = ''
    api_key = '' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read().decode('utf-8')
        obj = json.loads(result)
        
        return obj['Results']['WebServiceOutput0'][0]['Scored Labels']
    except urllib.error.HTTPError as error:
        return "The request failed with status code: " + str(error.code)

@app.route("/", methods=['GET', 'POST'])
def my_form_post():
    if request.method == 'POST':
        text = request.form['u']
        processed_text = text
        response = getData(processed_text)

    return response

#Main
if __name__ == "__main__":
    app.run()