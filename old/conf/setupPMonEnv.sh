if [ "$LD_LIBRARY_PATH" == "" ]
then
    echo "Empty shared library path"
    export LD_LIBRARY_PATH=../../../common-utils/source
else
    echo "Shared library path is $LD_LIBRARY_PATH"
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:../../../common-utils/source
fi

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:../../../third-party/snmp++/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:../../../ld-comms-proto/source
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:../../../ld-comms-client/source
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:../../config/source
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:../../packet-stats/source
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib

export DB_PRINT=0
export DLVL_pmon=0
export DB_MAXLOGSIZE=50MB
export DB_WRAP=20
export DLOG_pmon=./pmon.log
export DB_COMPDEBUG=1
export DCFG_pmon=./pmon_log.cfg
