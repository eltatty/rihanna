FROM ubuntu:20.04

# Functional Packages
# && apt install git -y
RUN apt update -y && apt install munge -y && apt install vim -y && apt install build-essential -y && apt install wget -y && apt install mariadb-server -y 
RUN apt install sudo -y && apt install python3 python3-pip -y 

ARG DEBIAN_FRONTEND=noninteractive
RUN apt install slurmd slurm-client -y
RUN apt install openssh-server -y
# RUN apt update

# MPI
# RUN apt update -y && apt install libopenmpi-dev -y && pip3 install mpi4py

# Create User
RUN useradd -m admin -s /usr/bin/bash -d /home/admin && echo "admin:admin" | chpasswd && adduser admin sudo && echo "admin     ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# SSH
RUN mkdir /var/run/sshd
RUN echo 'root:root' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

#SSH and SLURM ports
EXPOSE 22 6817 6818 6819

WORKDIR /home/admin

COPY slurm.conf /etc/slurm-llnl/
COPY cgroup.conf /etc/slurm-llnl/
COPY docker-entrypoint.sh /etc/slurm-llnl/

ENTRYPOINT ["/etc/slurm-llnl/docker-entrypoint.sh"]
