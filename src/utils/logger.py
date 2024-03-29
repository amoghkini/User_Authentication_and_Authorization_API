import logging
import logging.config



def config_root_logger(log_file: str) -> None:
    """
    Configures the root logger to write log messages to a specified file.

    Args:
        log_file (str): The path to the log file.

    Returns:
        None.

    Example usage:
        >>> config_root_logger('app.log')
    """
    
    formatter = "%(asctime)-15s" \
                "| %(levelname)-s " \
                "| %(filename)s " \
                "| %(funcName)s " \
                "| %(lineno)d " \
                "| %(message)s"

    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'root_formatter': {
                'format': formatter
            }
        },
        'handlers': {
            'log_file': {
                'class': 'logging.FileHandler',
                'level': 'DEBUG',
                'filename': log_file,
                'formatter': 'root_formatter',
            }
        },
        'loggers': {
            '': {
                'handlers': [
                    'log_file',
                ],
                'level': 'DEBUG',
                'propagate': True
            }
        }
    })
    
    '''
    # Can be used as backup if above code fails
    def initLoggingConfig():
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")
    '''
