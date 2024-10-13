
import logging
import time
import os

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler(os.path.join("/root/L2_NLP_pipeline_pytorch/log","%s.txt"%(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))))
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - "%(pathname)s", line %(lineno)d - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
 
logger.info("Start print log")
logger.debug("Do something")
logger.warning("Something maybe fail.")
logger.info("Finish")