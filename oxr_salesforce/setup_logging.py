import logging
import sys, os

def setup_logging(filename=None, mode='a', encoding='utf8', print_log_messages=True, level=logging.INFO):
    """
    Set up logging to log both into a file and console.
    Usage: 
    logger = setup_logging()
    logger.info(msg)
    ...
    """
    logger = logging.getLogger("")  # Use root logger   #  logging.getLogger(name) # or use a named one?
    # Clear previous handlers, if any
    if (logger.hasHandlers()):
        logger.handlers.clear()
    # Formatter
    formatter = logging.Formatter('{asctime} {levelname} {threadName} {module}:{funcName}:{lineno} {message}', style='{')

    # Handlers
    if filename is not None:
        os.makedirs(os.path.dirname(filename), exist_ok=True)# create folder if needed
        log_handler = logging.FileHandler(filename, mode=mode, encoding=encoding)
        logger.addHandler(log_handler)
        log_handler.setFormatter(formatter)
        log_handler.setLevel(level)
    if print_log_messages:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        stream_handler.setLevel(level)
    # Set level - pass all messages with level INFO or higher (WARNING, ERROR, CRITICAL)
    logger.setLevel(level)

    # Log uncaught exceptions
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception

    return logger