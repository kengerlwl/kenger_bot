import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, log_name="app service", log_level=logging.INFO):
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(log_level)
        
        # 避免重复添加 handler
        if not self.logger.handlers:
            log_dir = "logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            log_filename = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")
            file_handler = logging.FileHandler(log_filename, encoding='utf-8')
            console_handler = logging.StreamHandler()

            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s"
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

# 创建全局日志实例
logger = Logger().get_logger()
