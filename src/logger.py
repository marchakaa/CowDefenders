import logging
import functools
import os
from datetime import datetime

class Logger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._setup_logger()
        return cls._instance
    
    @staticmethod
    def _setup_logger():
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        logger = logging.getLogger('GameLogger')
        logger.setLevel(logging.DEBUG)
        
        current_date = datetime.now().strftime('%Y-%m-%d')
        file_handler = logging.FileHandler(f'logs/game_{current_date}.log')
        file_handler.setLevel(logging.DEBUG)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(log_format)
        console_handler.setFormatter(log_format)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        Logger._instance = logger
    
    @classmethod
    def debug(cls, message):
        cls._instance.debug(message)
    
    @classmethod
    def info(cls, message):
        cls._instance.info(message)
    
    @classmethod
    def warning(cls, message):
        cls._instance.warning(message)
    
    @classmethod
    def error(cls, message):
        cls._instance.error(message)
    
    @classmethod
    def log_method(cls, level='info'):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                class_name = args[0].__class__.__name__ if args else ''
                method_name = func.__name__
                
                log_message = f"{class_name}.{method_name} called"
                if args[1:] or kwargs:
                    log_message += f" with args: {args[1:]}, kwargs: {kwargs}"
                getattr(cls._instance, level)(log_message)
                
                try:
                    result = func(*args, **kwargs)
                    getattr(cls._instance, level)(f"{class_name}.{method_name} completed successfully")
                    return result
                except Exception as e:
                    cls._instance.error(f"{class_name}.{method_name} failed with error: {str(e)}")
                    raise
            return wrapper
        return decorator
    
