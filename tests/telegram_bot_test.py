import unittest
from utils.telegram_bot import send_message


class TestTelegramBot(unittest.TestCase):
    def test_send_hello(self):
        message = 'Hello World'
        json_response = send_message(message)
        print(json_response)

        # Check if the function return successfully
        self.assertEqual(
            json_response['ok'], True)
        self.assertEqual(
            json_response['result']['text'], message)


if __name__ == '__main__':
    unittest.main()
