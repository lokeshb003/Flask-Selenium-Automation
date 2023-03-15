from flask import Flask, request, render_template
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

# Set up the Chrome driver with a Service object
chrome_driver_path = r"C:\Users\raghu\PycharmProjects\FP\chromedriver.exe" # Replace with the path to your chromedriver executable
chrome_service = webdriver.chrome.service.Service(executable_path=chrome_driver_path)
chrome_service.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_url', methods=['POST'])
def process_url():
    url = request.form['url']
    browser = webdriver.Chrome(service=chrome_service)

    try:
        # Navigate to the user-specified URL
        browser.get(url)

        # wait for the search box to appear
        if(url=="https://in.search.yahoo.com/"):
           search_box = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.NAME, "p"))
         )
        elif(url=="https://www.google.com/"or url=="https://openverse.org/" or url=="https://www.bing.com/" or url=="https://www.ecosia.org/?c=en"):
            search_box = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
        else:
            search_box = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.NAME, "search"))
            )


        # interact with the search box
        search_box.send_keys('Techngium')
        search_box.submit()

        # get the page title
        title = browser.title

    except NoSuchElementException:
        title = 'Element not found'

    finally:
        # close the browser window
        browser.quit()

    return render_template('result.html', title=title)

@app.teardown_appcontext
def shutdown_session(exception=None):
    chrome_service.stop()

if __name__ == '__main__':
    app.run(debug=True)