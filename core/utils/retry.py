from tenacity import retry, stop_after_attempt, wait_fixed

def retryable(attempts: int = 2, wait_seconds: int = 1):
    return retry(stop=stop_after_attempt(attempts), wait=wait_fixed(wait_seconds))
