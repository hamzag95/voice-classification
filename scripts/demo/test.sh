#!/bin/bash

sox -d $1.wav rate 16k silence 1 0.1 3% 1 3.0 3%
mkdir -p ./test/$1
mv $1.wav ./test/$1

ffmpeg -i ./test/$1/$1.wav -f segment -segment_time 5 -c copy ./test/$1/out%03d.wav

rm ./test/$1/$1.wav

for file in ./test/$1/*.wav
do
    outfile=${file%.*}
	sox "$file" ${outfile}.r.wav remix 2
	sox "$file" ${outfile}.l.wav remix 1
    sox -m ${outfile}.l.wav ${outfile}.r.wav ${outfile}.mono.wav
	sox ${outfile}.mono.wav -n spectrogram -r -o ${outfile}.mono.png
	rm ${outfile}.l.wav ${outfile}.r.wav ${outfile}.mono.wav
done
