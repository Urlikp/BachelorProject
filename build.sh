#!/bin/bash

PARAMETER=0
ALL_RANDOM=0

while getopts ":af:" OPT
do
  case ${OPT} in
  a)
    ALL_RANDOM=1
    ;;
  f)
    FACE="${OPTARG}"
    PARAMETER=1
    ;;
  ?)
    break
    ;;
  esac
done

cp -v input_graph.txt Python/

(
  cd Python/ || exit

  if [ $PARAMETER -eq 1 ] && [ $ALL_RANDOM -eq 1 ]
  then
    python3 project.py "${FACE}" "all_random"
  elif [ $PARAMETER -eq 1 ]
  then
    python3 project.py "${FACE}"
  elif [ $ALL_RANDOM -eq 1 ]
  then
    python3 project.py "all_random"
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
