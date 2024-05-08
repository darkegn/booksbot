import scrapy


class GarantiCampaignSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["garantibbva.com.tr"]
    start_urls = [
        'https://www.garantibbva.com.tr/kampanyalar',
    ]

    def parse(self, response):
        for promotion_url in response.css("div.promotion-list-item a.promotion-detail ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(promotion_url), callback=self.parse_promotion_page)
        next_page = response.css("a.pagination-next ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_promotion_page(self, response):
        item = {}
        item["title"] = response.css("h1.promotion-detail-header ::text").extract_first()
        item['category'] = response.css("span.promotion-category ::text").extract_first()
        item['description'] = response.css("div.promotion-detail-text ::text").extract_first()
        item['validity'] = response.css("div.promotion-detail-text > p:nth-of-type(1) strong ::text").extract_first()
        item['conditions'] = "\n".join(response.css("div.promotion-detail-text ul > li ::text").extract())
        yield item
