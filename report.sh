python3 report.py $1 \
    | awk 'BEGIN{print "<table>"} {print "<tr>";for(i=1;i<=NF;i++)print "<td align=right>" $i"</td>";print "</tr>"} END{print "</table>"}' \
    | mail -s "Validator Stats `date -Iminutes`"  -a 'Content-Type: text/html' to@gmail.com -r from@gmail.com