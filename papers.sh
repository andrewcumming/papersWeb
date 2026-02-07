#!/bin/bash          
python3 $PAPERSWEB/papersWeb.py > $PAPERSWEB/papersWeb.html
open -a Safari $PAPERSWEB/papersWeb.html
