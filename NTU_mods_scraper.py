from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
import pandas as pd
    
def searchForDependentMods(prereq, courseAndYearOfStudy, acadYearCode):
    #-------------------Driver setup---------------------
    options = Options()
    #options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(10)
    driver.get('https://wis.ntu.edu.sg/webexe/owa/aus_subj_cont.main')

    #-------------------Search for desired course & year---------------------
    acadYearSelect = Select(driver.find_element(By.NAME, 'acadsem'))
    acadYearSelect.select_by_value(acadYearCode)
    sleep(1)

    courseSelect = Select(driver.find_element(By.NAME, 'r_course_yr'))
    courseSelect.select_by_value(courseAndYearOfStudy)

    allInputs = driver.find_elements(By.TAG_NAME, 'input')
    for inputElement in allInputs:
        if (inputElement.get_attribute('value') == 'Load Content of Course(s)'):
            loadCourseButton = inputElement
    loadCourseButton.click()
    sleep(1)

    #-------------------Get results---------------------
    driver.switch_to.frame('subjects')
    courseEntries = driver.find_elements(By.TAG_NAME, 'tbody')
    dependentMods = []
    for entry in courseEntries:
        allFontElements = entry.find_elements(By.TAG_NAME, 'font')
        isDependent = False
        for fontElement in allFontElements:
            if prereq in fontElement.text:
                isDependent = True
        if isDependent: 
            dependentMods.append(entry)

    print()
    for entry in dependentMods:
        print( entry.text )
        print()
    
    driver.close()

searchForDependentMods('EE3015', 'EEE;;4;F', '2021_2')