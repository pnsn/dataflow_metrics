#!/home/ahutko/anaconda3/bin/python

#
# Tally up all instances of acc >1% and 3%g (10 and 30cm/s^2) using
#   max Acc, both HP and BP.  acc_gt_2.0 (metric_id=86), 
#   hourly_max_acc (109), hourly_max_bp_acc (94)
#

import os
import datetime
from pytz import timezone
import numpy as np
import requests

# Import modules
try:
    from squacapi_client.models.write_only_measurement_serializer \
    import WriteOnlyMeasurementSerializer
    from squacapi_client.pnsn_utilities \
    import get_client, make_channel_map, make_metric_map, perform_bulk_create
    no_squacapi = False
except Exception as e:
    print("Info: squacapi_client not available, cannot use --squac option")
    no_squacapi = True

USER = os.environ['SQUACAPI_USER']
PASSWORD = os.environ['SQUACAPI_PASSWD']
HOST = 'https://squacapi.pnsn.org'

# Iniate the client
squac_client = get_client(USER, PASSWORD, HOST)

# Get all metrics; you'll need the right metric_id
#squac_metrics = squac_client.v1_0_measurement_metrics_list()
#metric_ids = []
#metric_names = {}
#for i in range(0,len(squac_metrics)):
#    metric_ids.append(squac_metrics[i].id)
#    metric_names[squac_metrics[i].id] = squac_metrics[i].name

# 109 hourly_max_acc
# 94 hourly_max_bp_acc
# 110 hourly_noise_floor_acc
# 86 acc_gt_2.0
# 84 hourly_mean

# Read in ShakeAlert chanfile
#(base) ahutko@namazu:~/proj/STATION_REPORT/DATA_MINING$ head Chanfile_ShakeAlert_all_Jan2021
#AZ   BZN -- HHE 33.4915 -116.6670  1301.0   100.00  6.299190e+06      counts/(cm/sec)       1.331692  90.0   0.0 UNKNOWN
#AZ   BZN -- HHN 33.4915 -116.6670  1301.0   100.00  6.299190e+06      counts/(cm/sec)       1.331692   0.0   0.0 UNKNOWN

# Read in list of ShakeAlert chanfiles
url = 'https://seismo.ess.washington.edu/ahutko/ShakeAlert_Chanfiles/chanfile_all.dat'
fShakeAlert = requests.get(url)
ShakeAlertSNCLs = []
for lineb in fShakeAlert.iter_lines():
    line = lineb.decode('utf-8')
    if ( '#' not in line ):
        try:
            sncl = line.split()[0] + '.' + line.split()[1] + '.' + line.split()[2] + '.' + line.split()[3]
            ShakeAlertSNCLs.append(sncl)
        except:
            pass

# Read in file that has all the SNCLs and squac channel ids (faster than 
#   currently barfing squac)
f = open('channels_squacids_west_coast')
lines = f.readlines()
f.close()
channels = {}
mychannels = []
for line in lines:
    sncl = line.split()[0]
    chid = line.split()[1]
    stat = sncl.split('.')[1]
    net = sncl.split('.')[0]
    chan = sncl.split('.')[3]
    slat = line.split()[4]
    slon = line.split()[5]
    channels[sncl] = [ chid, stat, slat, slon ]
    mychannels.append(sncl)

# hourly_max_acc (109) was created on 2021-12-15 in squac db
T1 = datetime.datetime(2020, 12, 16, 0, 0, 0).replace(tzinfo=timezone('UTC'))
T2 = datetime.datetime(2021, 5, 27, 0, 0, 0).replace(tzinfo=timezone('UTC'))

metric_ids = [ 109, 94 ]
accvaluemax = 98 * 4 # (this is 4g)

print('TIMES: ',T1, T2, ' AccValueMax: ',accvaluemax, ' cm/s^2')

for sncl in mychannels:
    channel_id = channels[sncl][0]
    slat = channels[sncl][2]
    slon = channels[sncl][3]
    distances = [ 30, 50, 100, 200 ]
    magnitudes = [ 3.0, 4.0, 5.0, 6.0 ]
    if ( sncl in ShakeAlertSNCLs ):
        for i in range(0,4):
            url = "https://prod-earthquake.cr.usgs.gov/fdsnws/event/1/query?format=xml&starttime=2020-10-21&endtime=2021-05-30&minmagnitude=" + str(magnitudes[i])  +  "&latitude=" + slat + "&longitude=" + slon + "&maxradiuskm=" + str(distances[i]) + "&format=text"
            feq = requests.get(url)
            eq_times = []
            for lineb in feq.iter_lines():
                line = lineb.decode('utf-8')
                if ( "#" not in line ):
                    timestr = line.split('|')[1]
                    qtime = datetime.datetime.strptime(timestr, '%Y-%m-%dT%H:%M:%S.%f')
                    qtime = qtime.replace(minute=0, second=0, microsecond=0)
                    mag  = float(line.split('|')[10])
                    eq_times.append(qtime.replace(tzinfo=timezone('UTC'))) 
        try:
            values = {}
            valuesarray = {}
            starttimes = {}
            ncount = {}
            nskipped = {}
            for metric_id in metric_ids:
                values[metric_id] = []
                starttimes[metric_id] = []
                ncount[metric_id] = 0
                nskipped[metric_id] = 0
                measurements = squac_client.v1_0_measurement_measurements_list(metric=metric_id, channel=channel_id, starttime=T1, endtime=T2)
                for measurement in measurements:
                    starttime = measurement.starttime
                    if ( starttime not in eq_times ):
                        if ( measurement.value < accvaluemax ):
                            values[metric_id].append(measurement.value)
                            starttimes[metric_id].append(measurement.starttime)
                            ncount[metric_id] += 1
                    else:
                        nskipped[metric_id] += 1
                valuesarray[metric_id] = np.asarray(values[metric_id])
                valuesarray[metric_id].sort()
                a = valuesarray[metric_id][valuesarray[metric_id] > 9.8]
            N_gt_5pct_hp = len(valuesarray[metric_ids[0]][valuesarray[metric_ids[0]] > 4.9])
            N_gt_10pct_hp = len(valuesarray[metric_ids[0]][valuesarray[metric_ids[0]] > 9.8])
            N_gt_30pct_hp = len(valuesarray[metric_ids[0]][valuesarray[metric_ids[0]] > 3*9.8])
            N_gt_5pct_bp = len(valuesarray[metric_ids[1]][valuesarray[metric_ids[1]] > 4.9])
            N_gt_10pct_bp = len(valuesarray[metric_ids[1]][valuesarray[metric_ids[1]] > 9.8])
            N_gt_30pct_bp = len(valuesarray[metric_ids[1]][valuesarray[metric_ids[1]] > 3*9.8])
            maxhp = max(valuesarray[metric_ids[0]])
            maxbp = max(valuesarray[metric_ids[1]])
            hp_50 = valuesarray[metric_ids[0]][int(len(valuesarray[metric_ids[0]])*.5)]
            bp_50 = valuesarray[metric_ids[1]][int(len(valuesarray[metric_ids[1]])*.5)]
            hp_95 = valuesarray[metric_ids[0]][int(len(valuesarray[metric_ids[0]])*.95)]
            bp_95 = valuesarray[metric_ids[1]][int(len(valuesarray[metric_ids[1]])*.95)]
            hp_99 = valuesarray[metric_ids[0]][int(len(valuesarray[metric_ids[0]])*.99)]
            bp_99 = valuesarray[metric_ids[1]][int(len(valuesarray[metric_ids[1]])*.99)]
            if ( ncount[metric_ids[1]] > 1 ):
              print(sncl, N_gt_5pct_hp, N_gt_5pct_bp, N_gt_10pct_hp, N_gt_10pct_bp, N_gt_30pct_hp, N_gt_30pct_bp, maxhp, maxbp, hp_50, bp_50, hp_95, bp_95, hp_99, bp_99, ncount[metric_ids[0]], ncount[metric_ids[1]], nskipped[metric_ids[0]], nskipped[metric_ids[1]] )
        except:
            pass


