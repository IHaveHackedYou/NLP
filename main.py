import word_counter

counter = word_counter.NumCounter()
urls = counter.create_gutenberg_urls(num_books=75, start_index=600)
# to 675
counter.iterate_through_urls(urls=urls, filename="word_frequency_2.txt")