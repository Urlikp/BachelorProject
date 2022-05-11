#!/bin/bash

cp -v input_graph.txt Python/
(
  cd Python/ || exit
  python3 project.py
  cp -v input_representation.txt ..
)
cp -v input_graph.txt input_representation.txt OpenGL/
(
  cd OpenGL/ || exit
  cmake .
  make
  ./project
)
