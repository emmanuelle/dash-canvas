import shutil
import sys
import dash
import dash_html_components as html
import dash_core_components as dcc
from time import sleep

from pytest_dash.wait_for import (
    wait_for_text_to_equal,
    wait_for_element_by_css_selector,
    wait_for_element_by_id,
    wait_for_element_by_xpath,
    wait_for_property_to_equal
)
import selenium

def test_install(dash_threaded):

    # Add the generated project to the path so it can be loaded from usage.py
    # It lies somewhere in a temp directory created by pytest-cookies

    # Test that `usage.py` works after building the default component.
    app = dash.Dash(__name__)
    driver = dash_threaded.driver

    app.layout = html.Div([
        html.Div('My test layout', id='out'),
        html.Button('click me', id='click-me', title='first'),
        html.Button('click me', id='click-also', title='second'),
        dcc.Input(id='input', value='MTL', type='text'),
    ])

    dash_threaded(app)

    button1 = wait_for_element_by_xpath(driver, "//button[@title='first']")
    button2 = wait_for_element_by_xpath(driver, "//button[@title='second']")
    input_el = wait_for_element_by_xpath(driver, "//input")
    print("all is", input_el.get_property('id'), input_el.get_property('width'), dir(input_el))

if __name__=='__main__':
    test_install()
