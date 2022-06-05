import datetime
import pandas
import requests
import selenium
import time
import urllib


class Crawler:
    def __init__(self, Url: str, dates: list, country: str,
                 country_filter: str, google_path: str):
        """ Class Crawler: Selenium Bot to iterate 
        through EU TRADE WEBSITE Be responsable and kind to this Sever"""
        self.Url = Url
        self.dates = dates
        self.country = country
        self.country_filter = country_filter
        self.google_path = google_path
        self.driver = selenium.webdriver.Chrome(
            executable_path=self.google_path)
        self.stop = 1

    def get_site(self):
        """ Initate Browser - Bot """
        self.driver.get(self.Url)

    def search_date_and_country(self) -> None:
        """This fuction insert and search in 
        The windows Search field: ONlY date and Country"""

        # Settings
        self.get_site()
        SEARCH = "//div[@class='min_width_inner containsStatus']//div[@class='search_left ui-resizable']"

        # Date
        DATE_BAR = SEARCH + str("//li[@id='tabFordate_search']")
        DATE_EXPIRATION = SEARCH + str(
            "//div[@id='date_search_line_2']//input")
        FIND_DATE = "//div[@id='date_search']//div[@class='searchButtonContainer bottom right']"

        # Country
        COUNTRY_BAR = SEARCH + str("//li[@id='tabForcountry_search']")
        CHOSEN_COUNTRY = SEARCH + str(
            "//div[@id='country_search_line_2']//input")
        FIND_COUNTRY = "//div[@id='country_search']//div[@class='searchButtonContainer bottom right']"

        # ----------> wait for n seconds
        sleep = time.sleep(3)

        # ----------> Find the date
        self.driver.find_element_by_xpath(DATE_BAR).click()
        self.driver.find_element_by_xpath(DATE_EXPIRATION).send_keys(
            self.dates, selenium.webdriver.common.keys.Keys.ENTER)
        sleep
        # ----------> Jumping into Country
        self.driver.find_element_by_xpath(COUNTRY_BAR).click()
        time.sleep(2)
        self.driver.find_element_by_xpath(CHOSEN_COUNTRY).send_keys(
            self.country)
        time.sleep(3)
        self.driver.find_element_by_xpath(CHOSEN_COUNTRY).send_keys(
            selenium.webdriver.common.keys.Keys.DOWN,
            selenium.webdriver.common.keys.Keys.ENTER)
        sleep

        # ----------> Search
        self.driver.find_element_by_xpath(FIND_COUNTRY).click()
        sleep

    def filter_by(self):
        """ Find and Filter """

        sleep = time.sleep(3)

        # Settings
        FILTERBY = "//div[@class='min_width_inner containsStatus']//div[@class='search_right']"

        # Filter
        FILTER_TW = FILTERBY + f"//div[@class='facetCounts columns_4']//label[@for='{self.country_filter}']"
        APPLY_FILTER = FILTERBY + str(
            "//div[@id='source_filter']//a[@role='button'][1]//span[@class='ui-button-text']"
        )

        # ----------> Filter by
        self.driver.find_element_by_xpath(
            "//*[@id='source_filter']/div[1]/div/div[6]/div/a[19]").click()
        self.driver.find_element_by_xpath(APPLY_FILTER).click()
        sleep

    def find_pag_number(self) -> int:
        """ Find the pages to iterate"""

        # ----------> wait for n seconds
        sleep = time.sleep(3)

        # Settings
        LIST = "//*[@id='results']/div[1]/div[2]/div[2]/span/div[2]/ul/li/a/span[2]"
        LAST_ELEM = "//*[@id='results']/div[1]/div[2]/div[2]/span/div[2]/ul/li/ul/li[last()]"
        PAG = "/html/body/div[4]/div[2]/form/div[3]/div[1]/div[2]/div[3]/div"

        # ----------> Move to number of rows
        self.driver.find_element_by_xpath(LIST).click()
        time.sleep(2)
        self.driver.find_element_by_xpath(LAST_ELEM).click()
        time.sleep(2)

        # ----------> Max Number
        pagination = self.driver.find_element_by_xpath(PAG).text[-2:]
        pagination = int(pagination)

        return pagination

    def scrapying_table(self) -> pandas.DataFrame:
        """ scrap all tables and codes"""

        ACTUAL_TABLE = "#skipValue1"
        NEXT = "#results > div.results_navigation.top_results_navigation.displayButtons > div.results_pager.ui-widget-content > div.arrow_container > a:nth-child(4) > span.ui-button-icon-primary.ui-icon.ui-icon-triangle-1-e"

        # previous tasks
        search = self.search_date_and_country()
        filter_ = self.filter_by()
        last_page = self.find_pag_number()
        frame = pandas.DataFrame()

        # ----------> wait for n seconds
        sleep = time.sleep(3)

        # ----------> Scrapying
        while True:
            sleep

            # Loading Table
            self.driver.find_element_by_css_selector(ACTUAL_TABLE).send_keys(
                selenium.webdriver.common.keys.Keys.CONTROL + "a",
                selenium.webdriver.common.keys.Keys.DELETE)
            time.sleep(2)
            self.driver.find_element_by_css_selector(ACTUAL_TABLE).send_keys(
                self.stop, selenium.webdriver.common.keys.Keys.ENTER)
            time.sleep(2)

            # Parsing
            parse_ = pandas.read_html(self.driver.page_source,
                                      skiprows=1,
                                      flavor='lxml')[0]

            # append
            frame = pandas.concat([frame, parse_], axis=0)
            self.stop += 1

            if self.stop > last_page:
                break

        # ----------> Fixing Table
        data = frame.iloc[:, [1, 8]]
        data.columns = ['name', 'number']
        data.reset_index(drop=True, inplace=True)

        return data


class EU_Crawler:
    def __init__(self, url: str, conx_type: str, headers: dict,
                 data: pandas.Series) -> pandas.DataFrame:
        """ Craw the Europe Pattern API"""

        self.url = url
        self.conx_type = conx_type
        self.headers = headers
        self.data = data
        self.data_ = {
            'Basis': [],
            'Name': [],
            'Nice_Classes': [],
            'Filing_Numbers': [],
            'Registration_Number': [],
            "Expirty_Date": [],
            'Organization': [],
            'Correspondence_Address': []
        }

        # Initiating Session
        self.s = requests.Session()

    def scrap_website(self):
        """ Scrap the API"""
        for code in self.data.values:
            try:
                # Time for connection
                time.sleep(.5)

                # Temporary url
                temp_url = self.url + str(code)

                # Connect to Server
                req = self.s.request(self.conx_type,
                                     temp_url,
                                     headers=self.headers)
                json_ = req.json()

                # Basis
                self.data_['Basis'].append(json_['entity']['basis'])

                # Name
                self.data_['Name'].append(json_['entity']['name'])

                # Nice Classes
                self.data_['Nice_Classes'].append(",".join(
                    json_['entity']['niceclasses']))

                # Filling Number
                self.data_['Filing_Numbers'].append(
                    int(json_['entity']['number']))

                # Registration Number
                self.data_['Registration_Number'].append(
                    int(json_['entity']['number']))

                # Expiration Date
                date_ = int(json_['entity']['expirydate']) / 1000
                date = datetime.datetime.fromtimestamp(date_).strftime(
                    '%Y-%m-%d')
                self.data_['Expirty_Date'].append(date)

                # Organization
                self.data_['Organization'].append(
                    json_['entity']['applicants'][0]['orga'])

                # Adress
                address = json_['entity']['applicants'][0]['address'][
                    'postalAddress'].replace('\n', '')
                self.data_['Correspondence_Address'].append(address)

                # Image
                digits_8 = json_['entity']['number']
                folder = r'mypath' + str('\\') + str(digits_8) + str('.png')

                if json_['entity']['image'] != None:
                    # image exists
                    url_image = str('https://euipo.europa.eu'
                                    ) + json_['entity']['image']['url']
                    urllib.request.urlretrieve(url_image, folder)

                else:
                    no_image = 'https://www.freeiconspng.com/thumbs/no-image-icon/no-image-icon-6.png'
                    urllib.request.urlretrieve(no_image, folder)
            except:
                print("Error with code", code)

        data = pandas.DataFrame.from_dict(self.data_)
        return data
