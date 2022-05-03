import word_counter

counter = word_counter.NumCounter()
urls = counter.create_gutenberg_urls(num_books=50, start_index=950)
# to 1000
# counter.remove_one_counts("word_frequency.txt")
counter.iterate_through_urls(urls=urls, filename="word_frequency.txt")