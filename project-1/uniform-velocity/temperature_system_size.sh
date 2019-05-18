export OMP_NUM_THREADS=4
num_mpi_threads=2

for box in $(seq 1 15); do
    mpirun -n $num_mpi_threads \
        lmp -var simbox $box \
        -var filename temperature_size_$box.log \
        < temperature_system_size.in
done