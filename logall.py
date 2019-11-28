#########################################################
# Script for record logs for all the operations         #
#                                                       #
# Authors : Ajinkya                                     #
# Last Modified : 12/03/2018                            #
#########################################################

import logging
# Basic config for logging
logging.basicConfig(level = logging.DEBUG)

#Create a custom logger
logger = logging.getLogger()

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')
c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

def loginfo(x):
	return logger.info(x)