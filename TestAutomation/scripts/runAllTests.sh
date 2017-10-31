#!/bin/bash
cd ..
cd testCasesExecutables

for d in testCasesExecutables/*/all; do
  python *.py "$d"
done
