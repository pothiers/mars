#!/usr/bin/env bash


function usage {
    echo "Usage: $0 path/to/location/of/webpackjs"
}

args=("$@")

len=${#args[@]}
if [ $len -ne 1 ];then
    usage
    exit
fi

projpath="${args[0]}"
binpath=$(npm bin)
curpath="$(pwd)"
cd $projpath
$binpath/webpack -w
cd $curpath
