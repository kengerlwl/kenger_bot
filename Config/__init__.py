# coding=utf-8
import json
import os
import logging


def get_config(run_env=None):
    # 读取配置文件
    if run_env is None:
        run_env = 'production.para'
    if 'SERVICE_ENV' in os.environ:
        run_env = os.environ['SERVICE_ENV']
    config_path = '{}/{}.json'.format(os.path.split(os.path.abspath(__file__))[0], run_env)
    # print(config_path)
    # config_path = 'Config/para.json'
    if os.path.isfile(config_path):
        config_data = open(config_path, "r", encoding="utf-8").read()
        app_config = json.loads(config_data)  

        app_config["RUN_ENV"] = run_env
        return app_config
    else:
        logging.error("Config not exist")
        exit()


# config.py
class Config:
    
    SQLALCHEMY_DATABASE_URI = 'mysql://username:password@127.0.0.1/dbname'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key'  # 用于保护 session
    SESSION_TYPE = 'filesystem'     # 存储 session 的方式

    def __init__(self, run_env=None):
        app_config = get_config(run_env)
        self.SQLALCHEMY_DATABASE_URI = app_config["service"]['SQLALCHEMY_DATABASE_URI']
        self.SECRET_KEY = app_config["service"]['SECRET_KEY']
        self.SESSION_TYPE = app_config["service"]['SESSION_TYPE']
