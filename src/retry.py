import time


def invoke_with_retry(chain, inputs, tries=3, wait=2):
    """Call chain.invoke, retrying on transient structured-output errors."""
    last_error = None
    for attempt in range(tries):
        try:
            return chain.invoke(inputs)
        except Exception as e:
            msg = str(e)
            if "PerDay" in msg:
                raise  # daily quota: retrying only wastes requests
            last_error = e
            time.sleep(wait * (attempt + 1))
    raise last_error