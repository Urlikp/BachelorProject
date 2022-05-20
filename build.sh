#!/bin/bash

PARAMETER=0
ALL_RANDOM=0
HELP="Usage: $0 [OPTIONS]

$(basename "$0") is a script that runs my implementation of Tutte embedding using OpenGL and Python. Default
implementation tries to find any face and designate it as main face, then it generates starting random coordinates for
all nodes but those, that are part of the main face.

OpenGL application controls:
    f - start the animation
    esc - exit the application

Options:
    -h  Print help and exit script
    -a  Generate starting random coordinates for all nodes
    -f <prefix>
        Choose custom main face, it should be in form: \"node_1,node_2,...,node_n\", for eample: \"0,1,5,4\""

while getopts ":haf:" OPT
do
  case ${OPT} in
  h)
    echo "$HELP"
    exit 0
    ;;
  a)
    ALL_RANDOM=1
    ;;
  f)
    FACE="${OPTARG}"
    PARAMETER=1
    ;;
  ?)
    echo "$HELP"
    exit 1
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
