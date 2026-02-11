'''
Plot output from gross error check
Robert Grumbine
'''

import sys

import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

#----------------------------------------------------------
fin = open(sys.argv[1],"r", encoding='utf-8')

try:
  title_tag = sys.argv[2]
except:
  title_tag = "ref"

markersize = float(sys.argv[3])

parm = []
i = []
j = []
lon = []
lat = []

for line in fin:
  if ("pm" in line):
    words = line.split()
    try:
      tp = (words[0].split(":"))[1]
    except:
      tp = words[0]
    parm.append(tp)
    i.append(int(words[1]))
    j.append(int(words[2]))
    lon.append(float(words[3]))
    tll = float(words[4])
    lat.append(tll)

print("found ",len(i)," error points")
if (len(i) == 0):
    sys.exit(0)

#debug print(max(lat), min(lat), max(lon), min(lon) )
latmax = max(lat)
latmin = min(lat)
lonmax = max(lon)
lonmin = min(lon)


# i-j plot of error points ----------------------------------
matplotlib.use('Agg') #batch mode


#Elaborations:
#  title
#  axis labels
#  separate color/symbol per parameter
#  different sizes per parameter

fig,ax = plt.subplots()
plt.scatter(i,j, s = markersize)
ax.grid() 
plt.title(title_tag)
plt.savefig("ij_errs_"+title_tag+".png")
plt.close()


# lat-lon plot of error points ---------------------------------

proj = ccrs.NorthPolarStereo(central_longitude=-170., true_scale_latitude = 60.)
#proj = ccrs.LambertConformal(central_longitude=-170., central_latitude = 60., cutoff=25.)
#proj = ccrs.PlateCarree()

ax = plt.axes(projection = proj)
fig = plt.figure(figsize = (8,6))
ax = fig.add_subplot(1,1,1,projection = proj)
plt.title(title_tag)

xlocs = list(range(-180,181,30))
#xlocs = list(range(10*int(lonmin/10), 10*int(lonmax/10), 10))

if ((latmax - latmin) < 30):
  mean = (latmax + latmin)/2.
  ax.set_extent((-180, 180, min(90, mean + 30), max(-90, mean - 30)), crs= proj )
  ylocs = list(range(int(max(-90, mean-30)), int(min(90, mean + 30) ), 5))
else:
  ylocs = list(range(-90, 91, 15))

ax.gridlines(crs=ccrs.PlateCarree(), xlocs=xlocs, ylocs=ylocs )
# not on hera: ax.coastlines()
ax.add_feature(cfeature.GSHHSFeature(levels=[1,2], scale="c") )
if markersize < 12:
    alpha = 1
else:
    alpha = 0.2/25

plt.scatter(lon, lat, transform=ccrs.PlateCarree(), s = markersize, alpha = alpha)
plt.savefig("ll_errs_"+title_tag+".png")
plt.close()

#debug: print(markersize)
