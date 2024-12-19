#!/bin/bash

name=$1
api=$2
mode=$3

command="pixi run \
--manifest-path ecoscope-workflows-${name}-workflow/pixi.toml \
--locked --environment test \
test-${api}-${mode}-mock-io --case month-grouper"

eval $command
