
if [[ "$#" -ne 2 ]]; then
    echo "Usage: $0 <log-filename> <lammps script>"
    exit;
fi


for box in $(seq 1 15); do
    mpirun -np $NUM_MPI_PROCESSES \
        lmp -var simbox $box \
        -var filename "$1"_$box.log \
        -in $2
done
