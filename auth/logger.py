import logging

auth_handler = logging.FileHandler('logs/auth.log')
auth_formatter = logging.Formatter('%(levelname)s:%(name)s-%(asctime)s-%(message)s')
auth_handler.setFormatter(auth_formatter)

auth_logger = logging.Logger(name='auth_logger', level=logging.INFO)
auth_logger.addHandler(auth_handler)
