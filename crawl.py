import os, time, sys
import secrets.info as info
def log (message, speak = True):
    if speak:
        os.system('say '+ message )
    print(message)
log('wyzant crawl starting')

selenium_path = '/Users/DZack/anaconda/lib/python3.5/site-packages/'
sys.path.append(selenium_path)
try:
    from selenium import webdriver
except:
    log('webdriver import failure')
from selenium.webdriver.support.ui import Select

my_subjects = {'Logic','SAT Writing','Trigonometry','Calculus', 'Python', 'Ruby', 'JavaScript', 'Computer Science', 'Computer Programming', 'JQuery', 'Precalculus', 'SAT Math'}


def login(browser):
    browser.get('https://www.wyzant.com/login')
    user_name_div = browser.find_element_by_id('Username')
    user_name_div.send_keys(info.user_name)
    password_div = browser.find_element_by_id('Password')
    password_div.send_keys(info.password)
    password_div.submit()

def get_job_links(browser, limit = float('inf')):
    # $('.wc-online') for checking if student is online
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
    body = browser.find_element_by_id('ApplicationText')
    text = body.get_attribute('value')
    # wait for text
    count = 0
    while not text:
        # print('waiting....')
        text = body.get_attribute('value')
        time.sleep(.05)
        print('in a loop %s' %(str(count)))
        count += 1
        if count > 100:
            return log('stuck in a loop, moving on')

    # reformat text (name and online)
    # closing_line = online_message if is_online else in_person
    # then format it
    text = text %(name)
    # put back in body
    body.clear()
    body.send_keys(text)
    submit_button = browser.find_element_by_css_selector('[type=submit]')
    submit_button.submit()

def hit_all_on_page(my_url, limit = float('inf')):
    # browser = webdriver.Chrome()
    browser.get(my_url)
    job_links = get_job_links(browser, limit)
    for job in job_links:
        apply_to_job(browser, job)
    message = 'Applied to %s jobs \n' %(len(job_links))
    log(message)
def set_rate(rate):
    browser.get('https://www.wyzant.com/Tutor/RateAndPolicies.aspx')
    rate_div = browser.find_element_by_id("ctl00_ctl00_PageCPH_ResponsiveContent_RateAndPolicies1_txtHourlyRate")
    rate_div.clear()
    rate_div.send_keys(rate)
    submit_button = browser.find_element_by_css_selector('[type=submit]')
    submit_button.click()

def main():
    prefix = 'https://www.wyzant.com/Tutor/Jobs?f='
    set_rate(55)
    log('comp online')
    hit_all_on_page(prefix + '5&cat=10&sub=0&lt=2&pageSize=100')
    log('all online')
    hit_all_on_page(prefix + '1&lt=2&pageSize=100', limit = 15)
    set_rate(70)
    log('comp person')
    hit_all_on_page(prefix +'5&cat=10&sub=0&lt=1&pageSize=100')
    log('all person')
    hit_all_on_page(prefix +'1&lt=1&pageSize=100', limit = 15)

browser = webdriver.PhantomJS()
try:
    login(browser)
    main()
    log('successful scrape, apparently')
except:
    log('something has gone wrong')
    current_time=  time.strftime("%Y-%m-%d %H:%M")
    new_file = open('Desktop/WYZANT_SCRAPE_ERROR', 'w')
    new_file.write(current_time)
    new_file.close()
