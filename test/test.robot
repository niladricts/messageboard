*** Settings ***
Documentation  This is a test suite with Robot Framework for message board
Library  Selenium2Library

*** Variables ***
${SERVER}          http://127.0.0.1:5000/
${BROWSER}         Chrome
${DELAY}           1

*** Keywords ***

Open Browser To Create page
   Open Browser  ${SERVER} ${BROWSER}
   Maximize Browser Window
   Set Selenium Speed ${DELAY}
*** Test Cases ***
[Teardown].     Close Browser