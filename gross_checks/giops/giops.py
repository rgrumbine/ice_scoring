import os
import datetime

import netCDF4

surface_parms = [ "iiceconc", "iicedivergence", "iicepressure", "iiceshear", 
                 "iicestrength", "iicesurftemp", "iicevol", "isnowvol", 
                 "itmecrty", "itzocrtx", "sokaraml", "somixhgt",  "sossheig" ]
level = "sfc_0"
grid="ps5km60N"
span="3h-mean"
ymd = datetime.datetime(2022,12,12).strftime("%Y%m%d")
cyc = "00"
base="/u/robert.grumbine/noscrub/model_intercompare/giops/giops."+ymd+"/"

for hr in range(3, 241, 3):
  hhh = "{:03d}".format(hr)
  for parm in surface_parms:
    fname = "CMC_giops_"+parm+"_"+level+"_"+grid+"_"+span+"_"+ymd+cyc+"_P"+hhh+".nc"
    if (not os.path.exists(base+fname)):
        print("problem with "+base+fname)
        continue
    else:
        print("ok")
    #print(fname)


-rw-r--r-- 1 robert.grumbine couple 10727961 Dec 12 05:16 CMC_giops_iiceconc_sfc_0_ps5km60N_3h-mean_2022121200_P003.nc
-rw-r--r-- 1 robert.grumbine couple 10718579 Dec 12 17:15 CMC_giops_iiceconc_sfc_0_ps5km60N_3h-mean_2022121212_P003.nc
-rw-r--r-- 1 robert.grumbine couple 11083848 Dec 12 05:16 CMC_giops_iicedivergence_sfc_0_ps5km60N_3h-mean_2022121200_P003.nc
-rw-r--r-- 1 robert.grumbine couple 11086902 Dec 12 17:16 CMC_giops_iicedivergence_sfc_0_ps5km60N_3h-mean_2022121212_P003.nc
-rw-r--r-- 1 robert.grumbine couple 10991544 Dec 12 05:16 CMC_giops_iicepressure_sfc_0_ps5km60N_3h-mean_2022121200_P003.nc
-rw-r--r-- 1 robert.grumbine couple 10981078 Dec 12 17:16 CMC_giops_iicepressure_sfc_0_ps5km60N_3h-mean_2022121212_P003.nc
-rw-r--r-- 1 robert.grumbine couple 11031879 Dec 12 05:16 CMC_giops_iiceshear_sfc_0_ps5km60N_3h-mean_2022121200_P003.nc
-rw-r--r-- 1 robert.grumbine couple 11032049 Dec 12 17:17 CMC_giops_iiceshear_sfc_0_ps5km60N_3h-mean_2022121212_P003.nc
-rw-r--r-- 1 robert.grumbine couple 10953770 Dec 12 05:17 CMC_giops_iicestrength_sfc_0_ps5km60N_3h-mean_2022121200_P003.nc
-rw-r--r-- 1 robert.grumbine couple 10951799 Dec 12 17:17 CMC_giops_iicestrength_sfc_0_ps5km60N_3h-mean_2022121212_P003.nc
-rw-r--r-- 1 robert.grumbine couple 10575135 Dec 12 05:17 CMC_giops_iicesurftemp_sfc_0_ps5km60N_3h-mean_2022121200_P003.nc
-rw-r--r-- 1 robert.grumbine couple 10575030 Dec 12 17:17 CMC_giops_iicesurftemp_sfc_0_ps5km60N_3h-mean_2022121212_P003.nc
-rw-r--r-- 1 robert.grumbine couple 10878233 Dec 12 05:18 CMC_giops_iicevol_sfc_0_ps5km60N_3h-mean_2022121200_P003.nc
-rw-r--r-- 1 robert.grumbine couple 10877519 Dec 12 17:18 CMC_giops_iicevol_sfc_0_ps5km60N_3h-mean_2022121212_P003.nc
-rw-r--r-- 1 robert.grumbine couple 10899872 Dec 12 05:19 CMC_giops_isnowvol_sfc_0_ps5km60N_3h-mean_2022121200_P003.nc
-rw-r--r-- 1 robert.grumbine couple 10899449 Dec 12 17:18 CMC_giops_isnowvol_sfc_0_ps5km60N_3h-mean_2022121212_P003.nc
-rw-r--r-- 1 robert.grumbine couple 10926960 Dec 12 05:20 CMC_giops_itmecrty_sfc_0_ps5km60N_3h-mean_2022121200_P003.nc
-rw-r--r-- 1 robert.grumbine couple 10933411 Dec 12 17:18 CMC_giops_itmecrty_sfc_0_ps5km60N_3h-mean_2022121212_P003.nc
-rw-r--r-- 1 robert.grumbine couple 10886172 Dec 12 05:20 CMC_giops_itzocrtx_sfc_0_ps5km60N_3h-mean_2022121200_P003.nc
-rw-r--r-- 1 robert.grumbine couple 10893319 Dec 12 17:19 CMC_giops_itzocrtx_sfc_0_ps5km60N_3h-mean_2022121212_P003.nc
-rw-r--r-- 1 robert.grumbine couple 11756367 Dec 12 05:21 CMC_giops_sokaraml_sfc_0_ps5km60N_3h-mean_2022121200_P003.nc
-rw-r--r-- 1 robert.grumbine couple 11751679 Dec 12 17:19 CMC_giops_sokaraml_sfc_0_ps5km60N_3h-mean_2022121212_P003.nc
-rw-r--r-- 1 robert.grumbine couple 11764027 Dec 12 05:21 CMC_giops_somixhgt_sfc_0_ps5km60N_3h-mean_2022121200_P003.nc
-rw-r--r-- 1 robert.grumbine couple 11745772 Dec 12 17:20 CMC_giops_somixhgt_sfc_0_ps5km60N_3h-mean_2022121212_P003.nc
-rw-r--r-- 1 robert.grumbine couple 11916253 Dec 12 05:21 CMC_giops_sossheig_sfc_0_ps5km60N_3h-mean_2022121200_P003.nc
-rw-r--r-- 1 robert.grumbine couple 11946595 Dec 12 17:20 CMC_giops_sossheig_sfc_0_ps5km60N_3h-mean_2022121212_P003.nc
-rw-r--r-- 1 robert.grumbine couple 12778400 Dec 12 05:21 CMC_giops_vomecrty_depth_0.5_ps5km60N_3h-mean_2022121200_P003.nc
-rw-r--r-- 1 robert.grumbine couple 12765314 Dec 12 17:20 CMC_giops_vomecrty_depth_0.5_ps5km60N_3h-mean_2022121212_P003.nc
-rw-r--r-- 1 robert.grumbine couple 11375416 Dec 12 05:21 CMC_giops_vosaline_depth_0.5_ps5km60N_3h-mean_2022121200_P003.nc
-rw-r--r-- 1 robert.grumbine couple 11374082 Dec 12 17:20 CMC_giops_vosaline_depth_0.5_ps5km60N_3h-mean_2022121212_P003.nc
-rw-r--r-- 1 robert.grumbine couple 10802907 Dec 12 05:21 CMC_giops_votemper_depth_0.5_ps5km60N_3h-mean_2022121200_P003.nc
-rw-r--r-- 1 robert.grumbine couple 10805613 Dec 12 17:20 CMC_giops_votemper_depth_0.5_ps5km60N_3h-mean_2022121212_P003.nc
-rw-r--r-- 1 robert.grumbine couple 12552338 Dec 12 05:21 CMC_giops_vozocrtx_depth_0.5_ps5km60N_3h-mean_2022121200_P003.nc
-rw-r--r-- 1 robert.grumbine couple 12686941 Dec 12 17:20 CMC_giops_vozocrtx_depth_0.5_ps5km60N_3h-mean_2022121212_P003.nc
/u/robert.grumbine/noscrub/model_intercompare/giops/giops.20221212
