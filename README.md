# Bloom Proof

## Description

A simple website using Flask to demonstrate using a Bloom Filter to check text for spelling mistakes. The inspiration
for this project was [this coding challenge](https://codingchallenges.fyi/challenges/challenge-bloom/).

## How it Works

Once the flask server is started, the user must load a dictionary of words into it to be used for spell checking. This
is done with `flask load dict.txt` using the provided dict.txt from this repository 
(generated with `cat /usr/share/dict/words >> dict.txt`). This loads the dictionary into a Bloom Filter that I
implemented off of the [Wikipedia article](https://en.wikipedia.org/wiki/Bloom_filter) on Bloom Filters.

Once the Bloom Filter is loaded, it is then dumped to a file, `filter.bf`. Headers are written to it, including an 
identifier for the file "BPBF" (Bloom Proof Bloom Filter), the number of hash functions used, and the size of the
bit array. 

When a POST request is made to the `/check` endpoint containing a payload of text, the Bloom Filter is loaded from the
`filter.bf` file and queried using the words from the payload. Any words not found within the Bloom Filter are sent
back to the user to indicate they are misspelled. Yes, I know loading the Bloom Filter from disk each time is not 
efficient, but the purpose of this app is really to demonstrate the use of the Bloom Filter. 

## Tools/Structures Used

* Poetry (Python dependency/venv management)
* Flask (server)
* Jinja (HTML templating)
* Click (CLI)
* HTMX (for simple interactivity within the website)
* Bloom Filter implementation (for spell checking)

## Demo

![Demo](demo.gif)