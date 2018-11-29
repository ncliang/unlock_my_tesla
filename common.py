class UnlockException(Exception):
    pass


def make_request(callable, callable_args=None):
    if not callable_args:
        callable_args = {}

    resp = callable(**callable_args)
    if not resp:
        return None

    if 'error' in resp:
        raise UnlockException(resp['error'])
    return resp['response']
