import datetime
import time
import shutil

def initialise_search_dict():
    DPIP_search_dict = {}
    DPIP_search_dict["category"] = []
    DPIP_search_dict["date_of_birth"] = []
    DPIP_search_dict["gender"] = []
    DPIP_search_dict["smoker"] = []
    DPIP_search_dict["coverage_term"] = []
    DPIP_search_dict["sum_assured"] = []
    DPIP_search_dict["critical_illness"] = []
    DPIP_search_dict["policies_available"] = [] #policies will be lumped into a string then added as a list for each search result

    return DPIP_search_dict

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def sanitize_HTML_to_XML(s):
    sanitize_dict = {"&gt;":">", "&lt;":"<", '&quot;':'"', "&apos;":"'"}

    for key, value in sanitize_dict.iteritems():
        s = s.replace(key, value)

    return s

def initialise_date_list():
    date_list=[]
    cur_year = 1980#int(datetime.datetime.now().year)
    year = cur_year
    while cur_year-year < 1:
        date = "01%2F01%2F"+str(year)
        date_list.append(date)
        year -= 1

    return date_list

def edit_gender(request, gender):
    index_to_change = request.index("selGender=") + len( "selGender=" )
    ls = list(request)
    ls[index_to_change] = gender
    request = "".join(ls)
    return request

def edit_smoker(request, smoker):
    index_to_change = request.index("selSmokStatus=") + len( "selSmokStatus=" )
    ls = list(request)
    ls[index_to_change] = smoker
    request = "".join(ls)
    return request

def edit_coverage_term(request, term):
    start = request.index("premiumTermDcips=") + len( "premiumTermDcips=" )
    end = request.index( "&", start )
    ls = list(request)
    ls[start:end] = ""
    request = "".join(ls)
    request = request[:start] + term + request[start:]
    return request

def edit_sum_assured(request, assured):
    start = request.index("SAWLDCIPS=") + len( "SAWLDCIPS=" )
    end = request.index( "&", start )
    ls = list(request)
    ls[start:end] = ""
    request = "".join(ls)
    request = request[:start] + assured + request[start:]
    return request

def edit_crit_ill(request, crit_ill):
    index_to_change = request.index("selCIRider=") + len( "selCIRider=" )
    ls = list(request)
    ls[index_to_change] = crit_ill
    request = "".join(ls)
    return request

def edit_date(request, date):
    start = request.index("dob=") + len( "dob=" )
    end = request.index( "&", start )
    ls = list(request)
    ls[start:end] = ""
    request = "".join(ls)
    request = request[:start] + date + request[start:]
    return request

def store_search_parameters(category, gender, smoker, term, assured, crit_ill, date, DPIP_search_dict):
    DPIP_search_dict["category"].append(category)
    DPIP_search_dict["date_of_birth"].append(date.replace('%2F', '/'))
    DPIP_search_dict["gender"].append(gender)
    DPIP_search_dict["smoker"].append(smoker)
    DPIP_search_dict["coverage_term"].append(term.replace('%20', ' '))
    DPIP_search_dict["sum_assured"].append(assured)
    DPIP_search_dict["critical_illness"].append(crit_ill)
    #DPIP_search_dict["policies_available"]

def get_prod_summary_text_url(s):
    elemStartTag = '<ProductSummary3>'
    elemEndTag = '</ProductSummary3>'
    startIndex = s.find(elemStartTag)
    endIndex = s.find(elemEndTag)
    url_path = s[startIndex + len(elemStartTag):endIndex]
    base_url = 'http://www.comparefirst.sg/wap/prodsummary/'
    return base_url + url_path

def sanitize_summary_text(txt):
    remove_elems = ['[Bold]', '[End_Bold]', '[UnderLine]', '[End_UnderLine]', '[Bullet]', '[NewLine]']
    for elem in remove_elems:
        txt = txt.replace(elem, '')

    txt = txt.replace('&', '&amp;')

    return txt

def fix_headers(file_preheaders, file_correctedheaders):
    from_file = open(file_preheaders, "r")
    to_file = open(file_correctedheaders, "w")
    headers = from_file.readline()
    to_remove = "SumAssured_CoverageTerm_"
    corrected_headers = headers.replace(to_remove, "")
    to_file.write(corrected_headers)
    shutil.copyfileobj(from_file, to_file)
    from_file.close()
    to_file.close()

    return



#PremAnnualGroup=select&PremSingleGroup=select&ProdsCompIDs=null&ProdsVisibleIDs=null&SATLAll=select&SATLDCIPS=50000&SATLNonDCIPS=select&SAWLAll=select&SAWLDCIPS=50000&SAWLNonDCIPS=select&breadCrumb=null&coverageTermEndow=select&coverageTermTLAllList=select&coverageTermTLDCIPs=5%20Years&coverageTermTLNonDCIP=select&dob=01%2F01%2F1980&gaSearchSummary=null&pageAction=search&premiumTermAll=select&premiumTermDcips=To%20age%2070&premiumTermNonDcips=select&premiumTypeDCIPs=Annual&premiumTypeOther=Annual&prodGroup=bips&prodStringXML=&prodSummaryTxt=&productGroup=invst&reportProdsCompIDs=null&searchResIncCount=5&searchResInitCount=10&searchproduct=&selCIRider=Y&selCategory=whole-life&selGender=M&selSmokStatus=Y&sortEndoGroup=select&sortNonWLGroup=1&sortOrderSelected=null&sortWLGroup=3&subCatCountJson=null&subCatSeleJson=null&viewProdsId=null
#PremAnnualGroup=select&PremSingleGroup=select&ProdsCompIDs=null&ProdsVisibleIDs=null&SATLAll=select&SATLDCIPS=50000&SATLNonDCIPS=select&SAWLAll=select&SAWLDCIPS=50000&SAWLNonDCIPS=select&breadCrumb=null&coverageTermEndow=select&coverageTermTLAllList=select&coverageTermTLDCIPs=5%20Years&coverageTermTLNonDCIP=select&dob=01%2F01%2F1980&gaSearchSummary=null&pageAction=search&premiumTermAll=select&premiumTermDcips=To%20age%2085&premiumTermNonDcips=select&premiumTypeDCIPs=Annual&premiumTypeOther=Annual&prodGroup=bips&prodStringXML=&prodSummaryTxt=&productGroup=invst&reportProdsCompIDs=null&searchResIncCount=5&searchResInitCount=10&searchproduct=&selCIRider=Y&selCategory=whole-life&selGender=M&selSmokStatus=Y&sortEndoGroup=select&sortNonWLGroup=1&sortOrderSelected=null&sortWLGroup=3&subCatCountJson=null&subCatSeleJson=null&viewProdsId=null
#PremAnnualGroup=select&PremSingleGroup=select&ProdsCompIDs=null&ProdsVisibleIDs=null&SATLAll=select&SATLDCIPS=50000&SATLNonDCIPS=select&SAWLAll=select&SAWLDCIPS=100000&SAWLNonDCIPS=select&breadCrumb=null&coverageTermEndow=select&coverageTermTLAllList=select&coverageTermTLDCIPs=5%20Years&coverageTermTLNonDCIP=select&dob=01%2F01%2F1980&gaSearchSummary=null&pageAction=search&premiumTermAll=select&premiumTermDcips=To%20age%2085&premiumTermNonDcips=select&premiumTypeDCIPs=Annual&premiumTypeOther=Annual&prodGroup=bips&prodStringXML=&prodSummaryTxt=&productGroup=invst&reportProdsCompIDs=null&searchResIncCount=5&searchResInitCount=10&searchproduct=&selCIRider=Y&selCategory=whole-life&selGender=M&selSmokStatus=Y&sortEndoGroup=select&sortNonWLGroup=1&sortOrderSelected=null&sortWLGroup=3&subCatCountJson=null&subCatSeleJson=null&viewProdsId=null
   #PremAnnualGroup=select&PremSingleGroup=select&ProdsCompIDs=null&ProdsVisibleIDs=null&SATLAll=select&SATLDCIPS=50000&SATLNonDCIPS=select&SAWLAll=select&SAWLDCIPS=select&SAWLNonDCIPS=select&breadCrumb=null&coverageTermEndow=select&coverageTermTLAllList=select&coverageTermTLDCIPs=5%20Years&coverageTermTLNonDCIP=select&dob=01%2F01%2F1980&gaSearchSummary=null&pageAction=search&premiumTermAll=select&premiumTermDcips=select&premiumTermNonDcips=select&premiumTypeDCIPs=Annual&premiumTypeOther=Annual&prodGroup=bips&prodStringXML=&prodSummaryTxt=&productGroup=invst&reportProdsCompIDs=null&searchResIncCount=5&searchResInitCount=10&searchproduct=&selCIRider=Y&selCategory=term-life&selGender=F&selSmokStatus=Y&sortEndoGroup=select&sortNonWLGroup=1&sortOrderSelected=null&sortWLGroup=select&subCatCountJson=null&subCatSeleJson=null&viewProdsId=null









