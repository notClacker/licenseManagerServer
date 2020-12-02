#!/bin/env bash

Filename="tmmp_tmp_db_table.txt"
Tmp="some_tmp_file.txt"
echo "Result in file $Filename"

touch $Filename &&
sqlite3 user_db.sql "select * from users_licenses" > $Filename &&
sed -e 's/|/\t/g' $Filename > $Tmp &&
cat $Tmp &&
rm $Filename &&
rm $Tmp
