import scrapy


class SecLatestFilingsSpider(scrapy.Spider):
    name = 'sec-latest-filings'
    allowed_domains = ['www.sec.gov']
    start_urls = ['https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=c&owner=include&count=20&action=getcurrent']

    def parse(self, response):
        filings = response.xpath('//div[@style="margin-left: 10px"]/table[2]/tr[@nowrap="nowrap"]')

        for filing in filings:
            # HANDLING FORM C'S ONLY
            if filing.xpath('.//td[1]/text()').get() == 'C':
                filing_date = filing.xpath('.//td[5]/text()').get()
                link = filing.xpath('.//td[2]/a[1]/@href').get()
                absolute_url = f'https://www.sec.gov{link}'
                yield scrapy.Request(url=absolute_url, callback=self.click_through_to_form, meta={'filing_date': filing_date})
            # HANDLING FORM C/A's
            # elif filing.xpath('.//td[1]/text()').get() == 'C/A':
            #     print("I am a C/A")
        yield filings
    
    def click_through_to_form(self, response):
        filing_date = response.request.meta['filing_date']
        link = response.xpath("//table/tr[2]/td[3]/a/@href").get()
        absolute_url = f'https://www.sec.gov{link}'
        
        yield scrapy.Request(url=absolute_url, callback=self.parse_form_c, meta={'filing_date': filing_date})

    def parse_form_c(self, response):
        filing_date = response.request.meta['filing_date']

        cik = response.xpath('//div[@class="content"]/table[@role="presentation"]/tr[1]/td[2]/div/text()').get()
        company_name = response.xpath('//td[text() = "Name of Issuer: "]/following::td[1]/div/text()').get()
        street_address = response.xpath('//td[text() = "Address 1: "]/following::td[1]/div/text()').get()
        city = response.xpath('//td[text() = "City: "]/following::td[1]/div/text()').get()
        state = response.xpath('//td[text() = "State/Country: "]/following::td[1]/div/text()').get()
        zipcode = response.xpath('//td[text() = "Mailing Zip/Postal Code: "]/following::td[1]/div/text()').get()
        website = response.xpath('//td[text() = "Website of Issuer: "]/following::td[1]/div/text()').get()
        intermediary_name = response.xpath('//h4[text() = "Intermediary through which the Offering will be Conducted: "]/following::tr[2]/td[2]/div/text()').get()
        intermediary_cik = response.xpath('//h4[text() = "Intermediary through which the Offering will be Conducted: "]/following::tr[1]/td[2]/div/text()').get()
        offering_type = response.xpath('//td[text() = "Specify: "]/following::td[1]/div/text()').get()
        offering_target = response.xpath('//td[text() = "Target Offering Amount: "]/following::td[1]/div/text()').get()
        offering_maximum = response.xpath('//td[text() = "Maximum Offering Amount (if different from Target Offering Amount): "]/following::td[1]/div/text()').get()
        offering_deadline = response.xpath('//td[text() = "Deadline to reach the Target Offering Amount: "]/following::td[1]/div/text()').get()
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
            'signature_title': signature_title
        }
