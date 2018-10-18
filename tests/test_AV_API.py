import requests
import csv

api_key = ""
with open("AV_token.txt", "r") as f:
    api_key = f.readline()


req = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=" + api_key + "&datatype=csv"
data = requests.get(req)

with open('out.csv', 'w') as f: 
    writer = csv.writer(f) 
    reader = csv.reader(data.text.splitlines()) 

    for row in reader: 
     writer.writerow(row) 