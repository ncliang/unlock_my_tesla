import mock
import unittest

import unlock_my_tesla


class UnlockMyTeslaTest(unittest.TestCase):
    @mock.patch('time.sleep')
    def test_make_request_basic(self, patched_sleep):
        resp = unlock_my_tesla.make_request(lambda: {'response': 'ok!'})
        patched_sleep.assert_not_called()
        self.assertEqual('ok!', resp)

    @mock.patch('time.sleep')
    def test_make_request_errors(self, patched_sleep):
        try:
            unlock_my_tesla.make_request(lambda: {'error': 'no!'},
                                         max_attempts=2,
                                         retry_interval_sec=1024)
            self.fail()
        except unlock_my_tesla.UnlockException:
            pass

        self.assertEqual([mock.call(1024)], patched_sleep.call_args_list)

    @mock.patch('time.sleep')
    def test_make_request_success_after_error_exponential_backoff(self, patched_sleep):
        class Responses(object):
            def __init__(self):
                self.responses = [
                    {'error': 'no!'},
                    {'error': 'still no!'},
                    {'response': 'ok!'}
                ]
                self.times_called = 0

            def call(self):
                try:
                    return self.responses[self.times_called]
                finally:
                    self.times_called += 1

        res = Responses()
        resp = unlock_my_tesla.make_request(res.call,
                                            max_attempts=3,
                                            retry_interval_sec=1024)
        self.assertEqual('ok!', resp)
        self.assertEqual(
            [mock.call(1024), mock.call(2048)],
            patched_sleep.call_args_list
        )

    @unittest.skip('')
    def test_unlock(self):
        unlock_my_tesla.lambda_handler({'clickType': 'SINGLE'}, None)

    @unittest.skip('')
    def test_pop_frunk(self):
        unlock_my_tesla.lambda_handler({'clickType': 'DOUBLE'}, None)


if __name__ == '__main__':
    unittest.main()
