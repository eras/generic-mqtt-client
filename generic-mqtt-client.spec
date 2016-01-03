Name:		generic-mqtt-client
Version:	0.1
Release:	1%{?dist}
Source:         %{name}-%{version}.tar.gz
Summary:	Generic MQTT client
Group:		miscellanous
License:	GPL
URL:		http://www.github.com/eras/generic-mqtt-client
BuildArch:      noarch
Requires:       python
Requires:       python-mosquitto
Requires:       dbus-python

%description

%prep
echo PREP
#%autosetup

%build
#%configure
echo BUILD
#make %{?_smp_mflags}

%install
echo INSTALL
%make_install

%files
/lib/systemd/system/generic-mqtt-client@.service
/usr/bin/generic-mqtt-client.py
/usr/share/lipstick/notificationcategories/x-nemo.messaging.mqtt.conf

%doc

%changelog
