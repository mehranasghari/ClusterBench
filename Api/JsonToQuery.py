import json
import os
import subprocess

query_file_path = "./Grafana-dasboard.json"
output_file_path_with_space = "./queries.txt"
query_file_path_without_space = "./query.txt"



# Convert JSON to InfluxDB query
def convert_panel_json_to_influxdb_query(query_file_path, output_file_path):
    with open(query_file_path) as file:
        json_data = json.load(file)

    targets = json_data.get("targets", [])
    influxdb_queries = []

    for target in targets:
        measurement = target.get("measurement")
        tags = target.get("tags", [])

        measurement_query = f'"{measurement}"'

        tag_queries = []
        for tag in tags:
            tag_name = tag.get("key")
            tag_value = tag.get("value")
            tag_operator = tag.get("operator", "=")
            tag_query = f'("{tag_name}" {tag_operator} {tag_value})'
            tag_queries.append(tag_query)

        tags_query = " AND ".join(tag_queries)

        influxdb_query = f'\'SELECT mean("value") FROM {measurement_query}'+' WHERE ("host" =~ /^{host}$/) AND time >= {start_time_query}ms AND time <= {end_time_query}ms GROUP BY {group_by} fill(null)\''

        influxdb_queries.append(influxdb_query)

    with open(output_file_path, 'w') as file:
        file.write('\n'.join(influxdb_queries))
    
convert_panel_json_to_influxdb_query(query_file_path, output_file_path_with_space)

# Ckeck output content and print if it is successfull or not
def content_checker(output_file_path):
    size = os.path.getsize(output_file_path)
    if size != 0:
        print("\033[92mQuery Converted\033[0m")
    else:
        print("\033[91mQuery Converting Failed\033[0m")
content_checker(output_file_path_with_space)