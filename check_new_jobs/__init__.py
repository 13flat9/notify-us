import logging
import azure.functions as func
from . import check_for_new

def configure_logging() -> None:
    logger = logging.getLogger() # no argument -> root level settings
    logger.setLevel(logging.DEBUG) # lowest level of logging

def main(mytimer: func.TimerRequest) -> None:

    configure_logging()
    logger = logging.getLogger(__name__) # here: __name__ == "__app__.check_new_jobs" 
    #               Inside module check_for_new: __name__ == "__app__.check_new_jobs.check_for_new"

    try:
        check_for_new.main()
    except Exception as e:
        logger.critical("Error somewhere in main function." ,exc_info=True)
        raise

    if mytimer.past_due:
        logger.info('The timer is past due!')
