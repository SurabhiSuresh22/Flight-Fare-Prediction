from flask import Flask, request, render_template
import sklearn
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("flight_rf.pkl", "rb"))

@app.route("/")
def home():
    return render_template("h.html")

@app.route("/predict", methods = ["GET", "POST"])
def predict():
    if request.method == "POST":

        # Date_of_Journey
        date_dep = request.form["Dep_Time"]
        Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)        

        # Departure
        Dep_hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
        
        # Arrival
        date_arr = request.form["Arrival_Time"]
        Arrival_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)        

        # Duration
        dur_hour = abs(Arrival_hour - Dep_hour)
        dur_min = abs(Arrival_min - Dep_min)        

        # Total Stops
        
        stops = int(request.form["stops"])
       
        # airline
        a = ['Jet Airways', 'IndiGo', 'Air India', 'Multiple_carriers','SpiceJet', 'Vistara','GoAir','Multiple carriers Premium economy', 'Jet Airways Business','Vistara Premium economy','Trujet']       
        airline = request.form['airline']
        for i in range(len(a)):
            if airline == a[i]:
                a[i] = 1
            else:
                a[i] = 0
                
        # Source   
        b = ['Delhi','Kolkata','Mumbai','Chennai']            
        Source = request.form["Source"] 
        for i in range(len(b)):
            if Source == b[i]:
                b[i] = 1
            else:
                b[i] = 0

        # Destination
        c = ['Cochin','Delhi','Hyderabad','Kolkata','New Delhi']
        Destination = request.form["Destination"]
        for i in range(len(c)):
            if Destination == c[i]:
                c[i]= 1
            else:
                c[i] =0
          
        prediction = model.predict([[stops,Journey_day,Journey_month,Dep_hour,
        Dep_min, Arrival_hour, Arrival_min,dur_hour,
        dur_min,a[2],a[6],a[1],a[0],a[8],a[3],a[7],a[4],a[10],a[5],a[9],b[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],c[4]]]) 

        output = round(prediction[0],2)

        return render_template('h.html',prediction_text="Your Flight price is Rs. {}".format(output))
    return render_template('h.html')


if __name__ == "__main__":
    app.run(debug=True)
