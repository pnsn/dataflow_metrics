# SQUAC Utilities
To hold scripts that send stuff to SQUAC via the SQUAC API making use of the squacapi_client.

Metrics about internal data flow at PNSN

See docs/pnsn_dataflow_metrics.md




 ## FOR RENATE LATEST RESULTS

[latest results](https://seismo.ess.washington.edu/ahutko/results_for_renate.txt)

Rsynced every half hour.  This version tosses out anything above 3920 cm/s^2 and is from 2021/4/1 to 2021/6/1. 

Also, I think from the first run (AccValueMax of 392 cm/s^2 and 2020/12/16 to 2021/5/27) you counted numbers wrong maybe?  Here are the numbers I got:

5168 unique sncls

Threshold    N_sncls_gt_0_hp  N_sncls_gt_0_bp  N_sncls_ge_1_per_week_hp N_sncls_ge_1_per_week_bp

3%:                  777              536               50                 26
