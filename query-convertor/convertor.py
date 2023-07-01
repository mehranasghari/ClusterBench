from influxdb import InfluxDBClient
import json
file_path = "./data.json"

client = InfluxDBClient(host='localhost', port=8086)
with open('file_path', 'r') as f:
    data = json.load(f)
client.write_points(data)
