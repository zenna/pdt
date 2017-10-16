"Funcs to search over hyperparameters"
import subprocess
import os
from wacacore.train.hyper import rand_product


def stringify(k, v):
  """Turn a key value into command line argument"""
  if v is True:
    return "--%s" % k
  elif v is False:
    return ""
  else:
    return "--%s=%s" % (k, v)


def make_batch_string(options):
  """Turn options into a string that can be passed on command line"""
  batch_string = [stringify(k, v) for k, v in options.items()]
  return batch_string

# Using Slurm #

def run_sbatch(file_path, options, bash_run_path=None):
  """Execute sbatch with options"""
  if bash_run_path is None:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    bash_run_path = os.path.join(dir_path, 'run.sh')
  run_str = ['sbatch', bash_run_path, file_path] + make_batch_string(options)
  print(run_str)
  subprocess.call(run_str)


def rand_sbatch_hyper_search(options, file_path, var_options_keys, nsamples,
                             prefix, nrepeats):
  """Randomized hyper parameter search locally without slurm"""
  rand_product(lambda options: run_sbatch(options, file_path),
               options, var_options_keys, nsamples, prefix, nrepeats)

# Local #


def run_local_batch(file_path, options, blocking=True):
  """Execute process with options"""
  run_str = ["python", file_path] + make_batch_string(options)
  print("Subprocess call:", run_str)
  if blocking:
    subprocess.call(run_str)
  else:
    subprocess.Popen(run_str)

def rand_local_hyper_search(file_path,
                            options,
                            var_options_keys,
                            nsamples,
                            prefix,
                            nrepeats,
                            blocking=True):
  """Randomized hyper parameter search on local machine"""
  rand_product(lambda options: run_local_batch(file_path, options),
               options, var_options_keys, nsamples, prefix, nrepeats)