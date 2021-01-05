import sys
from database import *

VALIDATORS_CNT = 2      # how many validators do you have
EXPECTED_REWARD = 48000 # what's your expected reward for each of them (Gwei)
ALARM_THRESHOLD = 0.95  # if you receive less than this (%) prints out the epoch

with db_session:
    max_epoch = max(s.epoch for s in Stats)
epoch_start = max_epoch - 1
epoch_limit = int(sys.argv[1]) if len(sys.argv) > 1 else 1


@db_session
def get_reward(start, limit):
    return list(select((s.epoch, sum(s.earn)) for s in Stats
                       if s.epoch <= start and s.epoch > start - limit and s.earn))


if __name__ == "__main__":
    r = dict(get_reward(epoch_start, epoch_limit))
    at_least = EXPECTED_REWARD * VALIDATORS_CNT * ALARM_THRESHOLD
    for epoch in range(epoch_start, epoch_start - epoch_limit, -1):
        if r[epoch] <= at_least:
            print ("Epoch: %d Reward: %d (expecting at least %d)" % (epoch, r[epoch], at_least))
   
        
