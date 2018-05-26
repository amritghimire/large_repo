#!/usr/bin/env python3
import sys, json
import random

VERSION = 39


import yaml

def get_in(value, path):
    for k in path:
        try:
            value = value[k]
        except:
            return None
    return value

used_params = [{'params.yaml': ['train.min_split',
                  'model.random_state',
                  'variables.sample',
                  'model.max_depth',
                  'model.split',
                  'train.estimators',
                  'model.ngrams',
                  'train.min_features',
                  'model.threads',
                  'validation.learning_rate',
                  'variables.num_est',
                  'variables.min_split',
                  'model.max_features',
                  'validation.weight_factor',
                  'model.num_est',
                  'validation.seed',
                  'variables.columns',
                  'train.max_features',
                  'validation.features',
                  'model.folds',
                  'variables.weight_factor',
                  'train.columns',
                  'variables.features',
                  'model.passes',
                  'validation.ngrams',
                  'validation.min_split',
                  'train.threads']}]

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

# Comment to update:6374425