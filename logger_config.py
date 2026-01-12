import logging

# Create and configure logger
logging.basicConfig(filename="mainApp.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)