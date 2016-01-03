all:
	true

install:
	install -m 755 -d $(DESTDIR)/lib/systemd/system
	install -m 644 generic-mqtt-client@.service $(DESTDIR)/lib/systemd/system
	install -m 755 -d $(DESTDIR)/usr/bin/
	install -m 755 generic-mqtt-client.py $(DESTDIR)/usr/bin/
	install -m 755 -d $(DESTDIR)/usr/share/lipstick/notificationcategories/
	install -m 644 x-nemo.messaging.mqtt.conf $(DESTDIR)/usr/share/lipstick/notificationcategories/
