from typing import Any

import scrapy
from scrapy.http import Response


class TechnologiesSpider(scrapy.Spider):
    name = "technologies"
    allowed_domains = ["djinni.co"]
    start_urls = ["https://djinni.co/jobs/?primary_keyword=Python"]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        for position in response.css("a.job-list-item__link"):
            detail_url = position.css("a.job-list-item__link::attr(href)").get()
            if detail_url:
                yield {
                    "position": position.css("a::text").get().strip("\n "),
                }
        if response.css(".pagination") is not None:
            next_page = response.css(".pagination > li")[-1].css("a::attr(href)").get()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
