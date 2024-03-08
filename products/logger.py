import logging

products_formatter = logging.Formatter('%(levelname)s:%(name)s-%(asctime)s-%(message)s')
products_handler = logging.FileHandler('logs/products.log')
products_logger = logging.Logger(name='products_logger')

products_handler.setFormatter(products_formatter)

products_logger.addHandler(products_handler)