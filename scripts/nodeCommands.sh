#!/bin/bash

for container in `docker ps | awk ' NF>1{print $NF} ' | grep node`
do
    docker exec $container $*
done

