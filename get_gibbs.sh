#!/bin/bash

for i in stb.fe-hcp # cdd.* stb.fe-hcp stb.fe2o-tet stb.ni-fcc
do
	cd $i/
	mkdir -p data/
	for pp in {300..400..10}
	do
		python3 ../tools/get_gibbs.py "$pp.0"
		mv gibbs_vs_t.yaml data/"$pp"_gpa.yaml
	done
	# cp data/350_gpa.yaml gibbs_vs_t.yaml
	cd ../
done
