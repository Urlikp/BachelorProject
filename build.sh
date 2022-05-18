#!/bin/bash

PARAMETER=0

while getopts ":f:" OPT
do
  case "${OPT}" in
  f)
    FACE="${OPTARG}"
    PARAMETER=1
    break
    ;;
  ?)
    break
    ;;
  esac
done

cp -v input_graph.txt Python/

(
  cd Python/ || exit

  if [ $PARAMETER -eq 1 ]
  then
    python3 project.py "${FACE}"
  else
    python3 project.py
  fi

  cp -v input_representation.txt input_random_representation.txt ..
)

cp -v input_graph.txt input_representation.txt input_random_representation.txt OpenGL/

(
  cd OpenGL/ || exit
  cmake .
  make
  ./project
)
