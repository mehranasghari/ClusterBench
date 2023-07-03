import json
import influxdb

panel_file_path = "./data.json"
output_file_path = "./queries.txt" # Specify the file path to write the queries

def convert_panel_json_to_influxdb_query(panel_json):
    # Load the JSON from file
    json_data = json.loads(panel_json)

    # Extract query information
    targets = json_data.get("targets", [])

    influxdb_queries = []

    # Process each query target
    for target in targets:
        measurement = target.get("measurement")
        tags = target.get("tags", [])

        # Construct the measurement and tags portion of the query
        measurement_query = f'"{measurement}"'

        tag_queries = []
        for tag in tags:
            tag_name = tag.get("key")
            tag_value = tag.get("value")
            tag_operator = tag.get("operator", "=")
            tag_query = f'("{tag_name}" {tag_operator} {tag_value})'
            tag_queries.append(tag_query)

        tags_query = " AND ".join(tag_queries)

        # Construct the complete InfluxDB query
        influxdb_query = f'SELECT mean("value") FROM {measurement_query} WHERE {tags_query}'+" AND time >= {start_time_query}ms and time <= {end_time_query}ms GROUP BY {group_by} fill(null);"
        influxdb_queries.append(influxdb_query)

    return influxdb_queries

# Read panel JSON from file
with open(panel_file_path, "r") as panel_file:
    panel_json = panel_file.read()

influxdb_queries = convert_panel_json_to_influxdb_query(panel_json)

# Open the file in write mode and write the queries
with open(output_file_path, "w") as output_file:
    for query in influxdb_queries:
        output_file.write(query + "\n")

print(f"Queries written to {output_file_path}")
