import word_counter

counter = word_counter.NumCounter()
urls = counter.create_gutenberg_urls(num_books=400, start_index=1600)
# to 2000
counter.iterate_through_urls(urls=urls, filename="word_frequency.txt")
# counter.remove_one_counts("word_frequency.txt")
# df = counter.normalize_counts(filename="word_frequency.txt")
# print(df)