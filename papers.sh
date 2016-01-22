#!/bin/bash          
python $PAPERSWEB/papersWeb.py > $PAPERSWEB/papersWeb.html
open -a Safari $PAPERSWEB/papersWeb.html
