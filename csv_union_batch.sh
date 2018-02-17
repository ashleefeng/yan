#! /usr/bin/env bash

for foldername in VE/*/; do
	./csv_union_finder.py "$foldername" "$foldername"/VoxelValues*.csv
done