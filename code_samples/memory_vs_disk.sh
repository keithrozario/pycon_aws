#!/usr/bin/env bash

sls invoke -f copy -d "{\"key\": \"100.txt\", \"iter\": 5, \"using\": \"memory\"}"
sls invoke -f copy -d "{\"key\": \"100.txt\", \"iter\": 5, \"using\": \"disk\"}"


sls invoke -f copy_big -d "{\"key\": \"1024.txt\", \"iter\": 1, \"using\": \"memory\"}"