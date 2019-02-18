#!/usr/bin/bash
export OMP_NUM_THREADS=4

for i in $(seq 2 5); do
    echo For i = $i we get dt = $(python -c "print('%f' % 10 ** (-$i))")
    ~/lammps/build/lmp \
        -var timestep $(python -c "print('%f' % 10 ** (-$i))") \
        -var filename thermo_$i.log \
        < energy.conf
done
