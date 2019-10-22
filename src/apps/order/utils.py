import uuid
from random import random


def generate_ordering_no(seeds=0):
    """
        The method is to generate a unique ordering no.
        :param int seeds: the seed to calculate the end of the ordering_no
        :rtype str
    """
    if not seeds:
        seeds = random.randint(1, 9999)
    unique_key = str(uuid.uuid1())
    tmp = int("{0}{1}".format(unique_key[0:8], unique_key[19:23]), 16) * 987
    if seeds <= 9999:
        return "{0:0<15}{1:0>4}".format(str(tmp)[0:15], seeds)
    else:
        return "{0:0<15}{1:0>4}".format(str(tmp)[0:15], str(seeds)[0:4])
