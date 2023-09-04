import logging
import azure.functions as func
from . import check_new_jobs


def configure_logging() -> None:
    logger = logging.getLogger()  # no argument -> root level settings
    logger.setLevel(logging.DEBUG)  # lowest level of logging


def main(mytimer: func.TimerRequest) -> None:
    configure_logging()
    # getLogger(__name__) works like this:
    # Here:                 __name__ == "__app__.check_new_jobs"
    # Inside check_for_new: __name__ == "__app__.check_new_jobs.check_for_new"
    logger = logging.getLogger(__name__)

    if mytimer.past_due:
        logger.info('The function was invoked past its due time.')

    try:
        check_new_jobs.main()
    except Exception as e:
        logger.critical("Error somewhere in main function.", exc_info=True)
        raise
