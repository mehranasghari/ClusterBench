  * This is an instruction for completing address.json

    -----> Time Defenition <-----
    "Time_add_to_end_of_test" : "Amount of time that will add to end time of test to add to backup in seconds(s)"
    "Time_reduce_from_first_of_test" : "Amount of time that will reduce from start time of test to add to backup in seconds(s)"

     -----> First DataBase <------
    "Primary_influxdb_DB_name" : "Name of database of main influxdb that contain data" 
    "Primary_influxdb_container_name" : "Name of main influxdb container"
    "Primary_influxdb_address_in_host" : "Mount point of main influxdb into host in the HOST(MC)"
    "Primary_influxdb_in_cintainer" : "Mount point of main influxdb into host in the CONTAINER"
    
     -----> Second Database <------ 
    "Secondary_influxdb_DB_name" : "Name of database of main influxdb that data will restore on it"
    "Secondary_influxdb_container_name" : "Name of secondary  influxdb container data will restore on this container"
    "Secondary_influxdb_address_in_host" : "Mount point of secondary influxdb into host in the HOST(MC)"
    "Secondry_influxdb_in_container_address" : "Mount point of secondary influxdb into host in the CONTAINER"