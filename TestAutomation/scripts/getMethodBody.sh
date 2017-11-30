#!/bin/sh
#$1 is the file name $2 is the method name 
cd ../testCaseExecutables
echo "" > tempMethodBody.txt
currentPath="$(eval pwd)" 
executableFile=$currentPath/$2.py
chmod +x $executableFile
methodBodyFile=$currentPath/tempMethodBody.txt
cd .. 
cd ../250src/main
echo "$2"
#get method body of $2 (method name) 
cat $1.py | awk "/def $2/,/NEW_FUNCTION/" > $methodBodyFile	
cd .. 
cd ..
cd TestAutomation/testCaseExecutables
pattern1="#TESTMETHOD"
pattern2="#MAIN"
#Empty the current method body from the executable file
sed -i "/$pattern1/,/$pattern2/{//!d;}" $executableFile
#Now insert contents of $methodBodyFile between the #TESTMETHOD and #MAIN tags of the $executableFile
sed -i "/$pattern1/r $methodBodyFile" $executableFile
#Now get rid of unnecessary #NEW_FUNCTION tag 
sed -i "s/#NEW_FUNCTION//g" $executableFile
#METHOD BODY HAS BEEN OVERWRITTEN WITH WHAT IS IN VIEWS.PY FILE!!! CONGRATULATIONS




