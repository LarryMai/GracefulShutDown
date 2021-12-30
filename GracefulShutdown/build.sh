#!/bin/bash

BUILD_ARCH=build
GRACEFUL_SHUTDOWN=graceful_shutdown

rm -rf ./bin ./obj ./$BUILD_ARCH
dotnet build -c Release -o $BUILD_ARCH /nowarn:CS0618 /nowarn:CS8632 /nowarn:CS1998 
tar -zcvf $GRACEFUL_SHUTDOWN.$BUILD_ARCH.tar.gz ./$BUILD_ARCH
rm -rf ../$BUILD_ARCH
mv ./$GRACEFUL_SHUTDOWN.$BUILD_ARCH.tar.gz  ../

# begin to packgage 
cd ../


rm -rf ./$GRACEFUL_SHUTDOWN
mkdir  $GRACEFUL_SHUTDOWN
mv ./$GRACEFUL_SHUTDOWN.$BUILD_ARCH.tar.gz ./$GRACEFUL_SHUTDOWN
cp ./run.sh ./$GRACEFUL_SHUTDOWN
sed 's@{BUILD_ARCH}@'"$BUILD_ARCH"'@g' -i ./$GRACEFUL_SHUTDOWN/run.sh

cp ./deploy.py ./$GRACEFUL_SHUTDOWN
sed 's@{BUILD_ARCH}@'"$BUILD_ARCH"'@g' -i ./$GRACEFUL_SHUTDOWN/deploy.py

cp ./$GRACEFUL_SHUTDOWN.service ./$GRACEFUL_SHUTDOWN

# rm -rf ./$GRACEFUL_SHUTDOWN
