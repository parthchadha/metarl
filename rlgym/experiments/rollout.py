# from rllab.sampler.utils import rollout
from rllab.misc import special
import argparse
import joblib
import uuid
import os
import matplotlib.pyplot as plt
from utils import rollout

import numpy as np
import sys
# from rllab.env.base import MDP
from rllab.misc.resolve import load_class

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str,
                        help='path to the snapshot file')
    parser.add_argument('--max_length', type=int, default=1000,
                        help='Max length of rollout')
    parser.add_argument('--speedup', type=int, default=1,
                        help='Speedup')
    parser.add_argument('--loop', type=int, default=1,
                        help='# of loops')
    args = parser.parse_args()

    policy = None
    env = None
    while True:
        if ':' in args.file:
            # fetch file using ssh
            os.system("rsync -avrz %s /tmp/%s.pkl" % (args.file, filename))
            data = joblib.load("/tmp/%s.pkl" % filename)
            if policy:
                new_policy = data['policy']
                policy.set_param_values(new_policy.get_param_values())
                path = rollout(env, policy, max_path_length=args.max_length,
                               animated=True, speedup=args.speedup)
            else:
                policy = data['policy']
                env = data['env']
                path = rollout(env, policy, max_path_length=args.max_length,
                               animated=True, speedup=args.speedup)
        else:
            data = joblib.load(args.file)
            policy = data['policy']
            env = data['env']
            path = rollout(env, policy )
        break