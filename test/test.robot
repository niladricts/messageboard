*** Settings ***
Library  Selenium2Library

*** Variables ***
${SERVER}          http://127.0.0.1:5000/create
${BROWSER}         firefox

*** Keywords ***
Set Environment Variable  webdriver.gecko.driver  C:\Users\bsens\Scripts\geckodriver.exe

*** Test Cases ***
Flask Test
    [Documentation]   This is a test suite with Robot Framework for message board.
    [Tags]  Tag.
    Open Browser  ${SERVER}
    Close Browser