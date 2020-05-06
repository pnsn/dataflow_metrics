# PNSN data flow metrics
## Waveserver metrics
Script: `ws_availability`, will need to be modified.

| metric name | description | frequency | unit | min_threshold | max_threshold |
|-------------|-------------|-----------|------|---------------|---------------|
import_server | 1, 2, 3, or 4; number of the PNSN import server that brings this channel in | once a day | integer | NA | NA
import_ws_port | port number of the wave_serverV on the import machine in which this channel is stored | once a day | integer | NA | NA
ewserver_ws_port | port number of the wave_serverV on the export machines in which this channel is stored | once a day| integer | NA | NA
ewserver_sl_port | port number of the ringserver (seedlink) on the export machine in which this channel is stored | once a day | integer| NA | NA
wave1_port | port number of the PNSN winston wave server that stores at least six months of data for this channel | once a day | integer | NA | NA
wave2_port | port number of the PNSN winston wave server that stores less than six months of data for this channel | once a day | integer | NA | NA
import_ws_feed | number of seconds between now and end of most recent data in ws | once every 10 mins | seconds | 0.0 | 700.0
export_ws_feed | number of seconds between now and end of most recent data in ws | once every 10 mins | seconds | 0.0 | 700.0
export_sl_feed | number of seconds between now and end of most recent data in ws | once every 10 mins | seconds | 0.0 | 700.0
l1z_late_count | number of l1z channels that are late | once every 10 mins | count | 0 | 20
wave1_wws_feed | number of seconds between now and end of most recent data in wws | once every 10 mins | seconds | 0.0 |700.0
wave2__wws_feed | number of seconds between now and end of most recent data in wws | once every 10 mins | seconds | 0.0 | 700.0
import_ws_gaps | number of gaps in the import wave server | once every 10 mins | count | 0 | TBD
export_ws_gaps | number of gaps in the export wave server | once every 10 mins | count | 0 | TBD
export_sl_gaps | number of gaps in the export ringserver | once every 10 mins | count | 0 | TBD
wave1_wws_gaps | number of gaps in the wave1 Winston wave server | once every 10 mins | count | 0 | TBD
wave2_wws_gaps | number of gaps in the wave2_feed Winston wave server | once every 10 mins | count | 0 | TBD

## WAVE_RING metrics
Script: `sniffwave_tally`, will need to be modified.

| metric name | description | frequency | unit | min_threshold | max_threshold |
|-------------|-------------|-----------|------|---------------|---------------|
| import_ring_latency | number of seconds between now and middle of packet, averaged over 600 seconds | every 10 mins | seconds | 0.0 | 5.0
| export_ring_latency | number of seconds between now and middle of packet, averaged over 600 seconds | every 10 mins | seconds | 0.0 | 5.0
| wave1_ring_latency | number of seconds between now and middle of packet, averaged over 600 seconds | every 10 mins | seconds | 0.0 | 5.0
| wave2_ring_latency | number of seconds between now and middle of packet, averaged over 600 seconds | every 10 mins | seconds | 0.0 | 5.0
| import_ring_gaps | number of gaps in last 10 mins | every 10 mins | count | 0 | 0
| export_ring_gaps | number of gaps in last 10 mins | every 10 mins | count | 0 | 0
| wave1_ring_gaps | number of gaps in last 10 mins | every 10 mins | count | 0 | 0
| wave2_ring_gaps | number of gaps in last 10 mins | every 10 mins | count | 0 | 0
