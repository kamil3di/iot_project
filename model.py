import paho.mqtt.client as mqtt 
import RPi.GPIO as GPIO
import dht11
import time
import datetime
import sklearn
from sklearn import *
import board
import busio
import joblib
import pandas as pd

#Load model
model = joblib.load("/home/pi/Desktop/knn_files/rf_model.sav")

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# read data using pin 14
instance = dht11.DHT11(pin=14)

client = mqtt.Client()
client.connect("mqtt.thingspeak.com", 1883, 60)

channelId = "1334074" #kendi channel ID'ni gir
apiKey =  "WZO06O50VBD33BWN" #kendi write api key'ini gir

try:
    while True:
        result = instance.read()
        if result.is_valid():
            temp = result.temperature
            humidity = result.humidity
            new_dataset = [[result.temperature],[result.humidity]]
            new_dataset = pd.DataFrame(new_dataset).T
            estimated_apr = ("{:.2f}".format(float(model.predict(new_dataset))))
            publish_path = "channels/" + channelId + "/publish/" + apiKey
            publish_data = "field1=" + str(temp) + "&field2=" + str(humidity) +"&field3=" + str(estimated_apr)
            client.publish(publish_path,publish_data)
            print("Last valid input: " + str(datetime.datetime.now()))
            print("Temperature: %-3.1f C" % result.temperature)
            print("Humidity: %-3.1f %%" % result.humidity)
            print("Estimated APR is: ",  estimated_apr)
        #time.sleep(5)  

except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()
#client.loop(2)
