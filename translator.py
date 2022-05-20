from selenium import webdriver
import time
import clipboard
def translate_text(text_list):
  PATH = "C:\Program Files (x86)\chromedriver.exe"
  driver = webdriver.Chrome(PATH)
  deepl_url = 'https://www.deepl.com/en/translator'
  driver.get(deepl_url)
  output_list = []
  for text in text_list:
    # Get thie inupt_area 
    input_css = 'div.lmt__inner_textarea_container textarea'
    input_area = driver.find_element_by_css_selector(input_css)

    # Send the text
    input_area.clear() 
    input_area.send_keys(text)

    # Wait for translation to appear on the web page
    time.sleep(3)

    # Get copybutton and click on it
    # button_css = 'span.deepl-ui-' 
    # button = driver.find_element_by_css_selector(button_css)
    button = driver.find_element_by_class_name("lmt__target_toolbar_right")
    button.find_element_by_tag_name("button").click()
    # button.click()

    # Get content from clipboard
    content = clipboard.paste()
    output_list.append(content)

    # Quit selenium driver
    # driver.quit()

    # Display results
    print('_'*50)
    print('Original    :', text)
    print('Translation :', content)
    print('_'*50)
  return output_list

print(translate_text(["I am a student", "you are a student"]))

  