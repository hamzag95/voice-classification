#!/bin/bash

for i in *.mp3; do lame --decode "$i" "`basename "$i" .mp3`".wav; done
