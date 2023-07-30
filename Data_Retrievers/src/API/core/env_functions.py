# core/env_functions.py
import os
from ast import literal_eval
from dotenv import load_dotenv
from pathlib import Path


"""
Env functions which loads env data into the system.
Do note that this is specifically designed to avoid hardcoding Service Keys 
or Server Data into code.

Make sure than git is not tracking any files with the .env extension
"""

def get_dotenv(env_name):
  env_dir = Path(__file__).resolve().parents[1]
  env_path = Path(env_dir)/f"{env_name}"

  if env_path.exists():
    load_dotenv(dotenv_path=env_path)

def get_env_variable(var_name):
    """Get environment variable from os"""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Set the {var_name} environment variable"
        raise AttributeError(error_msg)

def get_env_variable_list(var_name):
    try:
        return literal_eval(os.environ[var_name])
    except:
        error_msg = f"Something wrong at env_list"
        raise AttributeError(error_msg)