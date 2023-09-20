#!/bin/bash

docker run --mount type=bind,source=$(pwd),target=/home/aconeil -p 8200:8200 diffmark:latest
