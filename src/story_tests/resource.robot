*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem

*** Variables ***
${SERVER}    localhost:5000
${HOME_URL}    http://${SERVER}
${BROWSER}    chrome
${HEADLESS}    false
${DELAY}    0.5 seconds

*** Keywords ***
Open Browser To Home
    ${options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys
    Call Method    ${options}    add_argument    --no-sandbox
    Call Method    ${options}    add_argument    --disable-dev-shm-usage
    Call Method    ${options}    add_argument    --disable-gpu
    Run Keyword If    '${HEADLESS}' == 'true'    Call Method    ${options}    add_argument    --headless
    Run Keyword If    '${HEADLESS}' == 'true'    Set Selenium Speed    0 seconds
    Run Keyword If    '${HEADLESS}' != 'true'    Set Selenium Speed    ${DELAY}
    Open Browser    ${HOME_URL}    ${BROWSER}    options=${options}

Home Page Should Be Open
    Title Should Be    Lähde Kirjasto

Click Add Source And Navigate
    [Arguments]    ${type}
    Select From List By Value    id=lahde    ${type}
    Click Button    id=submit-btn
    Wait Until Location Contains    /add_${type}    timeout=5s

Fill Article Form
    Input Text    name=author    John Doe
    Input Text    name=title     Test Article
    Input Text    name=journal   Journal X
    Input Text    name=year      2024
    Input Text    name=month     1
    Input Text    name=volume    5
    Input Text    name=number    2
    Input Text    name=pages     100-120
    Input Text    name=notes     Sample notes
    Click Button   xpath=//button[contains(text(),'Lisää')]

Fill Book Form
    Input Text    name=author    Jane Smith
    Input Text    name=title     Test Book
    Input Text    name=editor    Editor X
    Input Text    name=publisher   Pub Y
    Input Text    name=year      2024
    Input Text    name=month     5
    Input Text    name=volume    v1
    Input Text    name=number    7
    Input Text    name=pages     200
    Input Text    name=notes     Book notes
    Click Button   xpath=//button[contains(text(),'Lisää')]

Fill Inproceedings Form
    Input Text    name=author    Bob Johnson
    Input Text    name=title     Test Proc
    Input Text    name=booktitle   Conf X
    Input Text    name=year      2023
    Input Text    name=month     3
    Input Text    name=editor    Ed Y
    Input Text    name=volume    1
    Input Text    name=number    12
    Input Text    name=series    Springer LNCS
    Input Text    name=pages     33-44
    Input Text    name=address   NY
    Input Text    name=organization  Org Z
    Input Text    name=publisher   Pub A
    Input Text    name=notes     Proc notes
    Click Button   xpath=//button[contains(text(),'Lisää')]

Fill Misc Form
    Input Text    name=author    Alice Brown
    Input Text    name=title     Test Misc
    Input Text    name=year      2022
    Input Text    name=month     10
    Input Text    name=url       https://example.com
    Input Text    name=notes     Misc notes
    Click Button   xpath=//button[contains(text(),'Lisää')]

Verify Item Visible On Home
    [Arguments]    ${text}
    Go To    ${HOME_URL}
    Page Should Contain    ${text}
