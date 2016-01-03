#
# Regular cron jobs for the generic-mqtt-client package
#
0 4	* * *	root	[ -x /usr/bin/generic-mqtt-client_maintenance ] && /usr/bin/generic-mqtt-client_maintenance
