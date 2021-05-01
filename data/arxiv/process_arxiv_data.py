import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

csv_data = 'processed/nodeidx2paperid.csv'
csv_out = 'processed/nodeidx2paperid_processed.csv'

OUT_FILE = open(csv_out, 'w')
PAGE_LOAD_TIME = 1  # in seconds
firefox_options = FirefoxOptions()
firefox_options.add_argument("user-agent=fri-masters-research")
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_options, executable_path='./geckodriver')
driver.set_page_load_timeout(5)  # page load timeout


def get_paper_title(paper_id):
    try:
        driver.get(f'https://academic.microsoft.com/paper/{paper_id}')
        time.sleep(PAGE_LOAD_TIME)
        title = driver.find_element_by_xpath('.//h1[@class="name"]').text
    except Exception:
        title = ''
    print(f'{paper_id} —> {title}')
    return title


with open(csv_data, 'r') as file:
    header = file.readline().strip()
    header += ',title\n'
    OUT_FILE.write(header)  # Write modified header

    for line in file:
        data_line = file.readline().strip()
        paper_id = data_line.split(',')[1]
        paper_title = get_paper_title(paper_id)
        data_line += f',{paper_title}\n'
        OUT_FILE.write(data_line)

OUT_FILE.close()