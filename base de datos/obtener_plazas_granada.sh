#!/usr/bin/env bash

wget http://www.movilidadgranada.com/kml/pmr201705.kmz
unzip pmr201705.kmz
rm pmr201705.kmz
rm 60cfcc09-9b19-465f-a007-0a74e6905879.png
python3 parser_plazas.py > plazas.csv
rm doc.kml
#head -n6 plazas.csv > plazas2.csv #comentar para dar de alta todas las plazas
if [ -f plazas2.csv ]; then
  rm plazas.csv
  mv plazas2.csv plazas.csv
fi
python3 poblar_bd.py
rm plazas.csv
