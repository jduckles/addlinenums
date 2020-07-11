#!/bin/bash
app="addlinenums"
docker build -t ${app} .
docker run --restart always -d -p 56733:80 \
  --name=${app} \
  -v $PWD:/app ${app}
