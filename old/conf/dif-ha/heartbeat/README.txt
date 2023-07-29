
Introduction
------------

The conf/dif-ha/heartbeat directory within the DIF distribution contains files
and scripts that can be used to setup a HA DIF deployment based upon simple IP
fail-over using Linux Heartbeat.

The suggested setup allows for a 2 node ACTIVE/PASSIVE cluster on two servers.

This will make use of three IP address. Here is an example for purely
illustrative purposes:

    Hostname          | IP Address    | Description
    ------------------+---------------+--------------------------------
    dif.example.com   | 100.200.230.1 | Virtual IP, not a physical node
    dif1.example.com  | 100.200.230.2 | DIF Server Node 1
    dif2.example.com  | 100.200.230.3 | DIF Server Node 2

100.200.230.2 & 100.200.230.3 (the IP's our two heartbeat nodes will be
using to communicate with each other over our Local Area Network, these
may be public(WAN) or private(LAN) addresses. Each of these two nodes should
preferably be on the same subnet but all that is needed is that each node
is able to communicate with the other/vice versa.) 

100.200.230.1 (our VIRTUAL IP Address that the two node's will "share" &
monitor/bring alive if one node should stop communicating). This IP Address
may be on ANY subnet.

Linux Heartbeat will then monitor that the DIF is running and that the floating
IP address is assigned to the node upon which it is executing.

Installation
------------

   1, Install Linux Heartbeat onto both DIF servers

      Redhat Linux :  yum install heartbeat

   2, The following configuration files from the directory conf/dif-ha/heartbeat should be
      copied to the /etc/ha.d directory on both of the DIF servers:

          - ha.cf
          - haresources
          - authkeys

      The permissions on the authkeys file must be set to 0600 and it must
      be owned by root. 

   3, Edit the file /etc/ha.d/ha.cf :

          debugfile /var/log/ha-debug
          logfile	/var/log/ha-log
          logfacility	local0

          udpport 694
          bcast eth0
          keepalive 1	               # Heartbeat interval 1 sec
          warntime 3	               # Log late heartbeat after 3 secs
          deadtime 5	               # Node is dead after 5 secs
          initdead 10	               # Post reboot dead time.
          crm no		               # Use pacemaker
          auto_failback off
          max_rexmit_delay 10000
          hbgenmethod time 

          node dif1.example.com        # DIF Node 1
          node dif2.example.com        # DIF Node 2

          ping 10.7.3.1	               # Ping a switch or router
          deadping 3	               # DEADPING MUST BE LESS THAN DEADTIME
          respawn hacluster /usr/lib/heartbeat/dopd
          apiauth dopd gid=haclient uid=hacluster

      Change the following lines:


	      ping 10.7.3.1          # Ping a switch or router
	      bcase eth0
	      node dif1.example.com  # DIF Node 1
	      node dif2.example.com  # DIF Node 2


      So that the IP address for the ping parameter is one of the local
      network switches, and that the two node line correspond to the names
      of the two DIF machines.

   4, Edit the file /etc/ha.d/haresources

	    dif1.example.com IPaddr::100.200.230.1/24 dif

      And change hobnob to be the name of the primary DIF machine, and
      change the IP address 100.200.230.1 to be the desired virtual IP
      address of the DIF instance. 

   5, Copy the DIF service file conf/dif-ha/heartbeat/dif-initd to /etc/init.d/ 
      renaming it to 'dif', i.e.
   
        prompt# cp conf/dif-ha/heartbeat/dif-initd /etc/init.d/dif

   6, Edit /etc/init.d/dif service file to edit the following variables
      if required:

        # Full path the the script that starts the DIF
        DIF=/opt/engine/bin/start-dif.sh

        # Name of the application
        DIF_EXE_NAME=dif

        # Name and location of the DIF PID File
        DIF_PID_FILE=/var/run/dif.pid

        # Name and location of the DIF Halt File
        DIF_HALT_FILE=/var/run/dif.halt

        # DIF command port number (Default = 62345)
        DIF_COMMAND_PORT=62345

   7, Ensure the the DIF service file is executable
   
        prompt# chmod +x /etc/init.d/dif
        
   8, Copy the DIF start script conf/dif-ha/heartbeat/start-dif.sh to engine bin directory
      and make it executable:
      
        prompt# cp conf/dif-ha/heartbeat/start-dif.sh /opt/engine/bin
        prompt# chmod +x /opt/engine/bin/start0-dif.sh
      
   9, Configure Services to Run at Boot

      The heartbeat and should run automatically, but the dif service should
      not since it is controlled by the heartbeat service:


	     prompt# chkconfig heartbeat on
	     prompt# chkconfig dif off
	
      These commands should be repeated on the the secondary DIF node.


