import shutil
import sys


from pytest_dash.wait_for import (
    wait_for_text_to_equal,
    wait_for_element_by_css_selector,
    wait_for_element_by_id,
    wait_for_element_by_xpath,
    wait_for_property_to_equal
)
from pytest_dash.application_runners import import_app
import selenium

def test_install(dash_threaded):

    # Add the generated project to the path so it can be loaded from usage.py
    # It lies somewhere in a temp directory created by pytest-cookies
    sys.path.insert(0, '..')

    # Test that `usage.py` works after building the default component.
    dash_threaded(import_app('app'))
    driver = dash_threaded.driver

    slider = wait_for_element_by_id(
          driver,
          'bg-width-slider'
      )
    #button_select = wait_for_element_by_xpath(
    #      driver,
    #      "//button[@title='Rectangle']"
    #)
    #button_undo = wait_for_element_by_xpath(
    #      driver,
    #      "//button[@title='Undo']"
    #)
    # button_select.click()
    canvas = wait_for_element_by_xpath(
            driver,
            "//DashCanvas"
            )
    print("for canvas", canvas.get_property('tool'),
                        canvas.get_property('width'),
                        canvas.get_property('lineWidth'))
    #my_component = selenium.find_element_by_id('input')
