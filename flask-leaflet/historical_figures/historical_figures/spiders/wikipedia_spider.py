import scrapy
from scrapy.crawler import CrawlerProcess
import sqlite3

class WikipediaSpider(scrapy.Spider):
    name = "spider"
    
    def __init__(self, figure_name=None, *args, **kwargs):
        super(WikipediaSpider, self).__init__(*args, **kwargs)
        """
        if figure_name:
            self.start_urls = [f'https://en.wikipedia.org/wiki/{figure_name.replace(" ", "_")}']
            self.figure_name = figure_name  # Store figure name for logging and database entry
        else:
            raise ValueError("A figure name must be provided to initialize the WikipediaSpider.")
        """
        figure_name = "Albert Einstein"
        if figure_name:
            self.start_urls = [f'https://en.wikipedia.org/wiki/{figure_name.replace(" ", "_")}']
            self.figure_name = figure_name  # Store figure name for logging and database entry
        else:
            raise ValueError("A figure name must be provided to initialize the WikipediaSpider.")
        
    
    def parse(self, response):
        # Extract the figure's name from the heading
        figure_name = response.xpath('//h1[@id="firstHeading"]/span/text()').get()
        
        if not figure_name:
            self.log("No name found in the heading.")
            return  # Stop if no name is found

        # Extract the infobox table
        infobox = response.xpath('//table[contains(@class, "infobox biography vcard")]')

        if not infobox:
            self.log(f"No infobox found for {self.start_urls[0]}")
            return  # Stop if no infobox is found

        # Dictionary to hold the extracted data
        biography_info = {"name": figure_name}
        
        # Extract each row in the infobox
        for row in infobox.xpath('.//tr'):
            label = row.xpath('.//th/text()').get()
            data = row.xpath('.//td//text()').extract()
            print((label,data))
            # Clean the data
            data = [d.strip() for d in data if d.strip()]
            
            if label:
                biography_info[label] = " ".join(data)

        # Save the scraped data to the database
        self.save_to_database(biography_info)

    def save_to_database(self, biography_info):
        # Connect to the database
        conn = sqlite3.connect('../../historical_figures.db')
        cursor = conn.cursor()

        # Insert figure into `figures` table
        cursor.execute('INSERT INTO figures (name) VALUES (?)', (biography_info['name'],))
        figure_id = cursor.lastrowid  # Get the ID of the newly inserted figure

        # Insert attributes into `attributes` table
        for key, value in biography_info.items():
            if key != 'name':
                cursor.execute('INSERT INTO attributes (figure_id, attribute_name, attribute_value) VALUES (?, ?, ?)', 
                               (figure_id, key, value))

        # Commit and close
        conn.commit()
        conn.close()
