import logging
from logging import Formatter
import os
from pytz import timezone
from datetime import datetime
from pathlib import Path

class Log():

    def __init__(self):

        # loggerオブジェクトの宣言
        self.logger = logging.getLogger(__name__)

        # loggerのログレベル設定
        self.logger.setLevel(logging.DEBUG)

        logging.Formatter.converter = lambda *args: datetime.now(tz=timezone('Asia/Tokyo')).timetuple()
        # ログ出力フォーマット設定
        self.handler_format = Formatter('%(asctime)s - %(levelname)s - %(message)s')

        root_path = os.environ['file_directory']
        log_path ='logs/'

        self.logs_directory = root_path + log_path

        if os.path.exists(self.logs_directory) == False:
            os.makedirs(name=self.logs_directory, mode=0o777, exist_ok=True)

    def error_log(self,message:str):

        error_log_file = self.logs_directory + "error.log"

        if os.path.isfile(error_log_file) == False:
            Path(error_log_file).touch()
        
        # FileHandlerの設定
        file_handler = logging.FileHandler(error_log_file)

        # FileHandlerにログ出力フォーマット設定
        file_handler.setFormatter(self.handler_format)

        # loggerにfile_handlerの設定適用
        self.logger.addHandler(file_handler)
        
        self.logger.error(message)



    def user_login_log(self,message):

        user_folder = self.logs_directory + "user/"

        if os.path.exists(user_folder) == False:
            os.makedirs(name=user_folder, mode=0o777, exist_ok=True)

        admin_login_file = user_folder + "login.log"

        if os.path.isfile(admin_login_file) == False:
            Path(admin_login_file).touch()
        
        file_handler = logging.FileHandler(admin_login_file)
        file_handler.setFormatter(self.handler_format)
        self.logger.addHandler(file_handler)
        self.logger.debug(message)