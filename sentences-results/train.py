#!/usr/bin/env python3
import sys, json
import random

VERSION = 66


import yaml

def get_in(value, path):
    for k in path:
        try:
            value = value[k]
        except:
            return None
    return value

used_params = [{'params.yaml': ['tagging.learning_rate',
                  'settings.layers',
                  'settings.random_state',
                  'concurrent.columns',
                  'concurrent.tags',
                  'tagging.tags',
                  'tagging.epochs',
                  'settings.columns',
                  'tagging.sample',
                  'model.trees',
                  'model.estimators',
                  'concurrent.split',
                  'model.min_features',
                  'concurrent.random_state',
                  'settings.epochs',
                  'concurrent.dense',
                  'tagging.split',
                  'concurrent.estimators',
                  'model.num_est']}]

params_values = {}
for rec in used_params:
    for fname, pnames in rec.items():
        with open(fname, 'r') as fd:
            params = yaml.safe_load(fd)

        for name in pnames:
            params_values[f"{fname}:{name}"] = get_in(params, name.split("."))


def get_param_value(name, default=None):
    return next((v for k, v in params_values.items() if k.endswith("." + name)), default)

def set_random_seed():
    random.seed(get_param_value("seed", 1234))

# A train generic fake script, simply add train params and "work" to the data
assert len(sys.argv) == 3, "Expected argv: train.py in model"

with open(sys.argv[1]) as fd, open(sys.argv[2], "w") as model:
    data = json.load(fd)
    data["params"].update(params_values)
    data["work"].append(VERSION)
    json.dump(data, model)

# Comment to update:372462711537809090