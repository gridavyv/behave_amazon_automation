from behave import step
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import warnings


@step("Navigate to '{test_page}'")
def step_impl(context, test_page):
    context.driver.get(url=context.PAGE_URL)
    print(f"The page {test_page} is opened")
    time.sleep(2)


##################################
# SEARCH FEATURE METHODS | START #
##################################


@step("[Header] Verify search category '{exp_category}'")
def step_impl(context, exp_category):
    xpath = "//div[@class='global-header-container' or @class='x-header']//select/option"
    categories = context.driver.find_elements(By.XPATH, xpath)
    try:
        if not categories:
            raise IndexError("List is empty. Categories widget has npt been found")
        if categories[0].text != exp_category:
            raise ValueError(f"Incorrect category: '{categories[0].text}' instead of '{exp_category}'")
    except (IndexError, ValueError) as e:
        print(f"Exception:{e}")


@step("[Header] Enter query '{query}'")
def step_impl(context, query):
    xpath = "//div[@class='global-header-container' or @class='x-header']//input[@type='text']"
    search_filed = context.driver.find_element(by=By.XPATH, value=xpath)
    search_filed.send_keys(query)


@step("[Header] Click on button '{bttn_name}'")
def step_impl(context, bttn_name):
    xpath = f"//div[@class='global-header-container' or @class='x-header']//input[@value='{bttn_name}']"
    search_bttn = context.driver.find_element(by=By.XPATH, value=xpath)
    search_bttn.click()
    time.sleep(2)


@step("Verify page title contains query '{query}'")
def step_impl(context, query):
    title = context.driver.title
    try:
        if query not in title:
            raise ValueError("Incorrect page title.")
    except ValueError as e:
        print(f"Exception: {e}")


@step("Verify all results are related to query '{exp_query}'")
def step_impl(context, exp_query):
    results_headers = context.driver.find_elements(By.XPATH,
                                                   "//div[@class ='srp-river srp-layout-inner']//div[@class='carousel__viewport']//following::span[@role='heading']")
    for heading_text in results_headers:
        if exp_query.lower() not in heading_text.text.lower():
            raise ValueError(
                f"Result: '{heading_text.text.lower()}' is not related to search query: '{exp_query.lower()}'.")


@step("[Result answer] Verify result feedback '{exp_text}'")
def step_impl(context, exp_text):
    result_answer = (WebDriverWait(context.driver, context.WAIT_TIME).until(EC.visibility_of_element_located(
        (By.XPATH, f"//li[contains(@class,'srp-river-answer srp-river-answer--')]//*[contains(text(),'{exp_text}')]")),
                                                             message="The element is NOT displayed"))
    if result_answer.text != exp_text:
        print(f"Incorrect answer: '{result_answer.text}' instead of '{exp_text}'")


@step("Verify num of items per page '{num_of_results}'")
def step_impl(context, num_of_results):
    # Get the number of elements per page from the last bttn_cell
    # use XPath with "following" to cut 3 irrelevant bttn_cells
    results_per_page = context.driver.find_element(By.XPATH,
                                                   "//nav[@class='pagination']//following::span[@class='btn__cell']").text
    assert int(results_per_page) == int(num_of_results), \
        f"Incorrect num of results: {results_per_page} instead of {num_of_results}"


@step("Verify num of presented results (excluding carousel results:{num_of_carousel_res}) equals to num items per page")
def step_impl(context, num_of_carousel_res):
    # Get the selected items per page from bttn_cell
    # XPath with "following" to locate the last of 4 bttn_cells
    results_per_page = context.driver.find_element(By.XPATH,
                                                   "//nav[@class='pagination']//following::span[@class='btn__cell']").text
    # Get number of results excluding the 1-st empty element and carousel (8 elements)
    result_headers = context.driver.find_elements(By.XPATH, "//span[@role='heading']")
    num_presented_results = len(result_headers) - int(num_of_carousel_res) - 1
    assert num_presented_results == int(results_per_page), \
        f"The statement is: {num_presented_results} instead of {int(results_per_page)}"


@step("Find on the page number {page_num} the item with the lowest price and print its title")
def step_impl(context, page_num):
    item_cards = context.driver.find_elements(By.XPATH,
                                              "//div[@class ='srp-river srp-layout-inner']//div[@class='carousel__viewport']//following::div[@class='s-item__info clearfix']")
    lowest_price = 0
    lowest_price_title = ""
    for item_card in item_cards:
        item_price_text = item_card.find_element(By.XPATH, "descendant::span[@class='s-item__price']").text
        item_price_num = float(item_price_text.replace("$", ""))
        if lowest_price == 0 or item_price_num < lowest_price:
            lowest_price = item_price_num
            lowest_price_title = item_card.find_element(By.XPATH, "descendant::span[@role='heading']").text
    print(lowest_price)
    print(lowest_price_title)


################################
# SEARCH FEATURE METHODS | END #
################################

######################################
# CATEGORIES FEATURE METHODS | START #
######################################

@step("[MainPage CategoryLinksContainer] Verify '{link_text}' is default category")
def step_impl(context, link_text):
    xpath = f"//ul[contains(@class,'nav__container')]//span[text()='{link_text}']"
    category = context.driver.find_element(By.XPATH, xpath)
    assert category, f"The category '{link_text}' is not displayed in CategoryLinksContainer."


@step("[MainPage CategoryLinksContainer] Click on '{link_text}'")
def step_impl(context, link_text):
    xpath = f"//ul[contains(@class,'nav__container')]/li/a[text()='{link_text}']"
    category = context.driver.find_element(By.XPATH, xpath)
    category.click()
    time.sleep(1)


@step("[SubPage] Verify page title '{exp_title}'")
def step_impl(context, exp_title):
    try:
        page_title = context.driver.title
        if page_title == "Security Measure":
            raise Exception("Captcha required.")
        if exp_title not in page_title:
            raise ValueError(f"Incorrect title '{page_title}' does not contain '{exp_title}'.")
    except (Exception, ValueError) as e:
        print(f"Exception: '{e}'")


@step("[SubPage PageContainerTop] Verify title '{exp_page_title}'")
def step_impl(context, exp_page_title):
    try:
        cont_title = WebDriverWait(driver=context.driver, timeout=context.WAIT_TIME).until(EC.visibility_of_element_located(
            (By.XPATH, "//*[self::div or self::section]//*[self::h1 or self::h1/span]")),
                                        message="The element is NOT displayed")
        if cont_title.text != exp_page_title:
            raise ValueError(f"Incorrect text: '{cont_title.text}'. Expected '{exp_page_title}'.")
    except ValueError as e:
        print(f"Exception: '{e}'")


####################################
# CATEGORIES FEATURE METHODS | END #
####################################

##########################################
# SEARCH_RESULTS FEATURE METHODS | START #
##########################################


@step("Verify all items from page '{start}' to '{end}' related to query '{exp_query}'")
def step_impl(context, start, end, exp_query):
    assert int(start) <= int(end), f"Incorrect input: start_page: {start} > end_page: {end}"
    start_page = context.driver.find_element(By.XPATH, f"//div[@class='s-pagination']//ol//a[text()='{start}']")
    start_page.click()
    cur_page_text = context.driver.find_element(By.XPATH,
                                                "//div[@class='s-pagination']//ol//a[@aria-current='page']").text
    while int(cur_page_text) <= int(end):
        print(f"I am on the page {cur_page_text}")
        context.execute_steps(f"""Then Verify all results are related to query '{exp_query}'""")

        next_page_icon = context.driver.find_element(By.XPATH,
                                                     "//div[@class='s-pagination']//a[@aria-label='Go to next search page']")
        next_page_icon.click()
        cur_page_text = context.driver.find_element(By.XPATH,
                                                    "//div[@class='s-pagination']//ol//a[@aria-current='page']").text


########################################
# SEARCH_RESULTS FEATURE METHODS | END #
########################################

###########################################
# BANNER_CAROUSEL FEATURE METHODS | START #
###########################################

@step("Print banners as webelements")
def step_impl(context):
    banners = WebDriverWait(context.driver, context.WAIT_TIME).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//div[contains(@class,'carousel__autoplay')]//li")),
        "Banner is not presented")
    for banner in banners:
        print(banner)


@step("[BannerCarousel] Verify there are '{exp_num_of_banners}' banners in the carousel")
def step_impl(context, exp_num_of_banners):
    banners = WebDriverWait(context.driver, context.WAIT_TIME).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//div[contains(@class,'carousel__autoplay')]//li")),
        "Banner is not presented")
    if len(banners) != int(exp_num_of_banners):
        raise Exception(f"Incorrect number of banners. Expected: '{exp_num_of_banners}', actual: '{len(banners)}'")


@step("[BannerCarousel] Verify that every '{exp_sec}' seconds new banner is displayed. The number of banners: '{num_of_banners}'.")
def step_impl(context, exp_sec, num_of_banners):
    banner_texts = []
    print(f" The Context var is '{context.cur_banner_text}'")
    for _ in range(int(num_of_banners)):
        remember_cur_banner_text(context)
        if context.cur_banner_text in banner_texts:
            raise ValueError(f"Banner text '{context.cur_banner_text}' has been shown before. The list of shown texts: {banner_texts}")
        banner_texts.append(context.cur_banner_text)
        time.sleep(float(exp_sec))
    print(banner_texts)


@step("[BannerCarousel] Click on '{bttn_name}' button")
def click_banner_bttn(context, bttn_name):
    carousel_bttn = WebDriverWait(driver=context.driver, timeout=context.WAIT_TIME).until(
        method=EC.visibility_of_element_located
        ((By.XPATH, f"//div[contains(@class,'carousel__autoplay')]//button[contains(@aria-label,'{bttn_name}')]")),
        message=f"The '{bttn_name}' button is not displayed")
    carousel_bttn.click()
    print(f"'{bttn_name}' button is clicked.")
    time.sleep(1)


@step("[BannerCarousel] Remember the current banner")
def remember_cur_banner_text(context):
    """The function retrieves the header text of the current banner and stores is in scenario level variable 'context.cur_banner_text'
    The function does not return anything, just updates the scenario level var."""
    cur_banner = WebDriverWait(context.driver, context.WAIT_TIME).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class,'carousel__autoplay')]//li[not(@aria-hidden)]")),
        "Banner is not presented")
    cur_banner_header = cur_banner.find_element(By.XPATH, "descendant::a//span")
    context.cur_banner_text = cur_banner_header.text  # assign value to scenario level variable to reuse later
    print(f"New value '{context.cur_banner_text}' is assigned to the scenario level var 'context.cur_banner_text'.")


@step("[BannerCarousel] Verify that banner is not changing for '{req_wait_in_sec}' seconds")
def step_imp(context, req_wait_in_sec):
    time.sleep(float(req_wait_in_sec))
    cur_banner = WebDriverWait(context.driver, context.WAIT_TIME).until(
            method=EC.presence_of_element_located
            ((By.XPATH, "//div[contains(@class,'carousel__autoplay')]//li[not(@aria-hidden)]")),
            message="Banner element is not presented")
    cur_banner_header = cur_banner.find_element(By.XPATH, "descendant::a//span")
    print(f"The actual banner after wait: '{cur_banner_header.text}'")
    if cur_banner_header.text != context.cur_banner_text:  # compare with the text from the first step of scenario execution
        raise ValueError(f"The expected banner is '{context.cur_banner_text}', actual banner is '{cur_banner_header.text}'")


@step("Verify '{num_of_banners}' banner links work")
def stem_impl(context, num_of_banners):
    click_banner_bttn(context, "Pause")  # make sure that banner will not change after pulling its header
    titles = {}
    titles["main_page_title"] = context.driver.title  # store main page title to compare with sub page titles
    for _ in range(int(num_of_banners)):
        remember_cur_banner_text(context)
        count_down = 4  # introduce a counter to avoid infinite while loop
        while context.cur_banner_text in titles.keys() and count_down != 0:  # make sure the banner is new
            click_banner_bttn(context, "Go to next")
            remember_cur_banner_text(context)
            count_down -= 1
        cur_banner = WebDriverWait(context.driver, context.WAIT_TIME).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'carousel__autoplay')]//li[not(@aria-hidden)]")),
            "Banner is not presented")
        cur_banner.click()  # at this point the banner is new
        sub_page_title = context.driver.title
        if sub_page_title not in titles.values():  # make sure the sub page title is not repeated
            titles[context.cur_banner_text] = sub_page_title
        else:
            raise ValueError(f"The banner '{context.cur_banner_text}' sub page has repeated the title '{sub_page_title}' that was presented already.\nAll headers & titles: '{titles}'")
        context.driver.back()
        click_banner_bttn(context, "Pause")  # after return to the main page the carousel is playing, so pause it again
    print(titles)


@step("[BannerCarousel] Verify the banner is changed")
def step_impl(context):
    cur_banner = WebDriverWait(context.driver, context.WAIT_TIME).until(
            method=EC.presence_of_element_located
            ((By.XPATH, "//div[contains(@class,'carousel__autoplay')]//li[not(@aria-hidden)]")),
            message="Banner element is not presented")
    cur_banner_header = cur_banner.find_element(By.XPATH, "descendant::a//span")
    if cur_banner_header.text == context.cur_banner_text:  # compare with the text from the first step of scenario execution
        raise ValueError(f"Banner is not changed. The actual banner is '{cur_banner_header.text}' and the previous banner is '{context.cur_banner_text}'")


@step("[BannerCarousel] Verify the banner is the same as in the beginning of the secenario execution.")
def step_impl(context):
    cur_banner = WebDriverWait(context.driver, context.WAIT_TIME).until(
        method=EC.presence_of_element_located
        ((By.XPATH, "//div[contains(@class,'carousel__autoplay')]//li[not(@aria-hidden)]")),
        message="Banner element is not presented")
    cur_banner_header = cur_banner.find_element(By.XPATH, "descendant::a//span")
    if cur_banner_header.text != context.cur_banner_text:  # compare with the text from the first step of scenario execution
        raise ValueError(
            f"The banner is not the same as in the beginning of the scenario execution.\nThe actual banner is '{cur_banner_header.text}' and the previous banner is '{context.cur_banner_text}'")

#########################################
# BANNER_CAROUSEL FEATURE METHODS | END #
#########################################

###############################
# LEFT SEARCH METHODS | START #
###############################


# @step("[LeftFilter] Filter '{target_filter_name}': select option '{target_option_name}'")
# def step_impl(context, target_filter_name, target_option_name):
#     filter_widget = WebDriverWait(context.driver, context.WAIT_TIME).until(
#         method=EC.presence_of_element_located
#         ((By.XPATH, f"//div[@class='srp-rail__left']//li[contains(@class,'x-refine')][.//h3[text()='{target_filter_name}']]")),
#         message=f"The filter widget '{target_filter_name}' is not found.")
#     option = filter_widget.find_elements(By.XPATH, f"descendant::div/span[text()='{target_option_name}']")  # one element in list expected
#     if len(option) == 1:
#         option[0].click()
#     else:
#         available_options = []
#         for each in filter_widget.find_elements(By.XPATH, f"descendant::span[@class='cbx x-refine__multi-select-cbx'][./span]"):
#             available_options.append(each.text.split("\n")[0])  # get only 1st line of text with option name, remove number of results
#         raise ValueError(f" The option '{target_option_name}' is missing or presented more than 1 time in the filter widget.\nAvailable options are {available_options}.")


@step("[LeftFilter] Select an option from a filter")
def step_impl(context):
    option_mismatches = {}
    for row in context.table.rows:
        filter_widget = WebDriverWait(context.driver, context.WAIT_TIME).until(method=EC.presence_of_element_located((By.XPATH, f"//div[@class='srp-rail__left']//li[contains(@class,'x-refine')][.//h3[text()='{row[0]}']]")), message=f"The filter widget '{row[0]}' is not found.")
        option = filter_widget.find_elements(By.XPATH, f"descendant::div/span[text()='{row[1]}']")  # one element in list expected
        if len(option) == 1:
            option[0].click()
        else:
            available_options = []
            for each in filter_widget.find_elements(By.XPATH, f"descendant::span[@class='cbx x-refine__multi-select-cbx'][./span]"):
                available_options.append(each.text.split("\n")[0])  # get only 1st line of text with option name, remove number of results
                option_mismatches[row[0]] = available_options
    if option_mismatches:
        raise ValueError(f"'{len(option_mismatches)}' out of '{len(context.table.rows)}' filters have mismatches. Mismatches are {option_mismatches}")


@step("[Results] Collect links to results sub pages")
def step_impl(context):
    result_cards = WebDriverWait(context.driver, context.WAIT_TIME).until(
        method=EC.presence_of_all_elements_located
        (locator=(By.XPATH, "//ul[@class='carousel__list']/following::div[@class='s-item__wrapper clearfix']")),
        message="The left filter widget is not found.")
    for card in result_cards:
        title = card.find_element(By.XPATH, "descendant::span[@role='heading']").text.lower()
        link = card.find_element(By.XPATH, "descendant::a[contains(@class,'link')]").get_attribute("href")
        context.result_links[title] = link  # assign on scenario level

@step("[Results] Verify result titles are related to '{target_option_name}'")
def step_impl(context, target_option_name):
    mismatch_in_title = []
    for title in context.result_links.keys():
        if target_option_name.lower() not in title.lower():
            mismatch_in_title.append(title.lower())
    if mismatch_in_title:
        raise ValueError(f"{len(mismatch_in_title)} results: '{mismatch_in_title}' are not related to search query: '{target_option_name.lower()}'.")

@step("[ResultsSubPage] Verify in spec the label '{exp_label}' matches the value '{exp_value}'")
def step_impl(context, exp_label, exp_value):
    results_page = context.driver.current_window_handle
    mismatch_in_spec = []
    item_spec = {}
    for key in context.result_links.keys():
        context.driver.execute_script(f"window.open('{context.result_links[key]}')")
        context.driver.switch_to.window(context.driver.window_handles[-1])

        # specification = WebDriverWait(context.driver, context.WAIT_TIME).until(method=EC.presence_of_element_located(locator=(By.XPATH, "//div[contains(@class,'section-module-evo')][.//span[text()='Item specifics']]")), message="The specification widget is not found.")
        # labels_text = []
        # values_text = []
        # labels = specification.find_elements(By.XPATH, "descendant::div[@class='ux-labels-values__labels']//span")
        # for l in labels:
        #     labels_text.append(l.text.lower())
        # values = specification.find_elements(By.XPATH, "descendant::div[@class='ux-labels-values__values']//span")
        # for v in values:
        #     values_text.append(v.text.lower())
        # if len(labels_text) != len(values_text):
        #     raise Exception(f"Number of labels '{len(labels_text)}' does not match number of values '{len(values_text)}' for item '{key}'.")
        # item_spec = dict(zip(labels_text, values_text))

        specification = WebDriverWait(context.driver, context.WAIT_TIME).until(method=EC.presence_of_all_elements_located(locator=(By.XPATH, "//div[contains(@class,'section-module-evo')][.//span[text()='Item specifics']]//div[contains(@class,'evo__col')][./div]")), message="The specification widget is not found.")
        # print(len(specification))
        for collection in specification:
            label = collection.find_element(By.XPATH, "descendant::div[@class='ux-labels-values__labels']//span[contains(@class,'ux-textspans')]").text
            value = collection.find_element(By.XPATH, "descendant::div[@class='ux-labels-values__values']//span[contains(@class,'ux-textspans')]").text
            item_spec[label.lower()] = value.lower()
        if exp_label.lower() not in item_spec.keys():
            mismatch_in_spec.append(f"Item '{key}' does not have label '{exp_label.lower()}' in its spec.\n")
        elif exp_value.lower() not in item_spec[exp_label.lower()]:
            mismatch_in_spec.append(f"Item '{key}' has a label '{exp_label.lower()}' in its spec, but value is '{item_spec[exp_label.lower()]}' instead of '{exp_value.lower()}'.")

        context.driver.close()
        context.driver.switch_to.window(results_page)
    if mismatch_in_spec:
        print("The list of mismatches is below:")
        for mismtach in mismatch_in_spec:
            print(mismtach)
        raise ValueError(f"'{len(mismatch_in_spec)}' out of '{len(list(context.result_links))}' results have mismatches.")


#############################
# LEFT SEARCH METHODS | END #
#############################

#################################
# ACTION CHAINS METHODS | START #
#################################

@step("Mouse hover '{exp_category}' category")
def stem_impl(context, exp_category):
    category = WebDriverWait(context.driver, context.WAIT_TIME).until(EC.presence_of_element_located((By.XPATH, f"//div[@class='vl-flyout-nav']//li/a[text()='{exp_category}']")), f"The category '{exp_category}' is not found.")
    action = ActionChains(context.driver)
    action.move_to_element(category)
    action.pause(2)
    action.perform()
    visible_element = WebDriverWait(context.driver, context.WAIT_TIME).until(EC.presence_of_element_located((By.XPATH, "//div[@class='vl-flyout-nav']//li[contains(@class,'__js-show')]/a")), f"The visible category is not found.")
    if exp_category.lower() != visible_element.text.lower():
        raise ValueError(f"The '{visible_element.text.lower()}' element is visible, instead of '{exp_category.lower()}'.")

###############################
# ACTION CHAINS METHODS | END #
###############################
