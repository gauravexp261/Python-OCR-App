import logging

def setup_logger(name, level=logging.DEBUG):

    logger = logging.getLogger(name)

    logger.setLevel(level)

    file_handler = logging.FileHandler(f"{name}.log")

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger