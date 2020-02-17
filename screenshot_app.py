from collections import defaultdict
from flask import Flask, render_template
import requests
import json
import logging
from logging.handlers import RotatingFileHandler
import datetime
import os
import re
import constant
import db_api
import validator


app = Flask(__name__)
app.config['SCREENSHOT_FOLDER'] = constant.SCREENSHOT_FOLDER


def url_validator(url):
    """
    Validate the website Url
    """
    if not re.match(validator.regex, url):
        return False
    return True


@app.route('/<url>/<option>')
def get_screenshot(url, option):
    """
    Get screenshot from thum.io by providing the website url
    @param : url --> Url of the website
            option --> Option to recieve the screenshot. If
            option is "view", then screenshot will be displayed in browser.

            If option is address, then user will receive the address
            of the saved screenshot
    @return : Screenshot will be displayed in the browser, or user will recieve
    the address of the screenshot, in case of successful execution.
    Else user will receive the appropriate error msg
    """
    url = constant.HTTP_ADAPTER + url
    # strip brackets and parenthesis
    url = re.sub('[\[()\]]', '', url)

    if not url_validator(url):
        return "Url is not valid, Please use valid web url"

    # Construct URL to fetch the image
    thum_io_url = constant.THUM_IO_GET_URL + constant.THUM_IO_AUTH + url

    try:
        tempfile = str(datetime.datetime.now().date()) + '_' + \
                   str(datetime.datetime.now().time()).replace(':', '.')
        full_path = str(os.getcwd()) + "\\" + constant.STATIC_PATH_MEMORY + \
                   tempfile + constant.SCREENSHOT_EXTENSION

        # Fetch the image
        response = requests.get(thum_io_url)
        # Save the image in a file
        if response.status_code == constant.SUCCESS_STATUS:
            with open(full_path, 'wb') as f:
                f.write(response.content)
            # Insert record to database
            db_api.update_to_db(url, full_path)
            # If the User choose the option to view the screenshot in browser
            if option == "view":
                render_path = "/" + constant.STATIC_PATH_RENDER + tempfile + \
                              constant.SCREENSHOT_EXTENSION
                return render_template('screenshot.html',
                                       screenshot_url=render_path)
            else:
                # Application will return the address of the screenshot
                return "Screenshot is saved in --> " + str(full_path)
        else:
            return "Error happened while getting screenshots", constant.FAILURE_STATUS

    except Exception as excep:
        return "Could not retrieve the site" + str(excep)


@app.route('/list')
def get_list_of_screenshots():
    """
    Function to show the scrrenshot table data
    """
    try:
        data = db_api.select_all_data_from_table()
    except Exception as excep:
        app.logger.error('Error occurred while showing screenshot data'
                         + str(excep))
    return render_template('index.html', rows=data)


if __name__ == '__main__':
    # Logging
    handler = RotatingFileHandler('app_logger.log', maxBytes=10000,
                                  backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    db_api.create_db_schema()
    app.run(debug=True)
