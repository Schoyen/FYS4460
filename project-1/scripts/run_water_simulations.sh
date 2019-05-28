
export OMP_NUM_THREADS=4

for T in $(seq 1 10 301); do
    mpirun -np 4 lmp -var T $T -in scripts/water.in
done
