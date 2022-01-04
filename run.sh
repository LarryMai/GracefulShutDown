#!/bin/bash

BUILD_ARCH={BUILD_ARCH}
cd /opt/graceful_shutdown
while true
do   
    dotnet ./$BUILD_ARCH/GracefulShutdown.dll 
done
