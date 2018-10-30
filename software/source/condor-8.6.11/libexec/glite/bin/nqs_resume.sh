#!/bin/bash

blahconffile="${GLITE_LOCATION:-/opt/glite}/etc/batch_gahp.config"
binpath=`grep nqs_binpath $blahconffile|grep -v \#|awk -F"=" '{ print $2}'|sed -e 's/ //g'|sed -e 's/\"//g'`

requested=`echo $1 | sed 's/^.*\///'`
${binpath}/qrls $requested >/dev/null 2>&1
