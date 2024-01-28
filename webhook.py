import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

app=Flask(__name__)
@app.route('/webhook', methods=['POST'])

def webhook():
    req=request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))

    res=makeResponse(req)
    res=json.dumps(res, indent=4)
    r=make_response(res)
    r.headers['Content-Type']='application/json'
    return r

def makeResponse(req):
    result=req.get("result")
    params=result.get("parameters")
    city=params.get("geo-city")
    date=params.get("date")
    r=requests.get('https://api.openweathermap.org/data/2.5/forecast?q=' +city+ '&appid=8c7f9d083add3660d543ec5bf00e858d')
    json_object=r.json()
    weather=json_object['list']
    for i in range(0,30):
        if date in weather[i]['dt_txt']:
            condition= weather[i]['weather'][0]['description']

    speech=" The forecast for"+city+ "for "+date+ " is " +condition
    return{
        "speech":speech,
        "displayText": speech,
        "source": "apiai-weather-webhook"
    }
if __name__=='__main__':
    port=int(os.getenv('PORT', 5000))
    print("starting app on port %d"  %port)
    app.run(debug=False, port=port, host='0.0.0.0')