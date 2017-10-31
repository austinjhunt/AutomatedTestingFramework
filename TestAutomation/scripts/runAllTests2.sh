#!/usr/bin/env python

cd ../testCases
for currentFile in *; do 
	COUNTER=1
	if [ $(eval "pwd") != "/home/austinhunt/Desktop/TestAutomation/testCases" ]; then
		cd ../testCases
	fi 
	printf "\n"
	while IFS= read -r line
	do
		
		if [ "$COUNTER" -eq 1 ]; then
			testCaseNum=$line
			echo TEST CASE $testCaseNum
	
		fi	
			
		if [ "$COUNTER" -eq 2 ]; then
			reqToTest=$line
			echo $reqToTest
		
		fi

		if [ "$COUNTER" -eq 3 ]; then 

			echo Component: $line

		fi
			
		if [ "$COUNTER" -eq 5 ]; then
			
			args=$line
		fi
		
		if [ "$COUNTER" -eq 6 ]; then 
			
			oracle=$line
			echo Oracle: $oracle
			cd ../testCasesExecutables
			python testCase$testCaseNum.py $args "$oracle"


		fi
		COUNTER=$((COUNTER+1))
 
	done < "$currentFile"

done
