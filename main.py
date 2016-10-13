import requests
from functions import *
import time
from time import time
import urlparse
import sys
from tqdm import *
from xmlutils.xml2csv import xml2csv
import shutil

t0 = time()

category_list = ["term-life", "whole-life"]
date_list = initialise_date_list()
gender_list = ["M", "F"]
smoker_list = ["Y", "N"]
termlife_coverage_term_list = ["5%20Years", "20%20Years", "To%20Age%2065"]
wholelife_coverage_term_list = ["To%20age%2070","To%20age%2085"]
termlife_sum_assured_list = ["50000", "100000", "200000", "300000", "400000"]
wholelife_sum_assured_list = ["50000", "100000", "200000"]
crit_ill_list = ["Y", "N"]
DPIP_search_dict = initialise_search_dict()
search_dict_col_order = ["category", "date_of_birth", "gender", "smoker", "coverage_term", "sum_assured", "critical_illness", "policies_available"]

url = "http://www.comparefirst.sg/wap/searchProductsEvent.action"
request_list = []

sample_termlife_request = "PremAnnualGroup=select&PremSingleGroup=select&ProdsCompIDs=null&ProdsVisibleIDs=null&SATLAll=select&SATLDCIPS=50000&SATLNonDCIPS=select&SAWLAll=select&SAWLDCIPS=select&SAWLNonDCIPS=select&breadCrumb=null&coverageTermEndow=select&coverageTermTLAllList=select&coverageTermTLDCIPs=5%20Years&coverageTermTLNonDCIP=select&dob=01%2F01%2F1980&gaSearchSummary=null&pageAction=search&premiumTermAll=select&premiumTermDcips=select&premiumTermNonDcips=select&premiumTypeDCIPs=Annual&premiumTypeOther=Annual&prodGroup=bips&prodStringXML=&prodSummaryTxt=&productGroup=invst&reportProdsCompIDs=null&searchResIncCount=5&searchResInitCount=10&searchproduct=&selCIRider=Y&selCategory=term-life&selGender=F&selSmokStatus=Y&sortEndoGroup=select&sortNonWLGroup=1&sortOrderSelected=null&sortWLGroup=select&subCatCountJson=null&subCatSeleJson=null&viewProdsId=null"

sample_wholelife_request = "PremAnnualGroup=select&PremSingleGroup=select&ProdsCompIDs=null&ProdsVisibleIDs=null&SATLAll=select&SATLDCIPS=50000&SATLNonDCIPS=select&SAWLAll=select&SAWLDCIPS=50000&SAWLNonDCIPS=select&breadCrumb=null&coverageTermEndow=select&coverageTermTLAllList=select&coverageTermTLDCIPs=5%20Years&coverageTermTLNonDCIP=select&dob=01%2F01%2F1980&gaSearchSummary=null&pageAction=search&premiumTermAll=select&premiumTermDcips=To%20age%2070&premiumTermNonDcips=select&premiumTypeDCIPs=Annual&premiumTypeOther=Annual&prodGroup=bips&prodStringXML=&prodSummaryTxt=&productGroup=invst&reportProdsCompIDs=null&searchResIncCount=5&searchResInitCount=10&searchproduct=&selCIRider=Y&selCategory=whole-life&selGender=M&selSmokStatus=Y&sortEndoGroup=select&sortNonWLGroup=1&sortOrderSelected=null&sortWLGroup=3&subCatCountJson=null&subCatSeleJson=null&viewProdsId=null"

# Scraping Term Life
category = category_list[0]
count = 1
request = sample_termlife_request

for gender in gender_list:
    request = edit_gender(request, gender)
    
    for smoker in smoker_list:
        request = edit_smoker(request, smoker)

        for term in termlife_coverage_term_list:
            request = edit_coverage_term(request, term)

            for assured in termlife_sum_assured_list:
                request = edit_sum_assured(request, assured)

                for crit_ill in crit_ill_list:
                    request = edit_crit_ill(request, crit_ill)

                    for date in date_list:
                        request = edit_date(request, date)
                        #print count, request
                        request_list.append(request)
                        store_search_parameters(category, gender, smoker, term, assured, crit_ill, date, DPIP_search_dict)
                        count += 1


# Scraping Whole life
category = category_list[1]
request = sample_wholelife_request

for gender in gender_list:
    request = edit_gender(request, gender)
    
    for smoker in smoker_list:
        request = edit_smoker(request, smoker)

        for term in wholelife_coverage_term_list:
            request = edit_coverage_term(request, term)

            for assured in wholelife_sum_assured_list:
                request = edit_sum_assured(request, assured)

                for crit_ill in crit_ill_list:
                    request = edit_crit_ill(request, crit_ill)

                    for date in date_list:
                        request = edit_date(request, date)
                        #   print count, request
                        request_list.append(request)
                        store_search_parameters(category, gender, smoker, term, assured, crit_ill, date, DPIP_search_dict)
                        count += 1


print "request list generated!", "Total requests:", len(request_list)

term_life_file = open('dpip_term_life.xml', 'w')
whole_life_file = open('dpip_whole_life.xml', 'w')
term_life_file.write('<ProdList>')
whole_life_file.write('<ProdList>')

count = 1
for request in tqdm(request_list):
    
    payload = request
    
    headers = {
        'origin': "http://www.comparefirst.sg",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'referer': "http://www.comparefirst.sg/wap/homeEvent.action",
        'accept-encoding': "gzip, deflate",
        'accept-language': "en-GB,en-US;q=0.8,en;q=0.6",
        'cookie': "autoVisit=1; _gat=1; _ga=GA1.2.460574506.1473850351; JSESSIONID-PROD_WAF_POOL=DOKDCBAK; JSESSIONID=\"k2U5WX+O8O56ltRtWo5iOzBG.host2:station2\"; disclaimerVisit=1; _ga=GA1.2.460574506.1473850351; JSESSIONID-PROD_WAF_POOL=DOKDCBAK",
        'cache-control': "no-cache",
        'postman-token': "c3d7bf8c-127c-d75c-4bcc-e9b29cec3b36"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    s = response.text
    start = '''prodStringXML" value='''
    end = '''/>'''
    s = find_between(s, start, end)[1:-1]
    s = sanitize_HTML_to_XML(s)

    prod_summary_text_url = get_prod_summary_text_url(s)
    dirty_summary_text = requests.request('GET', prod_summary_text_url).text
    summary_text = sanitize_summary_text(dirty_summary_text)

    query = urlparse.parse_qs(request)
    searchStartTerm = '<Product>'
    replaceStartTerm = ('<Product>'
        '<CategoryList>' + DPIP_search_dict["category"][count - 1] + '</CategoryList>'
        '<Date>' + DPIP_search_dict["date_of_birth"][count - 1] + '</Date>'
        '<Gender>' + DPIP_search_dict["gender"][count - 1] + '</Gender>'
        '<Smoker>' + DPIP_search_dict["smoker"][count - 1] + '</Smoker>'
        '<CoverageTerm>' + DPIP_search_dict["coverage_term"][count - 1] + '</CoverageTerm>'
        '<SumAssured>' + DPIP_search_dict["sum_assured"][count - 1] + '</SumAssured>'
        '<CriticalIllness>' + DPIP_search_dict["critical_illness"][count - 1] + '</CriticalIllness>')

    searchEndTerm = '</Product>'
    replaceEndTerm = ('<SummaryText>' + summary_text + '</SummaryText>'
        '</Product>')

    s = s.replace(searchStartTerm, replaceStartTerm)
    s = s.replace(searchEndTerm, replaceEndTerm)

    # if count < 3:
    #     filename = "output" + str(count) + ".xml"
    #     with open(filename, "w") as text_file:
    #         text_file.write(s)

    s = s.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '')
    s = s.replace('<ProdList>', '')
    s = s.replace('</ProdList>', '')
    s = s.replace('<ProdList/>', '')

    if DPIP_search_dict["category"][count - 1] == 'term-life':
        file_to_write = term_life_file
    elif DPIP_search_dict["category"][count - 1] == 'whole-life':
        file_to_write = whole_life_file

    file_to_write.write(s)
    file_to_write.flush()


    count += 1


term_life_file.write('</ProdList>')
term_life_file.close()
whole_life_file.write('</ProdList>')
whole_life_file.close()

term_life_xml_file = xml2csv('dpip_term_life.xml', 'dpip_term_life_preheaders.csv', encoding='utf-8')
term_life_xml_file.convert(tag='Product')
whole_life_xml_file = xml2csv('dpip_whole_life.xml', 'dpip_whole_life_preheaders.csv', encoding='utf-8')
whole_life_xml_file.convert(tag='Product')

fix_headers("dpip_term_life_preheaders.csv", "dpip_term_life.csv")
fix_headers("dpip_whole_life_preheaders.csv", "dpip_whole_life.csv")

print "Total time taken:", int((round(time()-t0, 3))/60), "min", (round(time()-t0, 3))%60, "s"

