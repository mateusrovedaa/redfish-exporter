# Redfish-Exporter

This is a Prometheus Exporter for extracting metrics from a server using the Redfish API.
The hostname of the server has to be passed as **target parameter** in the http call.

It has been tested with the following server models:

Cisco UCS C480M5, working properly since BMC FW 4.1(1d)  
Cisco UCS C240M4  
Cisco UCS C240M5  
Cisco UCS C220M4  
Cisco UCS C220M5

Cisco BMC FW below 4.x has its flaws regarding redfish API. Hence, I recommend updating at least to 4.0(1c).

Dell PowerEdge R640  
Dell PowerEdge R730  
Dell PowerEdge R740  
Dell PowerEdge R640  
Dell PowerEdge R840

Lenovo ThinkSystem SR950

HPE DL360 Gen10   
HPE DL560 Gen10

## Build and run

```
docker run -d --restart=always -e USERNAME=redfish -e PASSWORD=xxxxxxxxx -p 9210:9210 quocbao747/redfish-exporter:1.0-beta
```

or just hit `docker compose build && docker compose up -d` with default parameter

## Example Call

```bash
curl http://<IP>:9200/redfish?target=server1.example.com
```

## Parameters

`-l <logfile>` - all output is written to a logfile.

`-d` - switches on debugging mode

## Exported Metrics

All metrics returned by the redfish exporter are gauge metrics.

### redfish_up

Indicating if the redfish API was giving useful data back (== 1) or not (== 0).

### redfish_health

Show the health information of the hardware parts like processor, memory, storage controllers, disks, fans, power and chassis if available.

### redfish_memory_correctable

### redfish_memory_uncorrectable

Showing the count of errors per dimm.

Cisco servers do not seem to provide this kind of information via redfish. Dell PowerEdge servers only with certain DIMM manufacturers (Samsung not, Micron Technology and Hynix Semiconductor do).

### redfish_powerstate

Showing the powerstate of the server

### redfish_response_duration_seconds

The duration of the first response of the server to a call to /redfish/v1

### redfish_up

Metric indicating if there was a valid redfish response while calling /redfish/v1

### redfish_scrape_duration_seconds

Total duration of scarping all data from the server

### redfish_firmware

A collection of firmware version data stored in the labels. The value is always 1.
