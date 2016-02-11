#!/bin/bash

cd caffe
if [ ! -d "build" ]; then
	mkdir build
fi

cd build
cmake ../ -Dpython_version=2
make -j8
cd ../..

cd bell2014/krahenbuhl2013/
make -j8

