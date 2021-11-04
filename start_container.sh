#!/bin/bash 
docker run --rm  -dt --cpus 0.25 --memory 10MB busybox sleep 500
docker run --rm -dt --cpus 0.35 --memory 20MB busybox sleep 500
