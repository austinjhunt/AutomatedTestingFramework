#!/bin/sh

ls > $1
echo "" > $2
echo "<!DOCTYPE html>" >> $2
echo "<html>" >>$2 
echo "<h1> Top-Level Directory Contents </h1>" >> $2
echo "<body>" >> $2
while read -r line
do 
	echo "<p> $line </p> " >> $2

done < $1

echo"</body>" >> $2
echo "</html>" >> $2 

xdg-open $2

echo "script finished" 

exit 0  
