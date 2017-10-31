#!/usr/bin/env python

cd ../testCases
for currentFile in *; do 
	COUNTER=1
	if [ $(eval "pwd") != "/home/austinhunt/Desktop/TestAutomation/testCases" ]; then
		cd ../testCases
	fi 

	while IFS= read -r line
	do
		
		if [ "$COUNTER" -eq 1 ]; then
			testCaseNum=$line
			echo TEST CASE $testCaseNum
		fi	

		if [ "$COUNTER" -eq 5 ]; then
			
			
			cd ../testCasesExecutables
			python testCase$testCaseNum.py $line
		fi

		COUNTER=$((COUNTER+1))
 
	done < "$currentFile"

done
