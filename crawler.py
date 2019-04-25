# -*- coding: utf-8 -*-
import scrapy


class CrawlerSpider(scrapy.Spider):
    name = "webcrawler"
    allowed_domains = ['milliyet.com.tr']
    start_urls = ['http://www.milliyet.com.tr/gundem-tumhaberler/?PAGE=334']
    
    def parse(self, response):
        haberler = response.css('div.katNews2 > ul > li > a.nHText::attr(href)').extract()
                
        for haber in haberler:
            haber = response.urljoin(haber)
            yield scrapy.Request(url=haber, callback=self.parse_details)
        
        prev_page_url = response.css('li.pBck > a::attr(href)').extract_first()
        if prev_page_url:
           prev_page_url = response.urljoin(prev_page_url)
        yield scrapy.Request(url=prev_page_url, callback=self.parse)
   
    def parse_details(self, response):
        tarih = response.xpath('//*[@id="_MiddleLeft1"]/div[1]/div/div[2]/div[2]/div/div[1]//text()').extract()
        baslik = response.css('div.headSpot > h1::text').extract_first()
        icerik = response.xpath('//*[@id="articleBody"]/p//text()').extract()
        konu = "gundem"
        yield {
            'tarih': tarih,
            'baslik': baslik,
            'icerik': icerik,
            'konu' : konu
        }
        
