import requests
import bs4
import pypandoc
import os
import re
from tqdm import tqdm


# Getting the HTML content from the chapter page
def get_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

# Parse the HTML and get only the text containing the actual chapter. prettify() is used to keep the formatting (paragraphs).
def parse_html(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    chapter_text = soup.find('div', {'class': 'chapter-inner chapter-content'}).prettify()
    return chapter_text

# Same as above but only used for getting the book title
def get_book_title(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    # This is the HTML element that contains the book title.
    title_element = soup.find('h2', {'class': 'font-white'})
    if title_element:
        return title_element.text
    else:
        return ''

# Parse the HTML and get the title of the chapter.
def get_chapter_title(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    title_element = soup.find('h1', {'class': 'font-white'})
    if title_element:
        return title_element.text
    else:
        return ''

# Convert the data that was gathered to a ebook. Save it to the designated output directory.
def convert_to_epub(text, title, output_file):
    pypandoc.convert_text(text, 'epub', format='html', outputfile=output_file, extra_args=['--columns=10000', f'--metadata=title:{title}'])

def main():
    # Here we set the URL to the first chapter of the book
    chapter_url = 'https://www.royalroad.com/fiction/21220/mother-of-learning/chapter/301778/1-good-morning-brother'


    # Below we are essentially going back to the main page of the book to gather number of chapters. 
    # This is for creating a progress bar.

    # Extract the novel_id component - e.g 345678 and the novel name.
    novel_id = re.search(r'https://www\.royalroad\.com/fiction/(\d+)/', chapter_url).group(1)
    novel_name = re.search(r'https://www\.royalroad\.com/fiction/\d+/([^/]+)/', chapter_url).group(1)

    # Fetch and parse the HTML to get the number of chapters for the novel
    response_num_chapters = requests.get('https://www.royalroad.com/fiction/'+novel_id+"/"+novel_name)
    main_page_soup = bs4.BeautifulSoup(response_num_chapters.text, 'html.parser')

    # Find the span element containing the number of chapters
    span_element = main_page_soup.find('span', {'class': 'label label-default pull-right'})

    # Get the number of chapters from the text. Convert to integer.
    text_t = span_element.text
    matches = re.findall(r'\d+', text_t)
    num_chapters = int(matches[0])
    counter = 0
    # Initialize an empty list to store the chapters
    chapters = []

    # Initialize the progress bar
    with tqdm(total=num_chapters, desc='Chapters') as pbar:
        while True:
            html = get_html(chapter_url)
            chapter_text = parse_html(html)
            chapter_title = get_chapter_title(html)
            chapters.append((chapter_title, chapter_text))
            pbar.update(1)

            # Since we want all the chapters, we need to make the script continue to the next one
            # if it exists. We do this by using Soup to find the link to the next chapter.
            soup = bs4.BeautifulSoup(html, 'html.parser')
            next_link_element = soup.find('link', {'rel': 'next'})
            next_link = next_link_element['href'] if next_link_element else None
            if next_link:
                # If there is a link to the next chapter, update the URL and continue the loop
                chapter_url = "https://www.royalroad.com" + next_link
            else:
                break
    print("=" *39)
    print("Chapters gathered. Creating ebook.")

    book_title = get_book_title(html)

    # Combine all the chapters into a single string
    book_text = '\n\n'.join([f'<h1>{title}</h1>\n{text}' for title, text in chapters])

    # Set the output file and directory for the book.
    # Convert the book to epub format and save it.
    output_dir = "/home/user/Documents/Books"
    output_file = os.path.join(output_dir, book_title + '.epub')
    convert_to_epub(book_text, book_title, output_file)

    # Print end summary
    print("=" *39)
    print('\033[32m' + 'Complete ' + '\033[0m')
    print(f'{len(chapters)} chapters of "{book_title}" downloaded and saved to {output_file}')


if __name__ == '__main__':
    main()
