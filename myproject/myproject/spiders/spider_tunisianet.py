import scrapy

class ProductSpider(scrapy.Spider):
    name = 'product_spider'
    start_urls = ['https://www.tunisianet.com.tn/377-telephone-portable-tunisie']

    def parse(self, response):
        products = response.xpath("//div[contains(@class, 'item-product col-xs-12')]")
        for product in products:
            
            product_name = product.xpath(".//h2[contains(@class, 'h3 product-title')]/a/text()").get()
            price = product.xpath(".//span[contains(@class, 'price')]/text()").get()
            product_description = product.xpath(".//div[contains(@class, 'listds')]/a/text()").get()
            availability = product.xpath(".//span[contains(@class, 'in-stock')]/text()").get()
            image_url = product.xpath(".//img[contains(@class, 'center-block')]/@src").get()

            yield {
                'product_name': product_name.strip() if product_name else None,
                'price': price.strip() if price else None,
                'product_description': product_description.strip() if product_description else None,
                'availability': availability.strip() if availability else None,
                'image_url': image_url.strip() if image_url else None
            }

        pagination_links = response.xpath("//a[contains(@class, 'js-search-link')]/@href").getall()
        for link in pagination_links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse)
