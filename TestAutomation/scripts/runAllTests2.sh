#!/usr/bin/env python

cd ../reports

reportsPath="$(eval pwd)"

firstHalfHTML=$reportsPath/reportPartOne.html
appendHTML=$reportsPath/reportPartTwo.html


touch $appendHTML
echo "" > $appendHTML

cd ../testCases

for currentFile in *; do 
	COUNTER=1
	if ! echo "$PWD" | grep "testCases" ; then
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
			echo $component
	
		fi

		if [ "$COUNTER" -eq 4 ]; then
			
			if [ "$unit" != $line ]; then 
				echo "<tr style =\"height:1; border: 4.5px solid black\">" >> $appendHTML
				echo "<td></td>" >> $appendHTML
				echo "<td></td>" >> $appendHTML
				echo "<td></td>" >> $appendHTML
				echo "<td style=\"font-weight: bold; font-size: 14px\">NEW METHOD:</td>" >> $appendHTML
				echo "<td style=\"font-weight: bold; font-size: 14px; overflow-wrap: normal; overflow-x: scroll\">$line</td>" >> $appendHTML
				echo "<td></td>" >> $appendHTML
				echo "<td></td>" >> $appendHTML
				echo "<td></td>" >> $appendHTML
				echo "</tr>" >> $appendHTML
			fi 
			unit=$line
			echo $unit
		
		fi
			
		if [ "$COUNTER" -eq 5 ]; then
			
			args=$line
			echo "$args"
			
			
		fi
			echo $COUNTER
		if [ "$COUNTER" -eq 6 ]; then 
			
			oracle=$line
			echo Oracle: $oracle
			#need to be in scripts, run getmethodbody.sh to put the updated methodbody into its corresponding executable!
			
			cd ../scripts
			#pass in arguments 1 = $component and 2 = method name aka $unit
			sh getMethodBody.sh $component $unit
			cd ../testCaseExecutables
			#NOW execute driver
			python $unit.py "$args" "$oracle" > $reportsPath/tempTestOutput.txt	
			
			echo Hello!
			testOutput="$(cat $reportsPath/tempTestOutput.txt)"
			echo Test Output: $testOutput
			
			echo "<tr>" >> $appendHTML
			echo "<td>$testCaseNum</td>" >> $appendHTML
			echo "<td>$reqToTest</td>" >> $appendHTML
			echo "<td>$component</td>" >> $appendHTML
			echo "<td>$unit</td>" >> $appendHTML
			echo "<td>$args</td>" >> $appendHTML
			echo "<td>$oracle</td>" >> $appendHTML
			echo "<td>$testOutput</td>" >> $appendHTML
			
			if [ "$testOutput" = "$oracle" ]; then
				echo "<td style=\"font-weight:bold\"><font color = \"green\" size = \"5\">PASS!</font></td>" >> $appendHTML
			fi
			
			if [ "$testOutput" != "$oracle" ]; then
				echo "<td style=\"font-weight:bold\"><font color = \"red\" size = \"5\">FAIL!</font></td>" >> $appendHTML
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
rm $appendHTML
opSystem=$(eval 'uname')

xdg-open $testReport 
#open $testReport

