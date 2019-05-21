
for i in $(seq 2 5); do
    echo For i = $i we get dt = $(python -c "print('%f' % 10 ** (-$i))")
    echo $(python -c "print(__import__('math').ceil(10 / 10 ** (-$i)))")
    mpirun -np $NUM_MPI_PROCESSES lmp \
        -var timestep $(python -c "print('%f' % 10 ** (-$i))") \
        -var filename $DAT_PATH/"$ENERGY_FILENAME"_$i$LOG_EXTENSION \
        -var num_steps $(python -c "print(__import__('math').ceil(10 / 10 ** (-$i)))") \
        < $ENERGY_SCRIPT
done
