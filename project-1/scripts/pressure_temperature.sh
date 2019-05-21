
if [[ "$#" -ne 2 ]]; then
    echo "Usage: $0 <log filename> <lammps script>"
    exit
fi

for temperature in 2 5 10 15 20 25 30; do
    mpirun -np $NUM_MPI_PROCESSES \
        lmp -var temperature $temperature \
            -var filename "$1"_$temperature.log \
            -in $2
done
