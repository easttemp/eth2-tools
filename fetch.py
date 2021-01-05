import requests
import time
from datetime import datetime
from database import *

VALIDATORS = ['11111', '22222']
MAX_BALANCES = 10

def get_validators():
    return VALIDATORS

def get_results(url):
    while True:
        req = requests.get(url=url)
        data = req.json()
        if 'status' not in data or data['status'] != 'OK':
            time.sleep(60)
        else:
            return data['data']

@db_session
def fetch_attestations(validators):
    step = 5
    for i in range(0, 20, step):
        v_str = ",".join(validators[i: i + step])
        print("Fetching attestations (%s)... " % v_str, end='')
        results = get_results('https://beaconcha.in/api/v1/validator/%s/attestations' % v_str)
        print ("DONE.")

        for r in results:
            s = Stats.get_or_create(epoch=r['epoch'], validator=r['validatorindex'])
            s.att_slot = int(r['attesterslot'])
            s.inc_slot = int(r['inclusionslot'])
            s.status = int(r['status'])
            s.comm_idx = int(r['committeeindex'])
            s.dist = int(r['inclusionslot']) - int(r['attesterslot'])
            s.update_on = datetime.now()
            db.commit()


@db_session
def fetch_balances(validators):
    for idx, validator in enumerate(validators):
        print("Fetching balance %s... " % validator, end='')
        results = get_results('https://beaconcha.in/api/v1/validator/%s/balancehistory' % (validator))
        print("DONE.")
       
        for i, r in enumerate(results):
            s = Stats.get_or_create(epoch=r['epoch'], validator=r['validatorindex'])
            s.balance = int(r['balance'])
            s.earn = int(r['balance']) - int(results[i + 1]['balance'])
            s.update_on = datetime.now()
            db.commit()

            if i >= MAX_BALANCES:
                break
        
        if idx % 5 == 0:
            # Throttle yourself
            print("Sleeping...")
            time.sleep(31)


if __name__ == "__main__":
    v = get_validators()
    fetch_attestations(v)
    fetch_balances(v)

