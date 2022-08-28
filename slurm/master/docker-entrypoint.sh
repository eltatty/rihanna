#!/bin/bash
# Master
# Replace cores on slurm.conf for each node accordingly
 sudo sed -i "s/REPLACE_IT/CPUs=$(nproc)/g" /etc/slurm-llnl/slurm.conf

# Services to start
sudo service ssh start
sudo service munge start
sudo service slurmctld start

# Keep the containers running
tail -f /dev/null