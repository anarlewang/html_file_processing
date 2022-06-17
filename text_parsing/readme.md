This is the updated version of text parsing.

Usage:

import text_search

text_search.find_keyword_in_files(['CAPM',"cost of capital"],"data","2018-12-01","2018-12-31")

This will return a dictionary of filenames with keywords that presented in search. Searched keywords in a file as keys would have a value corresponding to the location its first appearance in the text.
