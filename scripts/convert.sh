#!/bin/bash

for file in *.wav
do
    outfile=${file%.*}
	sox "$file" ${outfile}.r.wav remix 2
	sox "$file" ${outfile}.l.wav remix 1
    sox -m ${outfile}.l.wav ${outfile}.r.wav ${outfile}.mono.wav
	sox ${outfile}.mono.wav -n spectrogram -r -o ${outfile}.mono.png
	rm ${outfile}.l.wav ${outfile}.r.wav ${outfile}.mono.wav
done