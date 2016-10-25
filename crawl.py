from selenium import webdriver
from selenium.webdriver.support.ui import Select
import info, time, sys

my_subjects = {'Calculus', 'Python', 'Ruby', 'JavaScript', 'Computer Science', 'Computer Programming', 'JQuery'}

def get_url():
    prefix = 'https://www.wyzant.com/Tutor/Jobs'
    return 'https://www.wyzant.com/Tutor/Jobs?f=5&cat=0&sub=361&lt=1' +'&pageSize=100'
def login(browser):
    browser.get('https://www.wyzant.com/login')
    user_name_div = browser.find_element_by_id('Username')
    user_name_div.send_keys(info.user_name)
    password_div = browser.find_element_by_id('Password')
    password_div.send_keys(info.password)
    password_div.submit()

def get_job_links(browser, limit = float('inf')):
    links = list()
    job_results = browser.find_elements_by_class_name('job-result')
    for job_result in job_results:
        description = job_result.find_element_by_xpath(".//h4").text
        subject = description.split('Student')[0].strip()
        if subject in my_subjects:
            url = job_result.find_element_by_class_name('btn-wide').get_attribute('href')
            links.append( (url, subject) )
            if len(links) >= limit:
                break
    return links

def apply_to_job(browser, job):
    url, subject = job
    browser.get(url)
    info_div = browser.find_element_by_id('jobTextModal')
    h4s = browser.find_elements_by_xpath('.//h4')
    print(subject)
    for h4 in h4s:
        if 'Personal message to' in h4.text:
            name = h4.text.strip('Personal message to').strip('(required)').strip()
            break
    drop_down = Select(browser.find_element_by_id('TemplateId'))
    drop_down.select_by_visible_text(subject)
    submit_button = browser.find_element_by_css_selector('[type=submit]')
    time.sleep(1)
    submit_button.submit()

def main():
    my_url = get_url()
    # browser = webdriver.Chrome()
    browser = webdriver.PhantomJS()
    login(browser)
    browser.get(my_url)
    job_links = get_job_links(browser, limit = 30)
    print('linkss???', len(job_links))
    for job in job_links:
        apply_to_job(browser, job)
    print('Applied to %s jobs' %(len(job_links))  )
main()
# get_url()
