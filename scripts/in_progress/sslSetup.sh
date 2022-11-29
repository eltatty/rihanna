#!/bin/bash

newIP=$(tail -1 /etc/resolv.conf | awk ' {print $2} ' | tr -d '\n')

./keytool -genkeypair -keystore spdrm.jks -storepass spdrm123 -keypass spdrm123 -keyalg RSA -validity 3650 -alias spdrm-certificate -dname "cn=spdrmsecurity,o=BetaCAE,c=GR" -ext SAN=IP:$newIP

./keytool -export -alias spdrm-certificate -keystore spdrm.jks -rfc -file spdrm-cert.crt

./keytool -import -alias spdrm-certificate -file spdrm-cert.crt -keystore spdrm-client.jks

