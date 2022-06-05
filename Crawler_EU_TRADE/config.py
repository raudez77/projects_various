# Xpath File
COUNTRY = "TW"

# Date and Country
SEARCH = "//div[@class='min_width_inner containsStatus']//div[@class='search_left ui-resizable']"
DATE_BAR = SEARCH + str("//li[@id='tabFordate_search']")
DATE_EXPIRATION = SEARCH + str("//div[@id='date_search_line_2']//input")
FIND_DATE = "//div[@id='date_search']//div[@class='searchButtonContainer bottom right']"


# Country
COUNTRY_BAR = SEARCH + str("//li[@id='tabForcountry_search']")
CHOSEN_COUNTRY = SEARCH + str("//div[@id='country_search_line_2']//input")
FIND_COUNTRY = "//div[@id='country_search']//div[@class='searchButtonContainer bottom right']"


# TABLE AND PAGE
LIST = "//*[@id='results']/div[1]/div[2]/div[2]/span/div[2]/ul/li/a/span[2]"
LAST_ELEM = "//*[@id='results']/div[1]/div[2]/div[2]/span/div[2]/ul/li/ul/li[last()]"
PAG = "/html/body/div[4]/div[2]/form/div[3]/div[1]/div# Xpath File" 


# Filter
FILTERBY = "//div[@class='min_width_inner containsStatus']//div[@class='search_right']"
FILTER_TW = FILTERBY + f"//div[@class='facetCounts columns_4']//label[@for='{COUNTRY}']"
APPLY_FILTER = FILTERBY + str("//div[@id='source_filter']//a[@role='button'][1]//span[@class='ui-button-text']")
SEARCH_ = "//*[@id='source_filter']/div[1]/div/div[6]/div/a[19]"
