#!/bin/sh
#$1 is the file name $2 is the method name 
cd ../testCaseExecutables

echo "" > tempMethodBody.txt
currentPath="$(eval pwd)" 
executableFile=$currentPath/$2.py
chmod +x $executableFile
methodBodyFile=$currentPath/tempMethodBody.txt

cd .. #in Test automation here
cd ../250src/main


#fileWithMethods="$(currentPath)/$1.py"
ls

echo "$2"

cat $1.py | awk "/def $2/,/NEW_FUNCTION/" > $methodBodyFile	#get method body of $2 (method name) 

cd .. #main -> 250
cd .. #250 -> Yeet
cd TestAutomation/testCaseExecutables

 echo HELLO 
#

remaining=$(sed -i "/TESTMETHOD/,/#/ d" $executableFile)

echo WHAT IS UP
echo $remaining

#cd .. 
#cd ../TestAutomation/testCaseExecutables
#echo $PWD

#executableFile="$2.py" #navigate to executable file
#want to overwrite the method definition that is there currently 

#sed -i 's/^[^def main]*def main/def main/' $executableFile




