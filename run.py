import flask
from flask import request, jsonify

from haversine import haversine 
import numpy as np 
import requests 
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def hav_distance(origin_lat,origin_lon,dest_lat,dest_lon): 
  start = (origin_lat, origin_lon) #lat,lon
  end = (dest_lat, dest_lon) 
  return haversine(start, end)

def congestion(day_of_week,start_hour):     
    mon = {16: 0.02, 
           17: 0, 
           18: 0, 
           19: 0, 
           20: 0, 
           21: 0.01, 
           22: 0.2, 
           23: 0.48, 
           0: 0.59, 
           1: 0.43, 
           2: 0.3, 
           3: 0.27, 
           4: 0.26, 
           5: 0.28, 
           6: 0.3, 
           7: 0.3, 
           8: 0.31, 
           9: 0.42, 
           10: 0.58, 
           11: 0.41, 
           12: 0.24, 
           13: 0.20, 
           14: 0.15, 
           15: 0.07}   
    tue = {16: 0.02,
           17: 0, 
           18: 0, 
           19: 0, 
           20: 0, 
           21: 0.02, 
           22: 0.21, 
           23: 0.48, 
           0: 0.58, 
           1: 0.43, 
           2: 0.32, 
           3: 0.29, 
           4: 0.28, 
           5: 0.30, 
           6: 0.32, 
           7: 0.31, 
           8: 0.31, 
           9: 0.42, 
           10: 0.59, 
           11: 0.42, 
           12: 0.25, 
           13: 0.22, 
           14: 0.17, 
           15: 0.09}   
    wed = {16: 0.03, 
           17: 0, 
           18: 0, 
           19: 0, 
           20: 0, 
           21: 0.02, 
           22: 0.2, 
           23: 0.47, 
           0: 0.59, 
           1: 0.45, 
           2: 0.32, 
           3: 0.29, 
           4: 0.28, 
           5: 0.29, 
           6: 0.32, 
           7: 0.30, 
           8: 0.30, 
           9: 0.43, 
           10: 0.60, 
           11: 0.43, 
           12: 0.26, 
           13: 0.22, 
           14: 0.17, 
           15: 0.08} 
    thurs = {16: 0.02, 
           17: 0, 
           18: 0, 
           19: 0, 
           20: 0, 
           21: 0.02, 
           22: 0.20, 
           23: 0.45, 
           0: 0.55, 
           1: 0.43, 
           2: 0.33, 
           3: 0.30, 
           4: 0.29, 
           5: 0.30, 
           6: 0.33, 
           7: 0.32, 
           8: 0.33, 
           9: 0.45, 
           10: 0.62, 
           11: 0.45, 
           12: 0.27, 
           13: 0.24, 
           14: 0.19, 
           15: 0.09}
    fri = {16: 0.03, 
           17: 0, 
           18: 0, 
           19: 0, 
           20: 0, 
           21: 0.02, 
           22: 0.19, 
           23: 0.44, 
           0: 0.52, 
           1: 0.43, 
           2: 0.34, 
           3: 0.32, 
           4: 0.32, 
           5: 0.31, 
           6: 0.37, 
           7: 0.35, 
           8: 0.36, 
           9: 0.52, 
           10: 0.69, 
           11: 0.49, 
           12: 0.29, 
           13: 0.28, 
           14: 0.26, 
           15: 0.15} 
    sat = {16: 0.07, 
           17: 0.02, 
           18: 0, 
           19: 0, 
           20: 0, 
           21: 0.01, 
           22: 0.1, 
           23: 0.14, 
           0: 0.21, 
           1: 0.28, 
           2: 0.33, 
           3: 0.37, 
           4: 0.37, 
           5: 0.37, 
           6: 0.35, 
           7: 0.34, 
           8: 0.33, 
           9: 0.33, 
           10: 0.36, 
           11: 0.33, 
           12: 0.25, 
           13: 0.25, 
           14: 0.23, 
           15: 0.14} 
    sun = {16: 0.06, 
           17: 0.01, 
           18: 0, 
           19: 0, 
           20: 0, 
           21: 0, 
           22: 0.06, 
           23: 0.08, 
           0: 0.13, 
           1: 0.16, 
           2: 0.20, 
           3: 0.23, 
           4: 0.24, 
           5: 0.24, 
           6: 0.22, 
           7: 0.21, 
           8: 0.21, 
           9: 0.22, 
           10: 0.22, 
           11: 0.21, 
           12: 0.20, 
           13: 0.18, 
           14: 0.13, 
           15: 0.07}
    if day_of_week == 0: 
        return mon[start_hour] 
    elif day_of_week == 1: 
        return tue[start_hour] 
    elif day_of_week == 2: 
        return wed[start_hour] 
    elif day_of_week == 3: 
        return thurs[start_hour] 
    elif day_of_week == 4: 
        return fri[start_hour] 
    elif day_of_week == 5: 
        return sat[start_hour] 
    elif day_of_week == 6: 
        return sun[start_hour]  

def euclidean(origin_lat,origin_lon,dest_lat,dest_lon): 
    return np.sqrt((origin_lat-origin_lon)**2+(origin_lon-dest_lon)**2)

def is_daytime(start_hour): 
  if start_hour in [0,1,2,3,4,5,6,7,8,9,10,23]: 
    return int(1) 
  else:
    return int(0) 

def weekend(day_of_week): 
  if day_of_week >= 5: 
    return int(1) 
  else: 
    return int(0)

def eta(origin_lat, origin_lon, dest_lat, dest_lon, start_hour, day_of_week):    
    """
    origin_lat : origin_latitude,  
    origin_lon : origin_longitude, 
    dest_lat : destination_latitude, 
    dest_lon : destination_longitude, 
    start_hour : trip start hour (0-23 UTC),
    day_of_week : day of trip (0-6 MON TO SUN UTC)
    """ 
    traffic_congestion = float(congestion(day_of_week,start_hour))
    haversine = float(hav_distance(origin_lat,origin_lon,dest_lat,dest_lon))
    eud_dist = float(euclidean(origin_lat,origin_lon,dest_lat,dest_lon))
    is_day = int(is_daytime(start_hour))
    is_weekend = int(weekend(day_of_week))
    body = { 
              "data": [  
                    { 
                      "origin_lat": origin_lat, 
                      "origin_lon": origin_lon, 
                      "dest_lat": dest_lat,  
                      "dest_lon": dest_lon, 
                      "start_hour": start_hour, 
                      "day_of_week": day_of_week, 
                      "lat_diff": 0, #both lat_diff and lon_diff are dummy inputs, not used in the model, originally part of the csv ingested to create our model
                      "lon_diff": 0,
                      "eud_dist": eud_dist, 
                      "haversine": haversine, 
                      "congestion": traffic_congestion, 
                      "is_day": is_day, 
                      "is_weekend": is_weekend 
                     }  
                  ]  
            }
    scoring_uri = 'http://1b42df7d-7ae6-4b3e-900b-e55446c86883.southeastasia.azurecontainer.io/score'  
    input_data = json.dumps(body,indent=2)
    headers = {"Content-Type": "application/json"}
    response = requests.post(scoring_uri, input_data, headers=headers).json()
    return str(round(json.loads(response)['result'][0])) #returns int object as part of competition requirements

@app.route('/')
def home():
    return '''<h1>Teh Cino Grab ETA Prediction</h1>
<p>You're actually at the wrong place. This is the main page.</p>
<p>Please make a POST request at </p>https://teamcinopreprocessapi.herokuapp.com/api/v1.0/etaAPI'''

@app.route('/api/v1.0/etaAPI', methods = ['POST'])
def predictETA():
    if request.method == 'POST':
        origin_lat = request.json.get('origin_lat')
        origin_lon = request.json.get('origin_lon')
        dest_lat = request.json.get('dest_lat')
        dest_lon = request.json.get('dest_lon')
        start_hour = request.json.get('start_hour')
        day_of_week = request.json.get('day_of_week') 

        return eta(origin_lat, origin_lon, dest_lat, dest_lon, start_hour, day_of_week)

if __name__ == '__main__':
    app.run()