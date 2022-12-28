# novel-scraper
Short script that can scrape a novel of royalroad.com and convert it to an ebook.

> NOTE: This script was made for fun. Use it on based on your own judgement.

## Pre-requirements
`pip install -r requirements.txt`

Set following variable on line 46 to the novel you want to scrape & convert.

Example:

`
chapter_url = 'https://www.royalroad.com/fiction/21220/mother-of-learning/chapter/301778/1-good-morning-brother'
`

Also set the following variable on line 100 to the directory you want the book in.

Example: 

`
output_dir = "/home/user/Documents/Books"
`

## Usage
To run:

`python converter.py`

### Example

```
➜ python converter.py 
Chapters: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 108/108 [00:28<00:00,  3.81it/s]
=======================================
Chapters gathered. Creating ebook.
=======================================
Complete 
108 chapters of "Mother of Learning" downloaded and saved to /home/user/Documents/Books/Mother of Learning.epub
```