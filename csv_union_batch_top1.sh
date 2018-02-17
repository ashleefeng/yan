#! /usr/bin/env bash

for foldername in VE/*/; do
	./csv_union_finder_top1.py "$foldername" "$foldername"/VoxelValues*.csv
done