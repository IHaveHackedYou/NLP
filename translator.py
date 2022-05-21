from selenium import webdriver
import time
import clipboard
import os
import pandas as pd
import word_counter


def translate_text(text_list, store_file_name):
  PATH = "C:\Program Files (x86)\chromedriver.exe"
  driver = webdriver.Chrome(PATH)
  deepl_url = 'https://www.deepl.com/en/translator'
  driver.get(deepl_url)
  output_list = []
  i = 0
  for text in text_list:
    i += 1
    
    if(i % 100 == 0):
      loaded_output_list = []
      if os.path.exists(store_file_name):
        df = pd.read_csv(store_file_name)
        loaded_output_list = df["translations"].values.tolist()

      list_to_store = loaded_output_list + output_list
      df = pd.DataFrame(data={"translations": list_to_store})
      os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
      df.to_csv(store_file_name)
      output_list = []

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
    clipboard.copy('')

    # Quit selenium driver
    # driver.quit()

    # Display results
    print('_'*50)
    print('Original    :', text)
    print('Translation :', content)
    print('_'*50)
  return output_list

def create_df(words, counts, translations):
  df = pd.DataFrame(data={"counts": counts, "words": words, "translations": translations})
  return df

counter = word_counter.NumCounter()
counter.remove_one_counts(load_filename="word_frequency.txt", store_filename="word_frequency_no_one_counts.txt", counts_to_remove=10)


filename = "word_frequency_no_one_counts.txt"
os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
if os.path.exists(filename):
  df = pd.read_csv(filename)
  words = df["words"].values.tolist()
  counts = df["counts"].values.tolist()
else:
  print("error")


translations = translate_text(words, "translations.txt")


new_filename = "translated_word_frequency.txt"
df = create_df(words, counts, translations)
df = df.sort_values(by="counts", ascending=False)

os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
if os.path.exists(new_filename):
   os.remove(new_filename)
df.to_csv(new_filename)