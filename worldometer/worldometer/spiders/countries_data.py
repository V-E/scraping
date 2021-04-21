# -*- coding: utf-8 -*-
import scrapy


def sanitize(value):
    if (not value) or (value.strip() == ''):
        return 0

    index = 1 if '+' in value else 0

    return float(''.join(value.strip().split('+')[index].split(',')))


def toggle_country(check1, check2):
    if not check1:
        return check2
    return check1


class CountriesDataSpider(scrapy.Spider):
    name = 'countries_data'
    allowed_domains = ['https://www.worldometers.info/coronavirus/']
    start_urls = ['https://www.worldometers.info/coronavirus/']

    def parse(self, response):
        rows = response.xpath('//table[@id="main_table_countries_today"]/tbody[1]/tr[not(contains(@style,"display: none"))]')
        for row in rows[1:-1]:
            yield {
                'country': toggle_country(row.xpath('td[2]/a/text()').get(), row.xpath('td[2]/span/text()').get()),
                'total_cases': sanitize(row.xpath('td[3]/text()').get()),
                'new_cases': sanitize(row.xpath('td[4]/text()').get()),
                'total_death': sanitize(row.xpath('td[5]/text()').get()),
                'new_death': sanitize(row.xpath('td[6]/text()').get()),
                'total_recovered': sanitize(row.xpath('td[7]/text()').get()),
                'active_cases': sanitize(row.xpath('td[8]/text()').get()),
                'serious_critical': sanitize(row.xpath('td[9]/text()').get()),
                'total_cases_per_million': sanitize(row.xpath('td[10]/text()').get()),
                'death_per_million': sanitize(row.xpath('td[11]/text()').get()),
                'total_tests': sanitize(row.xpath('td[12]/text()').get()),
                'tests_per_million': sanitize(row.xpath('td[13]/text()').get()),
                'population': sanitize(row.xpath('td[14]/text()').get()),
            }
