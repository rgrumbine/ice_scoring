FILENAME=`basename $1`
echo $FILENAME

#newer:
#temp_url_sig=2f667145b90e0ee49d98cc2854991bd40d3c1a36&temp_url_expires=1855560279&temp_url_prefix=incoming/ncep001

#older:
#temp_url_sig=cab288972e3d9378912b8d2c66c0d4f5fb346ca32&temp_url_expires=1496134511&temp_url_prefix=incoming/test001/

#curl -XPUT "https://swift.dkrz.de/v1/dkrz_0262ea1f00e34439850f3f1d71817205/SIDFEx/incoming/ncep001/$FILENAME?$sig" --data-binary @$FILENAME

curl -XPUT "https://swift.dkrz.de/v1/dkrz_0262ea1f00e34439850f3f1d71817205/SIDFEx/incoming/ncep001/$FILENAME?temp_url_sig=2f667145b90e0ee49d98cc2854991bd40d3c1a36&temp_url_expires=1855560279&temp_url_prefix=incoming/ncep001" \
--data-binary @$FILENAME
