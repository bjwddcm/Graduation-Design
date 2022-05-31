#!/bin/bash

sudo kill -9 `ps -elf|grep mjpg |awk '{print $4}'|awk 'NR==1'`

sudo kill -9 `ps -elf|grep mjpg |awk '{print $4}'|awk 'NR==1'`

sudo kill -9 `ps -elf|grep z_main |awk '{print $4}'|awk 'NR==1'`

sudo kill -9 `ps -elf|grep z_main |awk '{print $4}'|awk 'NR==1'`