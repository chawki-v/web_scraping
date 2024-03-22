import scrapy
import csv

class JumiaSpider(scrapy.Spider):
    name = 'jumia_spider'
    allowed_domains = ['jumia.com.tn']
    start_urls = ['https://www.jumia.com.tn/telephone-tablette/']

    def __init__(self):
        super(JumiaSpider, self).__init__() 
        self.csv_file = open('jumia_data.csv', 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)

        self.csv_writer.writerow(['Product URL', 'Category&Subcategory', 'Name', 'Prix', 'Disponibilite', 'Product Image'])

    def closed(self, reason):
        self.csv_file.close()

    def parse(self, response):
        href_urls = response.xpath('//a[@class="core"]/@href').getall()

        for href in href_urls:
            product_url = response.urljoin(href)
            yield scrapy.Request(product_url, callback=self.parse_product)

        next_pages = response.xpath('//a[@class="pg"]/@href').getall()
        for next_page in next_pages:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        cbs_elements = response.xpath('//a[@class="cbs"]/text()').getall()
        cbs_elements = [element for element in cbs_elements if element != "Accueil"]
        cbs = '->'.join(cbs_elements)

        fs20_pts_pbxs = response.xpath('//h1[contains(@class, "-fs20") and contains(@class, "-pts") and contains(@class, "-pbxs")]/text()').get()
        b_ubpt_tal_fs24_prxs = response.xpath('//span[contains(@class, "-b") and contains(@class, "-ubpt") and contains(@class, "-tal") and contains(@class, "-fs24") and contains(@class, "-prxs")]/text()').get()
        df_i_ctr_fs12_pbs_gy5 = response.xpath('//p[contains(@class, "-df") and contains(@class, "-i-ctr") and contains(@class, "-fs12") and contains(@class, "-pbs") and contains(@class, "-gy5")]/text()').get()

        product_image_url = response.xpath('//img[contains(@class, "-fw") and contains(@class, "-fh")]/@data-src').get()

        product_url = response.url

        disponibilite = df_i_ctr_fs12_pbs_gy5 if df_i_ctr_fs12_pbs_gy5 else "there is no data"

        self.csv_writer.writerow([product_url, cbs, fs20_pts_pbxs, b_ubpt_tal_fs24_prxs, disponibilite, product_image_url])
