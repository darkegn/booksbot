import scrapy

class GarantiCampaignSpider(scrapy.Spider):
    name = "garanti_campaigns"
    allowed_domains = ["garantibbva.com.tr"]
    start_urls = [
        'https://www.garantibbva.com.tr/kampanyalar',
    ]

    def parse(self, response):
        for promotion_url in response.css("div.card__griditem a ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(promotion_url), callback=self.parse_promotion_page)
        next_page = response.css("a.pagination__next ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_promotion_page(self, response):
        item = {}
        item["title"] = response.css("div.card-title ::text").extract_first()
        item['image_url'] = response.css("img.lozad ::attr(data-src)").extract_first()
        item['description'] = response.css("div.card-content ::text").extract_first()
        yield item
