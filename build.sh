#!/bin/bash

CC=g++
LDFLAGS=$(pkg-config --libs glew)
LDFLAGS="$LDFLAGS -lglut"

$CC main.cpp "$LDFLAGS" -o main
