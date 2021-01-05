import sys
from datetime import datetime
from database import *

with db_session:
    max_epoch = max(s.epoch for s in Stats)
epoch_start = max_epoch - 1
epoch_limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10


@db_session
def get_summary(start, limit):
    return list(select((s.earn // 1000, count(s)) for s in Stats
                       if s.epoch <= start and s.epoch > start - limit and s.earn))


@db_session
def get_summary_div_32(start, limit):
    return list(select((s.earn // 1000, count(s)) for s in Stats
                       if s.epoch <= start and s.epoch > start - limit and s.earn
                       and s.validator in select((s2.validator) for s2 in Stats
                                                 if s2.epoch == s.epoch - 2 and s2.validator == s.validator and
                                                 (s2.att_slot % 32 == 0 or s2.inc_slot % 32 == 0))))


@db_session
def get_details(epoch, min_earn, max_earn):
    return list(select(s for s in Stats
                       if s.epoch == epoch and s.earn and
                       s.earn >= min_earn and s.earn <= max_earn).order_by(Stats.validator))

@db_session
def get_reward(start, limit):
    return list(select((s.epoch, sum(s.earn)) for s in Stats
                       if s.epoch <= start and s.epoch > start - limit and s.earn))

def print_summary(summary1, summary2):
    total = sum([s[1] for s in summary1])
    summary2 = dict(summary2)
    print ("Reward Count Percent C32    P32")
    for s in summary1:
        c32 = summary2.get(s[0], 0)
        p32 = c32 / s[1] * 100
        print('{:>3}k {:>5} {:>6.1f}% {:>3} {:>5.1f}%'.format(s[0], s[1], s[1] / total * 100, c32, p32))



def print_details(stats):
    for s in stats:
        print("\t%d [https://beaconcha.in/validator/%s]" %
              (s.earn, s.validator))


if __name__ == "__main__":
    r = dict(get_reward(epoch_start, epoch_limit))
    s1 = get_summary(epoch_start, epoch_limit)
    s2 = get_summary_div_32(epoch_start, epoch_limit)
    print_summary(s1, s2)
    
    print("Total reward %.4f ETH" % (sum(r.values()) / 1000000000))
    for epoch in range(epoch_start, epoch_start - epoch_limit, -1):
        print("Epoch %d reward %.2f Zwei" % (epoch, r[epoch] / 1000000))

        stats = get_details(epoch, -99999, 45000)
        if stats:
            print_details(stats)
        
