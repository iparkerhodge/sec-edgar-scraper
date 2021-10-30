import scrapy


class Seeder2Spider(scrapy.Spider):
    name = 'seeder2'
    allowed_domains = ['www.sec.gov']
    start_urls = ['https://www.sec.gov/cgi-bin/srch-edgar?text=form-type+%3D+c&first=2014&last=2019']

    def parse(self, response):
        filings = response.xpath('//center/following::table/tr')

        for filing in filings:
            filing_date = filing.xpath('.//td[5]/text()').get()
            link = filing.xpath('.//td[2]/a[1]/@href').get()
            absolute_url = f'https://www.sec.gov{link}'
            yield scrapy.Request(url=absolute_url, callback=self.click_through_to_form, meta={'filing_date': filing_date})

        next_page = response.xpath(
            '//center[1]/a[text() = "[NEXT]"][1]/@href').get()
        absolute_url = f'https://www.sec.gov{next_page}'

        if next_page:
            yield scrapy.Request(url=absolute_url, callback=self.parse)
    
    def click_through_to_form(self, response):
        filing_date = response.request.meta['filing_date']
        link = response.xpath("//table/tr[2]/td[3]/a/@href").get()
        absolute_url = f'https://www.sec.gov{link}'
        
        yield scrapy.Request(url=absolute_url, callback=self.parse_form_c, meta={'filing_date': filing_date, 'url': absolute_url})

    def parse_form_c(self, response):
        filing_date = response.request.meta['filing_date']
        form_c_url = response.request.meta['url']

        cik = response.xpath('//div[@class="content"]/table[@role="presentation"]/tr[1]/td[2]/div/text()').get()
        company_name = response.xpath('//td[text() = "Name of Issuer: "]/following::td[1]/div/text()').get()
        street_address = response.xpath('//td[text() = "Address 1: "]/following::td[1]/div/text()').get()
        city = response.xpath('//td[text() = "City: "]/following::td[1]/div/text()').get()
        state = response.xpath('//td[text() = "State/Country: "]/following::td[1]/div/text()').get()
        zipcode = response.xpath('//td[text() = "Mailing Zip/Postal Code: "]/following::td[1]/div/text()').get()
        website = response.xpath('//td[text() = "Website of Issuer: "]/following::td[1]/div/text()').get()
        intermediary_name = response.xpath('//h4[text() = "Intermediary through which the Offering will be Conducted: "]/following::tr[2]/td[2]/div/text()').get()
        intermediary_cik = response.xpath('//h4[text() = "Intermediary through which the Offering will be Conducted: "]/following::tr[1]/td[2]/div/text()').get()
        offering_type = response.xpath('//td[contains(text(), "Type of Security Offered")]/following::td[1]/div/text()').get()
        offering_target = response.xpath('//td[text() = "Target Offering Amount: "]/following::td[1]/div/text()').get()
        offering_maximum = response.xpath('//td[contains(text(), "Maximum Offering Amount")]/following::td[1]/div/div/text()').get()
        offering_deadline = response.xpath('//td[contains(text(), "Deadline to reach")]/following::td[1]/div/div/text()').get()
        signature_name = response.xpath('//td[text() = "Signature: "]/following::td[1]/div/text()').get()
        signature_title = response.xpath('//td[text() = "Title: "]/following::td[1]/div/text()').get()

        cleaned_state = state.replace("\n\t\t\t\t", '').replace("\n\t\t\t", '')

        yield {
            'cik': cik,
            'company_name': company_name,
            'street_address': street_address,
            'city': city,
            'state': cleaned_state,
            'zipcode': zipcode,
            'website': website,
            'intermediary_name': intermediary_name,
            'intermediary_cik': intermediary_cik,
            'offering_type': offering_type,
            'offering_target': offering_target,
            'offering_maximum': offering_maximum,
            'offering_deadline': offering_deadline,
            'signature_name': signature_name,
            'signature_title': signature_title,
            'form_c_url': form_c_url,
            'filing_date': filing_date
        }
