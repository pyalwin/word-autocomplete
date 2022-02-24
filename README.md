# Word Search

This is a utility to provide autocomplete / search for English
words based on a training [dataset](https://www.dropbox.com/s/8iikupqozxbb9xv/word_search.tsv?dl=0) that contains 333,333 words 
based on the frequency of their usage in some corpus

The api has following endpoints

```
GET /search?word=<input>
```

Constraints used for the search results are as follows

1. The matching should be fuzzy and tolerate typos. For example, both `grtness` and `graetness` should match `greatness`.
2. Matches can occur anywhere in the string, not just at the beginning. For example, `eryx` should match `archaeopteryx` (among others).
3. The ranking of results should satisfy the following:
    1. We assume that the user is typing the beginning of the word. Thus, matches at the start of a word should be ranked higher. For example, for the input `pract`, the result `practical` should be ranked higher than `impractical`.
    2. Common words (those with a higher usage count) should rank higher than rare words.
    3. Short words should rank higher than long words. For example, given the input `environ`, the result `environment` should rank higher than `environmentalism`.
        1. As a corollary to the above, an exact match should always be ranked as the first result.

Approach for this utility as follows

* Load the input dataset into memory
* To identify the most closest result, identify the levenshtein ratio for each of the words in library against the search string
* Order the source based on ratio and frequency of the usage in descending manner
* Return top 25 results

## How to run 

* Create a virtual environment and install the requirements
```
pipenv install
```
* Activate the virtual environment
```
pipenv shell
```
* Run the fastapi server
```
uvicorn main:app
```
Now the service should be accessible at http://127.0.0.1:8000/
