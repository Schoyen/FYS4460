#!/usr/bin/bash
export OMP_NUM_THREADS=4

for i in $(seq 2 5); do
    echo For i = $i we get dt = $(python -c "print('%f' % 10 ** (-$i))")
    echo $(python -c "print(__import__('math').ceil(10 / 10 ** (-$i)))")
    ~/lammps/build/lmp \
        -var timestep $(python -c "print('%f' % 10 ** (-$i))") \
        -var filename thermo_$i.log \
        -var num_steps $(python -c "print(__import__('math').ceil(10 / 10 ** (-$i)))") \
        < energy.conf
done
