import word_counter
import pandas as pd

counter = word_counter.NumCounter()
txt = counter.get_all_text_old("https://www.gutenberg.org/files/1342/1342-0.txt")

f = open("extern_list.txt", "r")
listItems = f.read().splitlines()
print(len(listItems))