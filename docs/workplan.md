# Provisional work plan for getting metrics into SQUAC

**TO DO:**
1. Modify `sniffwave_tally` to post WAVE_RING metrics to SQUAC api. Add
  metric name as an argument (we need a different metric name depending on
  where the script runs).
2. Modify `ws_availability` to post wave_server metrics to SQUAC api. (script
  might get renamed, `ws_metrics`).
3. Clean up station_metrics, including renaming some metrics,
https://github.com/pnsn/station_metrics add dataflow_metrics
  documentation (these markdown files are an attempt).
4. Select MUSTANG metrics for the IRIS DMC data holdings dashboard.
5. Write script to select MUSTANG metric measurements and post to SQUAC api.  

## The **PNSN channel storage** dashboard
*Purpose*: To quickly find the import machine where a channel comes in as well
as the wave servers that you can find the data stored in.

*Five Metrics*: import_server, import_ws_port, ewserver_ws_port,
ewserver_sl_port, wave1_port, wave2_port

*Channel group*: all continuous PNSN channels

*How*: on each import server, run findwave.

## The **PNSN internal data flow** dashboard
*Purpose*: Comprehensive view of whether the data is flowing and being saved
everywhere it should without significant gaps.

Nineteen Metrics: import_ring_latency, import_ring_gaps, import_ws_feed,
import_ws_gaps, export_ring_latency, export_ring_gaps, export_ws_feed,
export_ws_gaps, export_sl_feed, export_sl_gaps, wave1_ring_latency,
wave1_ring_gaps, wave1_wws_feed, wave1_wws_gaps, wave2_ring_latency,
wave2_ring_gaps, wave2__wws_feed, wave2_wws_gaps, l1z_late_count

*Channel group*: all continuous PNSN channels

*How*: on each import server, run ws_metrics and sniffwave_tally.

## The **IRIS DMC data holdings** dashboard
*Purpose*: Overview of feed and data latency to the IRIS DMC as well as number of gaps etc. of our data as archived at the IRIS DMC.

*Channel group*: all continuous PNSN channels

*How*: script to be written to take metric measurements from MUSTANG and post
them to SQUAC api.

## The **Station Quality** dashboard
*Purpose*: To get a comprehensive view of the broadband waveform quality of each
channel.

Metrics:

## The **ShakeAlert Phase 1** dashboard
*Purpose*: The ShakeAlert Phase 1 quality criteria for each channel. This
includes time quality, data promptness, and station quality metrics.

Metrics: lcq_acceptable_percent, lce_acceptable_percent,
pct_latency_gt_3.5_ewserver1, pct_completeness_ewserver1, pct_completeness_ewserver1_incl_gap_penalty, gaps_per_hour_ewserver1,
acc_spikes_gt_.34, rms_above_.07



*How*: `eew_stationreport` script to be modified to take measurements based on
 LCQ, LCE channels, sniffwave_tally output, and station_report and post
them to SQUAC api. Alternately: take metrics from SQUAC and reassemble them
into eew_stationreport.

## The **ShakeAlert Phase 2** dashboard
*Purpose*: The ShakeAlert Phase 2 quality criteria for each channel.

Metrics: TBD

## Tasks that every SQUAC-feeding script needs to do
1. Verify that the NSCL exists in SQUAC. If not, query fdsn webservice and add
the NSCL to the NSCL app. --> This is currently **not permitted**, so at this
point script has to abort with a message that the NSCL is not in the SQUAC
database yet. The NSCL list that is in SQUAC will be updated nightly, using
the following request to the FDSN fedcatalog webservice at the DMC:
```
http://service.iris.edu/irisws/fedcatalog/1/query?datacenter=IRISDMC,NCEDC,SCEDC&targetservice=station&level=channel&net=AZ,BC,BK,CC,CE,CI,CN,IU,NC,NN,NP,NV,OO,SN,UO,US,UW&sta=*&cha=?N?,?H?&loc=*&minlat=31.5&maxlat=50&minlon=-128.1&maxlon=-113.8930&endafter=2017-01-01&format=text
```
If this does not include the channels you are interested in, send a inquiry to
Jon Connolly at UW.

2. Verify that the NSCL is a member of the channel group of interest and if not,
to add it.
3.


## Automatically update the channels in the data flow metrics channel group

Run findwave on each import earthworm server. Once an hour or once a day,
check to see if the NSCLs are already in your SQUAC channel group. If yes,
do nothing. If not, add the missing NSCL.

This requires creating a new script that reads the output of findwave, queries
SQUAC for the presence of each NSCL in a designated channel group, if it is
missing, checks to see if it is available in SQUAC and if so, adds it to the
channel group. Question for SQUAC team: can we use the api to add a channel to
the NSCL app? --> not currently, which might be smart.
