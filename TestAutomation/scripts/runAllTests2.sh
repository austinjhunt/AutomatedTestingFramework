#!/usr/bin/env python
import subprocess
reportsPath="/Users/austinhunt/Desktop/YEET/TestAutomation/reports"
firstHalfHTML=$reportsPath/reportPartOne.html
appendHTML=$reportsPath/reportPartTwo.html
echo "" > $appendHTML

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

			component=$line

		fi

		if [ "$COUNTER" -eq 4 ]; then

			unit=$line

		fi
			
		if [ "$COUNTER" -eq 5 ]; then
			
			args=$line
		fi
		
		if [ "$COUNTER" -eq 6 ]; then 
		
			oracle=$line
			echo Oracle: $oracle
			cd ../testCasesExecutables
			python $unit.py $args "$oracle" > $reportsPath/tempTestOutput.txt	
			testOutput="$(cat $reportsPath/tempTestOutput.txt)"
			
			
			echo "<tr>" >> $appendHTML
			echo "<td class=\"medium\">$testCaseNum</td>" >> $appendHTML
			echo "<td class=\"large\">$reqToTest</td>" >> $appendHTML
			echo "<td class=\"large\">$component</td>" >> $appendHTML
			echo "<td class=\"medium\">$unit</td>" >> $appendHTML
			echo "<td class=\"medium\">$args</td>" >> $appendHTML
			echo "<td class=\"large\">$oracle</td>" >> $appendHTML
			echo "<td class=\"large\">$testOutput</td>" >> $appendHTML
			
			if [ "$testOutput" == "$oracle" ]; then
				echo "<td class=\"reallysmall\">Pass!</td>" >> $appendHTML
			fi
			
			if [ "$testOutput" != "$oracle" ]; then
				echo "<td class=\"reallysmall\">Fail!</td>" >> $appendHTML
			fi
			
			
			echo "</tr>" >> $appendHTML			
			
			
		fi
		COUNTER=$((COUNTER+1))
 
	done < "$currentFile"
	
done
rm $reportsPath/tempTestOutput.txt


echo "</tbody> </table> </div> </section> </body> </html>" >> $appendHTML

testReport=$reportsPath/testReport.html
cat $firstHalfHTML $appendHTML > $testReport
cd ../reports
open testReport.html
