# eth2-tools

### Dependencies
- Python 3
- PonyORM

### Change parameters in:
  - alert.py
  - fetch.py (here you specify your validator(s) )



### Cron:

```bash
# fetches the data every 7 minutes and checks if there's an alert firing for the last epoch
*/7 * * * *     cd /path/to/eth2-tools/ && python3 fetch.py && python3 alert.py 1 | ifne mail -s "Alert Validator Earnings `date -Iminutes`"  to@gmail.com

# this will do a daily report on the last 220 epochs (you can also try 7300 220 which would mean, going back 220 epochs starting with epoch number 7300)
0 9 * * *       cd /path/to/eth2-tools/ && bash report.sh 220   
```
