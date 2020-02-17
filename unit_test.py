import unittest
import screenshot_app
import db_api
import validator
import constant


VALID_URL = "https://www.goal.com"
INVALID_URL = "google.com"
URL_WITH_BRACKETS = "goal.com()"
THUM_IO_INVALID_AUTH = "auth/invalid/"


class TestScreenshotMethods(unittest.TestCase):
    def test_valid_url(self):
        self.assertEqual(screenshot_app.url_validator(VALID_URL), True)

    def test_invalid_url(self):
        self.assertEqual(screenshot_app.url_validator(INVALID_URL), False)

    def test_remove_brackets(self):
        self.assertEqual(screenshot_app.remove_brackets_from_url(URL_WITH_BRACKETS), "goal.com")

    def test_fetch_image(self):
        thum_io_url = constant.THUM_IO_GET_URL + constant.THUM_IO_AUTH + VALID_URL
        response = screenshot_app.fetch_image_from_thum_io(thum_io_url)
        self.assertEqual(response.status_code, constant.SUCCESS_STATUS)

    def test_negetive_case_fetch_image(self):
        thum_io_url = constant.THUM_IO_GET_URL + THUM_IO_INVALID_AUTH + VALID_URL
        response = screenshot_app.fetch_image_from_thum_io(thum_io_url)
        self.assertNotEqual(response.status_code, constant.FAILURE_STATUS)

    def test_get_screenshot(self):
        response = screenshot_app.get_screenshot("goal.com", "address")
        self.assertEqual(response[1], constant.SUCCESS_STATUS)


if __name__ == '__main__':
    unittest.main()
