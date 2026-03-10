from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging

logger = logging.getLogger("anyida_scraper")

def retry_request(max_attempts=3, min_wait=1, max_wait=10):
    """
    Decorator for retrying functions with exponential backoff.
    """
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=min_wait, min=min_wait, max=max_wait),
        retry=retry_if_exception_type(Exception),
        before_sleep=lambda retry_state: logger.warning(
            f"Retrying {retry_state.fn.__name__} after error: {retry_state.outcome.exception()}"
        )
    )
