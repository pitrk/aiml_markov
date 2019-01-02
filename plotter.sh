#!/bin/bash
usage()
{
  echo "Usage: $0 data"
  echo "Plot will be saved in data.png"
}

if [ $# -eq 0 ]; then
  usage
  exit 1
fi


gnuplot <<EOF
    set term png;
    set output "$1.png"
    set yzeroaxis
    set xzeroaxis
    set xlabel "iteration"
    set ylabel "utilities"
    set yrange [-1.1:1.1]
    set key autotitle columnhead
    set key outside right center
    set key font ",6"
    N=`awk 'NR==1 {print NF}' $1`
    plot for [i=2:N] "$1" u 1:i w l lw 2 title columnhead(i) at end, for [i=2:N] "$1" u 1:i w l lw 2 title columnhead(i)
EOF
