*** Settings ***
Resource    resource.robot
Suite Setup     Open Browser To Home
Suite Teardown  Close Browser

*** Test Cases ***
User Can Navigate To Home Page
    Home Page Should Be Open

User Can Add Article
    Click Add Source And Navigate    article
    Fill Article Form
    Verify Item Visible On Home    Test Article

User Can Add Book
    Click Add Source And Navigate    book
    Fill Book Form
    Verify Item Visible On Home    Test Book

User Can Add Inproceedings
    Click Add Source And Navigate    inproceedings
    Fill Inproceedings Form
    Verify Item Visible On Home    Test Proc

User Can Add Misc
    Click Add Source And Navigate    misc
    Fill Misc Form
    Verify Item Visible On Home    Test Misc

User Can See All Added Items On Home Page
    Go To    ${HOME_URL}
    Page Should Contain    Test Article
    Page Should Contain    Test Book
    Page Should Contain    Test Proc
    Page Should Contain    Test Misc

User Cannot Add Book With Invalid Year
    Click Add Source And Navigate    book

    Input Text    name:author      Invalid Author
    Input Text    name:title       Invalid Book
    Input Text    name:editor      Invalid Editor
    Input Text    name:publisher   Invalid Publisher

    # Invalid year (letters into <input type="number">)
    Input Text    name:year        ABCD

    Click Button    Lisää

    # Form submission should be blocked → same URL
    Location Should Contain    /add_book

    # The item must not be visible on home page
    Go To    ${HOME_URL}
    Page Should Not Contain    Invalid Book
