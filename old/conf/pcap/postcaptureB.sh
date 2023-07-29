#!/bin/sh

# compress it
gzip --fast $1

# move it on
mv $1.gz /opt/engine/pcap/pickupDiameter

# delete old files in pickup if networking has gone
# only needs to run once (run by postcaptureA)
#perl /opt/engine/pcap/tidyNifPcapDiameter.pl

