#! /usr/bin/env bash

for foldername in VE/*/; do
	./csv_union_finder_top2.py "$foldername" "$foldername"/VoxelValues*.csv
done