#!/bin/bash
cd ..
cd testCasesExecutables
for d in testCasesExecutables; do
  python *.py "$d"
done
