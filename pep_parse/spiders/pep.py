import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    """Постраничный парсинг PEP-документациии."""

    name = "pep"
    allowed_domains = ["peps.python.org"]
    start_urls = ["https://peps.python.org/"]

    def parse(self, response):
        table = response.css('section#numerical-index')
        links = table.css('tbody a::attr(href)')

        for link in links:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        pep_title = response.css('h1.page-title::text')
        data = {
            'number': pep_title.re_first(r'PEP (\d+)'),
            'name': pep_title.get(),
            'status': response.css(
                'dl dt:contains("Status") + dd abbr::text'
            ).get()
        }
        yield PepParseItem(data)
