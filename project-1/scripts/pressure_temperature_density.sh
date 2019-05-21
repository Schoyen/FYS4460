
if [[ "$#" -ne 2 ]]; then
    echo "Usage: $0 <log filename> <lammps script>"
    exit
fi


for length in 10 12 14 16 18 20; do
    for temperature in 2 5 10 15 20 25 30; do
        mpirun -np $NUM_MPI_PROCESSES \
            lmp -var L $length \
                -var temperature $temperature \
                -var filename "$1"_"$length"_"$temperature" \
                -in $2
    done
done
