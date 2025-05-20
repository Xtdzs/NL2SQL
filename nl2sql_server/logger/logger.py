import logger
import os

class Logger:
    def __init__(self, name: str, log_to_file: bool = True, log_to_console: bool = False, log_file_path: str = None, log_level: str = "INFO"):
        self.name = name
        self.log_to_file = log_to_file
        self.logger = logger.get_logger(name)
        self.logger.setLevel(log_level)
        
        if log_to_file:
            if log_file_path is None:
                log_file_path = os.path.join(os.getcwd(), f"{name}.log")
            file_handler = logger.FileHandler(log_file_path)
            file_handler.setLevel(log_level)
            self.logger.addHandler(file_handler)
        if log_to_console:
            console_handler = logger.StreamHandler()
            console_handler.setLevel(log_level)
            self.logger.addHandler(console_handler)
        self.logger.info(f"Logger initialized for {name} with log level {log_level}")
        self.logger.info(f"Log file path: {log_file_path}")
        self.logger.info(f"Log to console: {log_to_console}")
        self.logger.info(f"Log to file: {log_to_file}")

    def log(self, message: str):
        level = self.logger.level
        if level == "DEBUG":
            self.logger.debug(message)
        elif level == "INFO":
            self.logger.info(message)
        elif level == "WARNING":
            self.logger.warning(message)
        elif level == "ERROR":
            self.logger.error(message)
        elif level == "CRITICAL":
            self.logger.critical(message)
        else:
            raise ValueError(f"Unknown log level: {level}")
        self.logger.info(message)  
        
    def set_log_level(self, log_level: str):
        self.logger.setLevel(log_level)
        self.logger.info(f"Log level changed to {log_level}")
        
    def get_log_level(self):
        return self.logger.level
    
    def get_log_file_path(self):
        return self.logger.handlers[0].baseFilename if self.log_to_file else None
    
    def get_log_to_console(self):
        return self.logger.handlers[1].stream if self.log_to_console else None
    
    def get_log_to_file(self):
        return self.logger.handlers[0].baseFilename if self.log_to_file else None
    
    def get_logger(self):
        return self.logger
    
    def close(self):
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)
        self.logger.info(f"Logger {self.name} closed")
        
        