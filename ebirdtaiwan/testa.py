# setup logger
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(name)s - %(asctime)s - %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    filename='DataPipeline.log'
)
logger = logging.getLogger('Automation')


if __name__ == '__main__':
    n = 0
    while n < 20:    
	    logger.info(f'test 333{n}')
	    n += 1
	    time.sleep(2)
