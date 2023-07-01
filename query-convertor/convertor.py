import json

def convert_panel_json_to_influxdb_query(panel_json):
    # Load the JSON from file or API response
    json_data = json.loads(panel_json)

    # Extract query information
    targets = json_data.get("targets", [])

    influxdb_queries = []

    # Process each query target
    for target in targets:
        query_type = target.get("type")

        if query_type == "query":
            # Extract raw InfluxDB query
            influxdb_query = target.get("query")

        elif query_type == "table" or query_type == "timeseries":
            measurement = target.get("measurement")
            tags = target.get("tags", [])
            fields = target.get("fields", [])

            # Construct the measurement and tags portion of the query
            measurement_query = f'"{measurement}"'

            tag_queries = []
            for tag in tags:
                tag_name = tag.get("key")
                tag_value = tag.get("value")
                tag_operator = tag.get("operator", "=")
                tag_query = f'"{tag_name}" {tag_operator} \'{tag_value}\''
                tag_queries.append(tag_query)

            tags_query = " AND ".join(tag_queries)

            # Construct the fields portion of the query
            field_queries = []
            for field in fields:
                field_func = field.get("func", "")
                field_name = field.get("key")
                field_query = f'{field_func}("{field_name}")'
                field_queries.append(field_query)

            fields_query = ", ".join(field_queries)

            # Construct the complete InfluxDB query
            influxdb_query = f'SELECT {fields_query} FROM {measurement_query} WHERE {tags_query}'

        else:
            # Handle unsupported query types
            influxdb_query = None
            print(f"Unsupported query type: {query_type}")

        if influxdb_query:
            influxdb_queries.append(influxdb_query)

    return influxdb_queries

# Example usage
panel_json = '''
{
    "id": 39,
    "gridPos": {
      "h": 7,
      "w": 8,
      "x": 0,
      "y": 0
    },
    "type": "graph",
    "title": "CPU - S1",
    "transformations": [
      {
        "id": "calculateField",
        "options": {
          "alias": "Mean - all",
          "mode": "reduceRow",
          "reduce": {
            "include": [],
            "reducer": "sum"
          },
          "replaceFields": false
        }
      }
    ],
    "thresholds": [],
    "pluginVersion": "8.0.0",
    "legend": {
      "avg": false,
      "current": false,
      "max": false,
      "min": false,
      "show": true,
      "total": false,
      "values": false
    },
    "aliasColors": {},
    "dashLength": 10,
    "fill": 1,
    "lines": true,
    "linewidth": 1,
    "nullPointMode": "null",
    "options": {
      "alertThreshold": true
    },
    "pointradius": 2,
    "renderer": "flot",
    "seriesOverrides": [],
    "spaceLength": 10,
    "targets": [
      {
        "alias": "User - s1",
        "datasource": {
          "type": "influxdb",
          "uid": "06O86T24z"
        },
        "groupBy": [
          {
            "params": [
              "$timeVariable"
            ],
            "type": "time"
          },
          {
            "params": [
              "none"
            ],
            "type": "fill"
          }
        ],
        "measurement": "netdata.system.cpu.user",
        "orderByTime": "ASC",
        "policy": "default",
        "query": "SELECT mean(\"value\") FROM \"netdata.system.cpu.user\" WHERE (\"host\" =~ /^$hostIs$/) AND $timeFilter GROUP BY time($timeVariable) fill(null)",
        "rawQuery": false,
        "refId": "A",
        "resultFormat": "time_series",
        "select": [
          [
            {
              "params": [
                "value"
              ],
              "type": "field"
            },
            {
              "params": [],
              "type": "mean"
            }
          ]
        ],
        "tags": [
          {
            "key": "host",
            "operator": "=~",
            "value": "/^$hostIs$/"
          }
        ]
      },
      {
        "alias": "System - s1",
        "datasource": {
          "type": "influxdb",
          "uid": "06O86T24z"
        },
        "groupBy": [
          {
            "params": [
              "$timeVariable"
            ],
            "type": "time"
          },
          {
            "params": [
              "none"
            ],
            "type": "fill"
          }
        ],
        "measurement": "netdata.system.cpu.system",
        "orderByTime": "ASC",
        "policy": "default",
        "refId": "B",
        "resultFormat": "time_series",
        "select": [
          [
            {
              "params": [
                "value"
              ],
              "type": "field"
            },
            {
              "params": [],
              "type": "mean"
            }
          ]
        ],
        "tags": [
          {
            "key": "host",
            "operator": "=~",
            "value": "/^$hostIs$/"
          }
        ]
      },
      {
        "alias": "Iowait - s1",
        "datasource": {
          "type": "influxdb",
          "uid": "06O86T24z"
        },
        "groupBy": [
          {
            "params": [
              "$timeVariable"
            ],
            "type": "time"
          },
          {
            "params": [
              "none"
            ],
            "type": "fill"
          }
        ],
        "measurement": "netdata.system.cpu.iowait",
        "orderByTime": "ASC",
        "policy": "default",
        "refId": "C",
        "resultFormat": "time_series",
        "select": [
          [
            {
              "params": [
                "value"
              ],
              "type": "field"
            },
            {
              "params": [],
              "type": "mean"
            }
          ]
        ],
        "tags": [
          {
            "key": "host",
            "operator": "=~",
            "value": "/^$hostIs$/"
          }
        ]
      },
      {
        "alias": "idle - s1 ",
        "datasource": {
          "type": "influxdb",
          "uid": "06O86T24z"
        },
        "groupBy": [
          {
            "params": [
              "$timeVariable"
            ],
            "type": "time"
          },
          {
            "params": [
              "none"
            ],
            "type": "fill"
          }
        ],
        "hide": true,
        "measurement": "netdata.system.cpu.idle",
        "orderByTime": "ASC",
        "policy": "default",
        "refId": "D",
        "resultFormat": "time_series",
        "select": [
          [
            {
              "params": [
                "value"
              ],
              "type": "field"
            },
            {
              "params": [],
              "type": "mean"
            }
          ]
        ],
        "tags": [
          {
            "key": "host",
            "operator": "=~",
            "value": "/^$hostIs$/"
          }
        ]
      }
    ],
    "timeRegions": [],
    "tooltip": {
      "shared": true,
      "sort": 0,
      "value_type": "individual"
    },
    "xaxis": {
      "buckets": null,
      "mode": "time",
      "name": null,
      "show": true,
      "values": []
    },
    "yaxes": [
      {
        "$$hashKey": "object:46",
        "format": "short",
        "label": null,
        "logBase": 1,
        "max": null,
        "min": null,
        "show": true
      },
      {
        "$$hashKey": "object:47",
        "format": "short",
        "label": null,
        "logBase": 1,
        "max": null,
        "min": null,
        "show": true
      }
    ],
    "yaxis": {
      "align": false,
      "alignLevel": null
    },
    "bars": false,
    "dashes": false,
    "fillGradient": 0,
    "hiddenSeries": false,
    "percentage": false,
    "points": false,
    "stack": false,
    "steppedLine": false,
    "timeFrom": null,
    "timeShift": null,
    "datasource": null
  }
'''

influxdb_queries = convert_panel_json_to_influxdb_query(panel_json)
for query in influxdb_queries:
    print(query)
