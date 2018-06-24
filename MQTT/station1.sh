#!/bin/bash
rm encrypted*
rm pubfile_*
rm Station1_sub
rm Station2_sub
echo "Removed all files"
python station1.py
