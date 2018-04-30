#!/bin/bash

CORRECT_OUTPUT="correct_output.dat"
CORRECT_TOP="correct_output.top"
OUTPUT_CONF="init_lammps.dat.oxdna"
OUTPUT_TOP="init_lammps.dat.top"

if [ ! -s init_lammps.dat ] 
then
	echo "Can't find input file. Are you sure you are in the right folder?"
	exit 1
fi

rm $OUTPUT_CONF $OUTPUT_TOP 2> /dev/null
python ../../src/lammps-to-oxDNA.py init_lammps.dat
(diff $CORRECT_OUTPUT $OUTPUT_CONF) && (diff $CORRECT_TOP $OUTPUT_TOP)

if [ $? -ne 0 ]
then
	echo "TEST FAILED";
	exit 1
else
	echo "TEST PASSED";
	exit 0
fi 
