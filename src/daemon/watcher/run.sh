#!/bin/bash

if [ "$USE_DEV_MODE" = "true" ]; 
    then nodemon --exec go run main.go;
    else go run main.go;
fi
