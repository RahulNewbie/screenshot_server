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
import db_schema_creator
import validator


app = Flask(__name__)
app.config['SCREENSHOT_FOLDER'] = constant.SCREENSHOT_FOLDER


def url_validator(url):
    """
    Validate the website Url
    @param: url --> website url
    @return: True if url is valid, False otherwise
    """
    if not re.match(validator.regex, url):
        return False
    return True


def fetch_image_from_thum_io(thum_io_url):
    """
    Use requests library to fetch screenshot using thum_io
    @param: thum_io url with cerdential
    @return: response
    """
    return requests.get(thum_io_url)


def remove_brackets_from_url(url):
    """
    Remove brackets and perenthasis from url
    @param : url
    @return: url after removing brackets and perenthasis
    """
    return re.sub('[\[()\]]', '', url)


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
    # Add https:// before the url
    url = constant.HTTP_ADAPTER + url
    # Remove brackets and parenthesis from the url, if any
    url = remove_brackets_from_url(url)
    # Check if the url is valid or not
    if not url_validator(url):
        return "Url is not valid, Please use valid web url"

    # Construct URL to fetch the image
    thum_io_url = constant.THUM_IO_GET_URL + constant.THUM_IO_AUTH + url

    try:
        # Construct screenshot file name as the current date and time
        tempfile = str(datetime.datetime.now().date()) + '_' + \
                   str(datetime.datetime.now().time()).replace(':', '.')
        # Full path to save the screenshot file in drive
        full_path = str(os.getcwd()) + "\\" + constant.STATIC_PATH_MEMORY + \
                   tempfile + constant.SCREENSHOT_EXTENSION

        # Fetch the image
        response = fetch_image_from_thum_io(thum_io_url)
        # Save the image in a file
        if response.status_code == constant.SUCCESS_STATUS:
            with open(full_path, 'wb') as f:
                f.write(response.content)
            # Insert record to database
            db_api.update_to_db(url, full_path)
            # If the User choose the option to view the screenshot in browser
            if option == "view":
                app.logger.info("User has chosen to view the screenshot")
                render_path = "/" + constant.STATIC_PATH_RENDER + tempfile + \
                              constant.SCREENSHOT_EXTENSION
                return render_template('screenshot.html',
                                       screenshot_url=render_path)
            elif option == "address":
                # Application will return the address of the screenshot
                app.logger.info("Screenshot fetched and saved successfully. "
                                "Address of the saved screenshot "
                                "returned to user ")
                return "Screenshot is saved in --> " + str(full_path), \
                       constant.SUCCESS_STATUS
            else:
                return "Please use valid option. Either \"view\" or \"address\""
        else:
            app.logger.error("Error happened while getting screenshots")
            return "Error happened while getting screenshots", \
                   constant.FAILURE_STATUS

    except Exception as excep:
        app.logger.error("Error while retrieve screenshot from "
                         "the provided url" + str(excep))
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
    db_schema_creator.create_db_schema()
    app.run(debug=True)
