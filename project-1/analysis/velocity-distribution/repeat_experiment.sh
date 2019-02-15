#!/usr/bin/bash

mkdir histograms

word='xyz'
for i in $(seq 1 10); do
    ~/lammps/build/lmp -var seed $RANDOM < uniform_dist.conf
    for j in $(seq 1 ${#word}); do
        mv vel_${word:j-1:1}.histo histograms/vel_${word:j-1:1}_$i.histo
    done
done
