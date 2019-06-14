#https://www.startupindia.gov.in/content/sih/en/search.html?roles=Startup&page=0
## Original Source in -- OWN file --- /media/dhankar/Dhankar_1/a7_18/a7_18_NewsPaper/newspaper/scrap_startupIndia.py

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
"""
Additional IMPORTS
"""
from selenium.webdriver.common.by import By ### for link_text #
# Source -- https://selenium-python.readthedocs.io/locating-elements.html
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests
import re , io , os 

import pandas as pd
from bs4 import BeautifulSoup
import datetime
dt_now = str(datetime.datetime.now())
#print("DHANK_date_____",dt_now)

### Headers not used ??
headers = {
'User-Agent_1': 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36',###
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }

#base_url = "https://www.startupindia.gov.in/content/sih/en/search.html?roles=Startup&page="

class linkedin_Scraper():
    def __init__(self):
        pass
        # FOO_ Nothing defined here as of now - lets see what DEFAULTS can be given here within the __init__ ..

    def init_scrap_linkedin(self,init_str_linkedin):
        """
        SCRAP Google Search for LinkedIn pages URL's
        init_searchStr --- Is coming from MODELS -- model_init_Search_LinkedIn ## TBD 
        """
        #print("----------init_searchStr-----------",init_searchStr)
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options
        options = Options()
        options.add_argument("--headless")
        #browser = webdriver.Firefox(firefox_options=options, executable_path=r"path to geckodriver")
        driver = webdriver.Firefox(firefox_options=options) ### OK MAIN HEADLESS
        #driver = webdriver.Firefox() ### Testing NON HEADLESS
        
        lnkd_all_soups_list = []
        google_per_page_soup_ls = [] 

        base_google_search_url = "https://www.google.com/search?client=ubuntu&channel=fs&q=" + str(init_str_linkedin) + "&ie=utf-8&oe=utf-8"
        driver.get(base_google_search_url)
        time.sleep(3) ## DONT REDUCE this TIME SLEEP..
        html = driver.page_source
        soup  = BeautifulSoup(html,'html.parser')
        str_soup = str(soup)
        google_per_page_soup_ls.append(str_soup)

        # Driver Click - Next Page 
        ### /html/body/div[6]/div[3]/div[10]/div[1]/div[2]/div/div[5]/div/span[1]/div/table/tbody/tr/td[3]/a
        time.sleep(3)
        driver.find_element_by_xpath('/html/body/div[6]/div[3]/div[10]/div[1]/div[2]/div/div[5]/div/span[1]/div/table/tbody/tr/td[3]/a').click()
        html_1 = driver.page_source
        soup_1  = BeautifulSoup(html_1,'html.parser')
        str_soup_1 = str(soup_1)
        google_per_page_soup_ls.append(str_soup_1)

        ### /html/body/div[6]/div[3]/div[10]/div[1]/div[2]/div/div[5]/div/span[1]/div/table/tbody/tr/td[4]/a
        time.sleep(3)
        driver.find_element_by_xpath('/html/body/div[6]/div[3]/div[10]/div[1]/div[2]/div/div[5]/div/span[1]/div/table/tbody/tr/td[4]/a').click()
        html_2 = driver.page_source
        soup_2  = BeautifulSoup(html_2,'html.parser')
        str_soup_2 = str(soup_2)
        google_per_page_soup_ls.append(str_soup_2)

        ### /html/body/div[6]/div[3]/div[10]/div[1]/div[2]/div/div[5]/div/span[1]/div/table/tbody/tr/td[5]/a
        time.sleep(3)
        driver.find_element_by_xpath('/html/body/div[6]/div[3]/div[10]/div[1]/div[2]/div/div[5]/div/span[1]/div/table/tbody/tr/td[5]/a').click()
        html_3 = driver.page_source
        soup_3  = BeautifulSoup(html_3,'html.parser')
        str_soup_3 = str(soup_3)
        google_per_page_soup_ls.append(str_soup_3)

        return google_per_page_soup_ls
        

    def data_from_per_page_soup(self,parms):
        """
        Scarp Profiles from Per Page Soups of Google Init Search pages
        org_name_lnkd_from_initModel = str(latest_Lnkd_ls[k].Org_Name)
                city_lnkd_from_initModel = str(latest_Lnkd_ls[k].Geo_City)
                cntry_lnkd_from_initModel = str(latest_Lnkd_ls[k].Geo_Country)

        """
        designation = parms["designation"]
        org_name = parms["org_name"]
        city = parms["city"]
        cntry = parms["cntry"]
        college = parms["college"]
        university = parms["university"]
        google_per_page_soup_ls = parms["google_per_page_soup_ls"]
        #

        lnkd_profile_urls_ls = []
        lnkd_urls_list = []
        lnkd_names_list = []
        profile_names_ls = []
        frst_nam_ls = []
        mid_nam_ls = []
        last_nam_ls = []
        dt_now_ls = []
        #

        org_name_lnkd_ls = []
        city_lnkd_ls = []
        country_lnkd_ls = []
        college_lnkd_ls = []
        university_lnkd_ls = []
        designation_lnkd_ls = []
        #

        ## CHUNK -1 --- from Google INIT Search Page 
        # START TAG == <div class="rc">
        # END TAG == </span></div></div></div>
        com_in = "com/in/"
        jobs = "jobs"

        for k in range(len(google_per_page_soup_ls)):
            str_soup = str(google_per_page_soup_ls[k])
            # print(str_soup)
            # print("          "*300)

            lnkd_chunk_one = re.findall(r'<div class="rc">(.*?)</div></div></div><!--n--></div>',str_soup,re.M|re.S)

            for k in range(len(lnkd_chunk_one)):
                # print("-------------str(lnkd_chunk_one[k]-----------",str(lnkd_chunk_one[k]))
                profile_url = re.findall(r'<a href="(.*?)" onmousedown=',str(lnkd_chunk_one[k]),re.M|re.S)
                if com_in in str(profile_url):
                    if jobs not in str(profile_url):
                        profile_url = re.sub(r"\[","",str(profile_url))
                        profile_url = re.sub(r"\]","",str(profile_url))
                        lnkd_profile_urls_ls.append(profile_url)
                        # print("-----------lnkd_profile_urls_ls-------------",lnkd_profile_urls_ls)

                        profile_name = re.findall(r'class="LC20lb">(.*?)</h3>',str(lnkd_chunk_one[k]),re.M|re.S)
                        # print("   "*90)
                        # print("----------profile_name-----------",profile_name)

                        profile_names_ls.append(profile_name)
                        profile_name_1 = str(profile_name).split("-")
                        #print("-----------profile_name_1------------------",profile_name_1)
                        profile_name_1 = str(profile_name_1[0])
                        #print("-----------profile_name_1---22-------------",profile_name_1)
                        profile_name_ls = str(profile_name_1).split()
                        #print("-----------profile_name_1----LS------------",profile_name_ls)
                        #
                        if len(profile_name_ls) > 3:
                            first_name = str(profile_name_ls[0])
                            first_name = re.sub(r"\[\'","",str(first_name))
                            frst_nam_ls.append(first_name)
                            middle_name = str(profile_name_ls[1])
                            mid_nam_ls.append(middle_name)
                            last_name = str(profile_name_ls[2])
                            last_nam_ls.append(last_name)

                        if len(profile_name_ls) == 3:
                            first_name = str(profile_name_ls[0])
                            first_name = re.sub(r"\[\'","",str(first_name))
                            frst_nam_ls.append(first_name)
                            middle_name = str(profile_name_ls[1])
                            mid_nam_ls.append(middle_name)
                            last_name = str(profile_name_ls[2])
                            last_nam_ls.append(last_name)
                        if len(profile_name_ls) == 2:
                            first_name = str(profile_name_ls[0])
                            first_name = re.sub(r"\[\'","",str(first_name))
                            frst_nam_ls.append(first_name)
                            middle_name = "__NA__"
                            mid_nam_ls.append(middle_name)
                            last_name = str(profile_name_ls[1])
                            last_nam_ls.append(last_name)
                        if len(profile_name_ls) == 1:
                            first_name = str(profile_name_ls[0])
                            first_name = re.sub(r"\[\'","",str(first_name))
                            frst_nam_ls.append(first_name)
                            middle_name = "__NA__"
                            mid_nam_ls.append(middle_name)
                            last_name = "__NA__"
                            last_nam_ls.append(last_name)
                        if len(profile_name_ls) > 3:
                            pass
                       
                    else:
                        pass

                #print("   "*90)
                len_frst_nam_ls = len(frst_nam_ls)
                # print("-------------len_frst_nam_ls-------------",len_frst_nam_ls)
                # print("----FIRST NAME LS ===",frst_nam_ls)
                # print("   "*90)

                len_mid_nam_ls = len(mid_nam_ls)
                #print("-------------len_mid_nam_ls--------------",len_mid_nam_ls)
                #print("-----MID NAME LS ===",mid_nam_ls)
                #print("   "*90)

                len_last_nam_ls = len(last_nam_ls)
                #print("------------len_last_nam_ls---------------",len_last_nam_ls)
                #print("-----LAST NAME LS ===",last_nam_ls)
                #print("   "*90)

                len_lnkd_profile_urls_ls = len(lnkd_profile_urls_ls)
                #print("-----len_lnkd_profile_urls_ls---------",len_lnkd_profile_urls_ls)
                #print("-----lnkd_profile_urls_ls=------------",lnkd_profile_urls_ls)
                #print("   "*90)
                
                
        for k in range(len(frst_nam_ls)):
            dt_now_ls.append(dt_now) 
            org_name_lnkd_ls.append(str(org_name))
            city_lnkd_ls.append(str(city))  
            country_lnkd_ls.append(str(cntry))
            college_lnkd_ls.append(str(college))
            university_lnkd_ls.append(str(university))
            designation_lnkd_ls.append(str(designation))
        
        len_city_lnkd_ls = len(city_lnkd_ls)
        #print("---------len_city_lnkd_ls-------",len_city_lnkd_ls) 
        len_country_lnkd_ls = len(country_lnkd_ls)
        #print("----------len_country_lnkd_ls----",len_country_lnkd_ls)         
        len_org_name_lnkd_ls = len(org_name_lnkd_ls)
        #print("---------len_org_name_lnkd_ls----",len_org_name_lnkd_ls)
        len_dt_now_ls = len(dt_now_ls)
        #print("------len_dt_now_ls-----",len_dt_now_ls)
        print("   "*90)

        df_lnkd_init = pd.DataFrame({'First_Name':frst_nam_ls,'Middle_Name':mid_nam_ls,'Last_Name':last_nam_ls,'designation':designation_lnkd_ls,'Org_Name':org_name_lnkd_ls,'college':college_lnkd_ls,'university':university_lnkd_ls,'City':city_lnkd_ls,'Country':country_lnkd_ls,'LinkdeIn':lnkd_profile_urls_ls ,'TimeStamp':dt_now_ls })
        print(df_lnkd_init)
        print("   "*90)   
        
        return df_lnkd_init #lnkd_profile_urls_ls , profile_names_ls  ## MAKE a DF of these #profile_urls_ls#lnkd_names_list #lnkd_urls_list

        """
        #<cite class="iUh30">https://www.linkedin.com/in/stlandis</cite>
        #profile_urls_ls = soup.find_all('cite' , attrs={'class="iUh30"': re.compile("ww.linkedin.com")}) 
        # ## Didnt Work here.. Worked below for TRACXN 
        profile_names_ls = soup.find_all('h3')
        profile_urls_ls = soup.find_all('cite')
        
        linkedin = "LinkedIn"

        for k in range(len(profile_names_ls)):
            if linkedin in str(profile_names_ls[k]):
                #
                # <cite class="iUh30">
                #<h3 class="LC20lb">
                str_lnkd_name = re.sub('<h3 class="LC20lb">','',str(profile_names_ls[k]))
                str_lnkd_name = re.sub('LinkedIn</h3>','',str_lnkd_name)
                str_lnkd_name = re.sub('\|','',str_lnkd_name)
                lnkd_names_list.append(str(str_lnkd_name).strip())
        print("-----------lnkd_names_list--------------",lnkd_names_list)

        linkedin_url = "https://www.linkedin.com/in/"

        for k in range(len(profile_urls_ls)):
            if linkedin_url in str(profile_urls_ls[k]):
                #
                print(profile_urls_ls[k])
        
                # profile_urls_ls = soup.find_all('cite')
                # for k in range(len(profile_urls_ls)):
                #     # <cite class="iUh30">
                #     str_lnkd_url = re.sub('<cite class="iUh30">','',str(profile_urls_ls[k]))
                #     str_lnkd_url = re.sub('</cite>','',str_lnkd_url)
                #     lnkd_urls_list.append(str(str_lnkd_url).strip())
                
                # # for k in range(len(lnkd_urls_list)):
                #     driver.get(str(lnkd_urls_list[k]))
                #     time.sleep(5) ## DONT REDUCE this TIME SLEEP..
                #     html_profile = driver.page_source
                #     soup_profile = BeautifulSoup(html_profile,'html.parser')
        return profile_urls_ls#lnkd_names_list #lnkd_urls_list

        """
        


class Startup_Scraper():
    def __init__(self):
        pass

    def scrapingTracxn(self,init_searchStr):
        """
        SCRAP Google Search for Tracxn pages URL's
        init_searchStr --- Is coming from MODELS --
        """
        
        #print("----------init_searchStr-----------",init_searchStr)
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options
        options = Options()
        options.add_argument("--headless")
        #browser = webdriver.Firefox(firefox_options=options, executable_path=r"path to geckodriver")
        #driver = webdriver.Firefox(firefox_options=options) ### OK MAIN HEADLESS
        driver = webdriver.Firefox() ### Testing NON HEADLESS
        
        txcn_all_soups_list = []
        txcn_url_nameslist = []
        txcn_url_nameslist_1 = []
        txcn_urls_list = []
        txcn_urls_list_1 = []
        all_soups_list = []

        #try:
        #driver = webdriver.Firefox()
        #driver = webdriver.PhantomJS() ## PhantomJS - Deprecatewd

        base_google_search_url = "https://www.google.com/search?client=ubuntu&channel=fs&q=" + str(init_searchStr) + "&ie=utf-8&oe=utf-8"
        driver.get(base_google_search_url)
        time.sleep(5) ## DONT REDUCE this TIME SLEEP..
        html = driver.page_source
        soup  = BeautifulSoup(html , 'html.parser')
        #txcn_url_nameslist = soup.find_all('h3' , attrs={'class="LC20lb"': re.compile("Analyst Notes")})
        txcn_url_nameslist = soup.find_all('h3')
        #print("----------txcn_url_nameslist--------------",txcn_url_nameslist)
        print("     "*90)

        ##  <h3 class="LC20lb">Tracxn Global Analyst Notes – AgriTech | Tracxn Blog</h3>
        for k in range(len(txcn_url_nameslist)):
            str_tcxn_name = re.sub('<h3 class="LC20lb">','',str(txcn_url_nameslist[k]))
            str_tcxn_name = re.sub('</h3>','',str_tcxn_name)
            txcn_url_nameslist_1.append(str(str_tcxn_name).strip())
        #print("---------txcn_url_nameslist-------FROM SCRAPING.py------",txcn_url_nameslist_1) # OK 
        print("     "*90)

        txcn_urls_list = soup.find_all('cite')
        #<cite class="iUh30">https://blog.tracxn.com/2018/02/10/tracxn-analyst-notes-india-practice-604/</cite>
        for k in range(len(txcn_urls_list)):
            str_tcxn_url = re.sub('<cite class="iUh30">','',str(txcn_urls_list[k]))
            str_tcxn_url = re.sub('</cite>','',str_tcxn_url)
            txcn_urls_list_1.append(str(str_tcxn_url).strip())

        #print("---------txcn_urls_list_1-------FROM SCRAPING.py------",txcn_urls_list_1) # OK 
        print("     "*90)
        
        for k in range(len(txcn_urls_list_1)):
            driver.get(str(txcn_urls_list_1[k]))
            time.sleep(5) ## DONT REDUCE this TIME SLEEP..
            html = driver.page_source
            soup  = BeautifulSoup(html , 'html.parser')
            all_soups_list.append(soup)
            #print("----------all_soups_list----------------",all_soups_list)
            print("     "*90)
        return all_soups_list
    # except Exception as e:
    #         #raise e 
    #         print("    "*90)
    #         print("EXCEPTION from ---SCRAPING.py--- scrapingTracxn-----",e)
    #         print("    "*90)
    #     return all_soups_list
            

    def parse_soup_tcxn(self,str_soup_inFile):
        #
        """
        PARSING SOUP of Indl Pages of TRACXN from local text gzip file .
        """
        list_str1 = []
        tcxn_list_str2 = []
        tcxn_list_str3 = []
        tcxn_list_str4 = []
        strong_str = "<strong>"
        tracxn_analyst_notes_urls = [] #tracxn-analyst-notes
        tracxn_analyst_notes_names = [] #tracxn-analyst-notes
        tracxn_analyst_notes = "tracxn-analyst-notes"
        fa_angle = "fa-angle"
        tracxn_archiveURL_ls = []
        startUp_Org_Name_ls = []

        """
        All ARCHIVES
        """
        tracxn_archiveURL = re.findall(r'<span>Archives</span>(.*?)chimpy_ajaxurl',str_soup_inFile,re.M|re.S)
        for k in range(len(tracxn_archiveURL)):
            tracxn_archiveURL_links = re.findall(r'href="(.*?)">',str(tracxn_archiveURL[k]),re.M|re.S)
            for k in range(len(tracxn_archiveURL_links)):
                #print(str(tracxn_archiveURL_links[k])) ## OK 
                tracxn_archiveURL_ls.append(str(tracxn_archiveURL_links[k]))
        ## No action for now --- laterz SRAPE all -- tracxn_archiveURL_ls
        """
        tracxn_analyst_notes
        """
        tracxn_analyst_notes_ls = re.findall(r'<a href="https://blog.tracxn.com(.*?)</a>',str_soup_inFile,re.M|re.S)
        for k in range(len(tracxn_analyst_notes_ls)):
            if tracxn_analyst_notes in str(tracxn_analyst_notes_ls[k]):
                if fa_angle not in str(tracxn_analyst_notes_ls[k]):
                    str_anal_notes = str(tracxn_analyst_notes_ls[k])
                    ls_anal_notes = str_anal_notes.split('">')
                    str_anal_notesURL = "https://blog.tracxn.com" + str(ls_anal_notes[0])
                    str_anal_notesNAMES = ls_anal_notes[1]
                    tracxn_analyst_notes_urls.append(str_anal_notesURL)
                    tracxn_analyst_notes_names.append(str_anal_notesNAMES)
        # print("-------tracxn_analyst_notes_ls--------",tracxn_analyst_notes_urls)
        # print("-------tracxn_analyst_notes_names--------",tracxn_analyst_notes_names)
        # print("     "*290)
        # ## No action for now --- laterz SRAPE all -- tracxn_analyst_notes_urls
        ## create a DF of these LS in utily.py and save in DB --- maybe reqd laterz

        """
        org_name_main , loca_comparable , comparable_global
        """
        loca_comparable = "Local comparable"
        comparable_global = "Global comparable"
        ls_org_url_locals = []
        ls_org_name_locals = []
        
        ls_org_url_globals = []
        ls_org_name_globals = []
        
        ls_org_name_main = []
        ls_org_url_main = []

        ls_org_news = []


        ls_comparables_org_urls = []
        ls_comparables_org_urls_others = []
        ls_comparables_org_name = []
        ls_comparables_org_name_others = []



        ls_names1 = re.findall(r'<span class="fa"></span>Login</a>(.*?)<span class="fa"></span>Login</a>',str_soup_inFile,re.M|re.S)
        for k in range(len(ls_names1)):
            #<p><span style="color: #000000;"> ----- TO ---- target="_blank">Link<
            first_chunk = re.findall(r'#000000;">(.*?)target="_blank">Link<',str(ls_names1[k]),re.M|re.S)
            for k in range(len(first_chunk)):
                count_usg = re.findall(r';usg=',str(first_chunk[k]),re.M|re.S)
                #print("-----------len(count_usg)---------",count_usg)
                #print("-----------len(count_usg)---------",len(count_usg))
                if len(count_usg) > 4:
                    #print("-----------len(count_usg)---->> 4-----",len(count_usg))
                    str_comparables = str(first_chunk[k])

                    comparables_org_name_main = re.findall(r'target="_blank">(.*?)</a>',str(str_comparables),re.M|re.S)
                    for k in range(len(comparables_org_name_main)):
                        if k == 0:
                            ### ONLY MAIN ORG 
                            ls_comparables_org_name.append(comparables_org_name_main[k])
                        else:
                            #### ONLY OTHERS LOCALS ORGS 
                            ls_comparables_org_name_others.append(comparables_org_name_main[k])
                            
                    for k in range(len(comparables_org_name_main)-2): ### FOO_ERROR -2 ### CHECK 
                        ls_comparables_org_name.append(" ")

                    mainComparables_org_urls = re.findall(r'en&amp;q=(.*?)&amp;source',str(str_comparables),re.M|re.S)
                    for k in range(len(mainComparables_org_urls)):
                        if k == 0:
                            #### ONLY MAIN ORG
                            if len(mainComparables_org_urls[k]) > 40:
                                pass
                            else:
                                ls_comparables_org_urls.append(str(mainComparables_org_urls[k]))
                        else:
                            #### ONLY OTHERS LOCALS ORGS
                            if len(mainComparables_org_urls[k]) > 40:
                                pass
                            else:
                                ls_comparables_org_urls_others.append(str(mainComparables_org_urls[k]))

                    for k in range(len(mainComparables_org_urls)-3): ### FOO_ERROR -3 ### CHECK 
                        ls_comparables_org_urls.append(" ")

                if len(count_usg) == 3:
                    str_non_compare_3 = str(first_chunk[k])
                    #print(len(str_non_compare_3))
                if len(count_usg) == 2:
                    str_non_compare_2 = str(first_chunk[k])
                    #print(len(str_non_compare_2))
                elif len(count_usg) == 1:
                    str_non_compare_1 = str(first_chunk[k]) 
                    #print(len(str_non_compare_1))


                """
                ###FOO_ERROR_usg_count_1
                <p><span style="color: #000000;">Alium Capital, Sydney-based venture capital firm, 
                """    


            org_name_main = re.findall(r'target="_blank">(.*?)</a>',str(first_chunk),re.M|re.S)
            # print("-----------org_name_main--------------",org_name_main)
            # print("    "*90)
            for k in range(len(org_name_main)):
                ls_org_name_main.append(str(org_name_main[k]))

            org_url_main = re.findall(r'en&amp;q=(.*?)&amp;source',str(first_chunk),re.M|re.S)
            #print("-----------org_url_main--------------",org_url_main)
            #print("    "*90)
            for k in range(len(org_url_main)):
                if len(org_url_main[k]) > 40:
                    pass
                    #ls_org_news.append(str(org_url_main[k]))
                else:
                    ls_org_url_main.append(str(org_url_main[k]))

                #print(str(org_url_main[k]))
                #print(len(org_url_main[k]))

            # count_usg = re.findall(r';usg=',str(first_chunk),re.M|re.S)
            # print("-----------len(count_usg)---------",count_usg)

            # org_url_news = re.findall(r';usg=(.*?)target="_blank">Li',str(first_chunk),re.M|re.S)
            # print("----------org_url_news---------------",org_url_news)

               
        return ls_org_name_main , ls_org_url_main , ls_comparables_org_urls , ls_comparables_org_urls_others , ls_comparables_org_name , ls_comparables_org_name_others


            # startUp_Org_RaisingYear = re.findall(r'target="_blank">(.*?)</a>',str(ls_names1[k]),re.M|re.S)
            # startUp_Org_HQ_Location = re.findall(r'target="_blank">(.*?)</a>',str(ls_names1[k]),re.M|re.S)
        
            # news_stub = re.findall(r'#000000;">(.*?)xc2',str(ls_names1[k]),re.M|re.S) 
            # news_stub = re.sub(r'\\','',str(news_stub)) ## '\\' IS WRONG r'\\' IS RIGHT
            # if strong_str in str(news_stub):
            #     ls_news_stub = news_stub.split('#000000;">')
            #     news_stub = str(ls_news_stub[1])

            # ls_names2 = re.findall(r'<span class="fa"></span>Login</a>(.*?)source=gmail&amp',str(ls_names1[k]),re.M|re.S)
            # print("--------len(ls_names2)--------",len(ls_names2)) # ??
            # for k in range(len(ls_names2)):
            #     list_str1.append(str(ls_names2[k]))
            # print("------------TEST---------",list_str1)    

            # ls_names3 = re.findall(r'<a data-saferedirecturl=(.*?)<a data-saferedirecturl=',str(ls_names1[k]),re.M|re.S)
            # for k in range(len(ls_names3)):
            #     long_str = str(ls_names3[k])
            #     ls_long_str = long_str.split('en&amp;q=')
            #     ls_long_str = ls_long_str[1]
            #     ls_long_str = ls_long_str.split('&amp;source=')
            #     long_str1 = ls_long_str[0]

        #for k in range(len(ls_names1)):
        
                
        # #print("---NEWS SOURCE URL------long_str1--------",long_str1)
        # tcxn_list_str4.append(long_str1)
        # print("--------tcxn_list_str4--------",tcxn_list_str4)
        # print("    "*90)
        # #print("---news_source_name-------------------",news_source_name)
        # print("    "*90)
        # tcxn_list_str3.append(news_source_name)
        # print("--------tcxn_list_str3--------",tcxn_list_str3)
        # #print("---news_stub-------------------",news_stub)
        # print("    "*90)
        # tcxn_list_str2.append(news_stub)
        # print("--------tcxn_list_str2--------",tcxn_list_str2)

        #return list_str1 , tcxn_list_str2 , tcxn_list_str3 , tcxn_list_str4 , ls_org_url_globals , ls_org_name_globals , ls_org_url_locals , ls_org_name_locals , ls_org_name_main , ls_org_url_main

        #return list_str1 , tcxn_list_str2 , tcxn_list_str3 , tcxn_list_str4 , org_name_locals , org_url_locals , org_name_main , org_url_main

        #
        # for k in range(len(ls_names)):
        #     ls_str_1a = str(ls_names[k]).split('amp;q=')
        #     str_1a = ls_str_1a[1]
        #     str_1a = re.sub('&amp;','',str_1a)
        #     list_str1.append(str(str_1a).strip())
        

        # list_alt = ls_names[1::2]
        # for k in range(len(list_alt)):
        #     str_1 = re.sub('<p','',str(list_alt[k]))
        #     str_2 = re.sub('</span></p>','',str_1)
        #     str_3 = re.sub('<a class="margin-b10 display-ib" href="','',str_2)
            
        #     list_str1.append(str_3)
        #     ls_str_3 = str_3.split('" target="')
        #     ls_str_3a = str(ls_str_3[0]).split("\n")
        #     ls_str_3a = str(ls_str_3a).split("\\n")
            
        #     #ls_str_3 = re.sub('\\n','',str(ls_str_3[0]))
        #     print("-----------ls_str_3a----------------",ls_str_3a)
        #     str_name_1 = re.sub(r"\[","",str(ls_str_3a[0]))
        #     str_name_1 = re.sub(r"\]","",str_name_1)
        #     str_name_1 = re.sub(r"\'","",str_name_1)
        #     str_name_1 = re.sub(r"\\","",str_name_1)
        #     str_name_1 = re.sub(r"&amp","",str_name_1)
        #     list_str2.append(str(str_name_1))
        #     print("-----------list_str2----------------",list_str2)
        #     print("    "*90)
        #     str_name_2 = re.sub(r"\]","",str(ls_str_3a[1]))
        #     str_name_2 = re.sub(r"\'","",str_name_2)

        #     str_name_2 = re.sub(r"&amp","",str_name_2)
        #     list_str3.append(str(str_name_2))
        # print("---len(list_str2)----",len(list_str2)) # ORG_Name
        # print("---len(list_str3)----",len(list_str3)) # ORG_URL
        # print("---len(list_str3)----",list_str3)

        # """
        # Engagement Level
        # """
        # ls_eng_level = re.findall(r'Engagement Level : <strong>(.*?)<div class="rating-star">',str_soup_inFile,re.M|re.S)
        # list_alt1 = ls_eng_level[1::2]
        # for k in range(len(list_alt1)):
        #     str_1a = re.sub(r'</strong>','',str(list_alt1[k]))
        #     str_1b = re.sub(r'</p>','',str_1a)
        #     str_1b = re.sub(r'\\n\\n','',str_1b) ##FOO_ERROR_Check
        #     ls_eng_levl.append(str_1b)
        # print("---len(ls_eng_levl)----",len(ls_eng_levl))


    def scraping_main(self,base_url):
        """
        Scraping the StartUps.
        """
        INT_Increment = 0
        for i in range(1):            
            INT_Increment += 1
            print("INT_Increment==",INT_Increment)            
            I_txt = str(INT_Increment) 
            ### Selenium for DELAYING THE DOM Loading 
            driver = webdriver.Firefox()
            driver.get(base_url+I_txt)
            time.sleep(10) ## DONT REDUCE this TIME SLEEP...
            """
            SORT BY NAME ---
            # XPATH --- of the </li> ---->> /html/body/div[1]/div[2]/div[2]/div/div/div[3]/div[1]/div/ul/li[3]
            """
            #driver.find_element_by_link_text("sort-header active").click()
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/div[3]/div[1]/div/ul/li[3]").click()
            time.sleep(2)
            """
            LOAD MORE --- #XPATH --- //*[@id="loadmoreicon"]
            """
            for k in range(1): ### FOO_ERROR-- Change to 5 or 10 required 
                driver.find_element_by_xpath('//*[@id="loadmoreicon"]').click()
                time.sleep(5)
            # Click on LOAD MORE and ----- sleep for 5 Secs.??  [CRITICAL] WORKER TIMEOUT (pid:21964)

            html = driver.page_source
            soup  = BeautifulSoup(html , 'html.parser')

            profile_tags_list = soup.find_all('a' , attrs={'href': re.compile("profile")})
            str_links = str(profile_tags_list)
            ## "href="/content"
            Startup = "Startup"
            str_a = "https://www.startupindia.gov.in/content/sih/en/profile.Startup."
            str_b = ".html"

            ls_profile_urls = re.findall(r'content(.*?).html',str_links,re.M|re.S)
            ls_url_nums = []
            for k in range(len(ls_profile_urls)):
                if Startup in str(ls_profile_urls[k]):
                    num_only_url = re.sub(r'/sih/en/profile.Startup.','',str(ls_profile_urls[k]))
                    final_url = str_a + num_only_url + str_b
                    #print("-------final_url--------from SCRAPING.py-----",final_url)
                    ls_url_nums.append(final_url)
            #print(ls_url_nums)

            ls_timeStamp = []
            for k in range(len(ls_url_nums)):
                ls_timeStamp.append(str(dt_now))

            df_indl_urls = pd.DataFrame({'Indl_Page_URLs':ls_url_nums,'TimeStamp':ls_timeStamp})
            col_names = ['Indl_Page_URLs','TimeStamp']
            df_indl_urls = df_indl_urls[col_names]
            with open('df_indl_urls_.csv', 'a') as out_file:
                df_indl_urls.to_csv(out_file, header=True)
            return ls_url_nums , df_indl_urls


    def scraping_indl_pgs(self,ls_url_nums):
        all_soups_list = []
        driver = webdriver.Firefox()
        for k in range(len(ls_url_nums)):
            driver.get(str(ls_url_nums[k]))
            time.sleep(5)
            html = driver.page_source
            soup  = BeautifulSoup(html , 'html.parser')
            all_soups_list.append(soup)
        #print(all_soups_list)
        return all_soups_list
        

        # import gzip
        # with gzip.open('soup_file.txt.gz', 'wb') as file_to_be_written:
        #     file_to_be_written.write(str(all_soups_list).encode('utf-8'))

        # # textfilename = 'startUpIndia_Soup_'+dt_now+'.txt'
        # # with io.open(textfilename, 'w') as outfile:  #'w' WRITE STRING to FILE  ## 
        # #     outfile.write(str(all_soups_list))
        # # print("     "*90)



    def parse_soup(self,str_soup_inFile):
        """
        PARSING the SOUP of Indl Pages from local text gzip file .
        """
        list_str1 = []
        list_str2 = []
        list_str3 = []
        ls_eng_levl = []
        ls_org_img = []
        sih_api = "sih/api"
        ls_reg_coy = []

        ls_names = re.findall(r'span class="name">(.*?)class="orglevel"',str_soup_inFile,re.M|re.S)
        list_alt = ls_names[1::2]
        for k in range(len(list_alt)):
            str_1 = re.sub('<p','',str(list_alt[k]))
            str_2 = re.sub('</span></p>','',str_1)
            str_3 = re.sub('<a class="margin-b10 display-ib" href="','',str_2)
            
            list_str1.append(str_3)
            ls_str_3 = str_3.split('" target="')
            ls_str_3a = str(ls_str_3[0]).split("\n")
            ls_str_3a = str(ls_str_3a).split("\\n")
            
            #ls_str_3 = re.sub('\\n','',str(ls_str_3[0]))
            print("-----------ls_str_3a----------------",ls_str_3a)
            str_name_1 = re.sub(r"\[","",str(ls_str_3a[0]))
            str_name_1 = re.sub(r"\]","",str_name_1)
            str_name_1 = re.sub(r"\'","",str_name_1)
            str_name_1 = re.sub(r"\\","",str_name_1)
            str_name_1 = re.sub(r"&amp","",str_name_1)
            list_str2.append(str(str_name_1))
            print("-----------list_str2----------------",list_str2)
            print("    "*90)
            str_name_2 = re.sub(r"\]","",str(ls_str_3a[1]))
            str_name_2 = re.sub(r"\'","",str_name_2)

            str_name_2 = re.sub(r"&amp","",str_name_2)
            list_str3.append(str(str_name_2))
        print("---len(list_str2)----",len(list_str2)) # ORG_Name
        print("---len(list_str3)----",len(list_str3)) # ORG_URL
        print("---len(list_str3)----",list_str3)

        """
        Engagement Level
        """
        ls_eng_level = re.findall(r'Engagement Level : <strong>(.*?)<div class="rating-star">',str_soup_inFile,re.M|re.S)
        list_alt1 = ls_eng_level[1::2]
        for k in range(len(list_alt1)):
            str_1a = re.sub(r'</strong>','',str(list_alt1[k]))
            str_1b = re.sub(r'</p>','',str_1a)
            str_1b = re.sub(r'\\n\\n','',str_1b) ##FOO_ERROR Check
            ls_eng_levl.append(str_1b)
        print("---len(ls_eng_levl)----",len(ls_eng_levl))


        """
        LinkedIn --- Regis Info 
        """
        #for="star1"></label>
        #<ul class="search-filters-list list-unstyled recognition-list">
        ls_linkedin = []
        linked = "www.linkedin.com/in/"
        Follow_span = "Follow</span>"
        this_url = "this.url"
        linkedin_url = re.findall(r'for="star1"></label>(.*?)<ul class="search-filters-list',str_soup_inFile,re.M|re.S)
        print("-----INIT-------len(list_alt2)----------",len(linkedin_url))

        for k in range(len(linkedin_url)):
            if Follow_span not in str(linkedin_url[k]):
                str_b1 = "No_Linked_URL_FollowSPAN_Missing"
                ls_linkedin.append(str(str_b1).strip())
            else:
                if linked in str(linkedin_url[k]):
                    str_b1 = str(linkedin_url[k]).split('<span class="networkfacebook">')
                    str_b1 = str_b1[0].split('href="')
                    str_b1 = re.sub('">','',str(str_b1[1]))
                    str_b1 = re.sub(r'\\n','',str_b1) ## FOO_ERROR Check
                    print(str_b1)
                    print("     "*90)
                    ls_linkedin.append(str(str_b1).strip())
                else:
                    str_b1 = "NO_LinkedIn_URL"
                    ls_linkedin.append(str(str_b1).strip())
        ls_linkedin = ls_linkedin[1::2]

        print("---len(ls_linkedin)----",len(ls_linkedin))
        print("---len(ls_linkedin)----",ls_linkedin)

        """
        ORG Image
        """
        org_img = re.findall(r'<div class="wrapper-image person">(.*?)"/>',str_soup_inFile,re.M|re.S)
        for k in range(len(org_img)):
            str_12a = re.sub('<div class="outer-container">','',str(org_img[k]))
            str_12a = re.sub('<img src="','',str_12a)
            if sih_api in str_12a:
                str_12a = re.sub('\\n\\n','',str_12a) ## FOO_ERROR Check
                str_12a = str_12a
            else:
                str_12a = "_No_ORG_IMAGE_"   
            ls_org_img.append(str(str_12a).strip())
        print("---len(ls_org_img)----",len(ls_org_img))

        """
        REGISTERED COMPANY
        """
        regis = "Regis"
        reg_coy = re.findall(r'recognition-list">(.*?)</ul>',str_soup_inFile,re.M|re.S)
        list_alt_reg = reg_coy[1::2] ## getting the Alternate Entries
        for k in range(len(list_alt_reg)):
            if regis in str(list_alt_reg[k]):
                str_reg = "REGISTERED COMPANY"
            else:
                str_reg = "NOT - REGISTERED COMPANY"
            ls_reg_coy.append(str_reg)    
        print("---len(ls_reg_coy)----",len(ls_reg_coy))

        """
        STAGE - Scaling -- b5">Stage</p>
        """    
        ls_stage = []
        stage_coy = re.findall(r'b5">Stage</p>(.*?)</p></div>',str_soup_inFile,re.M|re.S)
        list_alt_stage = stage_coy[1::2] ## getting the Alternate Entries
        for k in range(len(list_alt_stage)):
            str_14 = re.sub('<div class="focus-content"> <p>','',str(list_alt_stage[k]))
            str_14 = re.sub('\\n','',str(str_14))
            str_14 = re.sub('\\n','',str(str_14))
            str_14 = re.sub('\\n','',str(str_14))
            ls_stage.append(str(str_14).strip()) ## FOO_ERROR Check
        print("---len(ls_stage)----",len(ls_stage))

        """
        Focus Industry  -- b5">Focus Industry</p>
        """
        ls_indus = []
        get_tag = "getTag"
        focus_ind = re.findall(r'b5">Focus Industry</p>(.*?)</p></div>',str_soup_inFile,re.M|re.S)
        for k in range(len(focus_ind)):
            if get_tag in str(focus_ind[k]):
                pass
            else:
                str_15 = re.sub('<div class="focus-content"><p>','',str(focus_ind[k]))
                str_15 = re.sub('&amp;',' and ',str_15)
                str_15 = re.sub('\\n','',str(str_15))
                str_15 = re.sub('\\n','',str(str_15))
                str_15 = re.sub('\\n','',str(str_15))
                ls_indus.append(str(str_15).strip()) ## FOO_ERROR Check
        ls_indus.append("DUMMY---INDUS")        
        print("---len(ls_indus)----",len(ls_indus))
        print("---ls_indus----",ls_indus)
        print("   "*90)


        """
        FOO_ERROR --- to be fixed --- seem to have mixed up the Service Area and Focus Sector ??
        Look at --- 2 Feets Relax Your Feets ---- b5">Service Area(s)</p> === <p>E-commerce</p>
        Look at --- 2 Feets Relax Your Feets ---- b5">Focus Sector</p> === <p>Lifestyle</p> ??? 
        FOCUS SECTOR -- b5">Focus Sector</p>
        """
        ls_sector = []
        each = "#each"
        focus_sector = re.findall(r'Service Area(.*?)</li>',str_soup_inFile,re.M|re.S)
        for k in range(len(focus_sector)):
            if each in str(focus_sector[k]):
                pass
            else:
                str_17 = str(focus_sector[k])
                ls_str_17 = str_17.split("</div>")
                str_19 = str(ls_str_17[0]).strip()
                str_19 = re.sub('<div class="focus-content">','',str_19)
                str_19 = re.sub('</p>','',str_19)
                str_19 = re.sub('<p>','',str_19)
                str_19 = re.sub('\(s\)','',str_19)
                str_19 = re.sub('\\n\\n','',str(str_19))
                str_19 = re.sub('\\n\\n','',str(str_19))
                str_19 = re.sub('\\n','',str(str_19))
                str_19 = re.sub('\\n','',str(str_19))
                str_19 = re.sub('\\n','',str(str_19))
                ### FOO_ERROR --- Dont do so many "re.sub" 
                # --- https://stackoverflow.com/questions/15175142/how-can-i-do-multiple-substitutions-using-regex-in-python
                ls_sector.append(str(str_19).strip()) ### FOO_ERROR--- strip == \\n\\n
        ls_sector.append("DUMMY---SECTOR")
        print("---len(ls_sector)----",len(ls_sector))

        """
        LOCATION    - b5">Location</p>
        """
        ls_loc = []
        getTagName = "getTagName"
        focus_loc = re.findall(r'b5">Location</p>(.*?)</li>',str_soup_inFile,re.M|re.S)
        for k in range(len(focus_loc)):
            if getTagName in str(focus_loc[k]):
                pass
            else:
                str_20 = str(focus_loc[k])
                str_20 = re.sub('</p>','',str_20)
                str_20 = re.sub('<p>','',str_20)
                str_20 = re.sub('\\n','',str(str_20))
                str_20 = re.sub('\\n','',str(str_20))
                str_20 = re.sub('\\n','',str(str_20))
                str_20 = re.sub('\\n','',str(str_20))
                str_20 = re.sub('\\n','',str(str_20))

                ls_loc.append(str_20.strip())
        print("---len(ls_loc)----",len(ls_loc))


        """
        ABOUT ME ---- <p class="heading margin-b5 margin-t15">About Me</p>
        """
        ls_about_me = []
        about_me_ls = re.findall(r'margin-b5 margin-t15">About Me</p>(.*?)<div class="more-content-foot">',str_soup_inFile,re.M|re.S)
        for k in range(len(about_me_ls)):
            str_23 = str(about_me_ls[k])
            str_23 = re.sub('</p>','',str_23)
            str_23 = re.sub('<p>','',str_23)
            str_23 = re.sub('\\n','',str(str_23))
            str_23 = re.sub('\\n','',str(str_23))
            str_23 = re.sub('\\n','',str(str_23))
            #<div class="show-read-more more-content clearfix">
            str_23 = re.sub('<div class="show-read-more more-content clearfix">','',str_23)
            #\n<div class="show-read-more more-content clearfix more-content-height-fixed">
            str_23 = re.sub('<div class="show-read-more more-content clearfix more-content-height-fixed">','',str_23)
            ls_about_me.append(str_23.strip())
        print(len(ls_about_me))



        """
        # TBD ---- BOOTSTRAPPED --- b5">Funded or Bootstrapped?</p>
        # """
        # ls_boot = []
        # boot_ls = re.findall(r'Bootstrapped(.*?)</ul></div>',str_soup_inFile,re.M|re.S)
        # print(boot_ls)
        # for k in range(len(boot_ls)):
        #     print(boot_ls[k])
            

        ls_timeStamp = []
        for k in range(len(list_str3)):
            ls_timeStamp.append(str(dt_now))
        
        df_data1 = pd.DataFrame({'ORG_Name':list_str2,'ORG_URL':list_str3,'ENG_Levl':ls_eng_levl,'LinkedIn_URL':ls_linkedin,'ORG_Image':ls_org_img,'REG_Coy':ls_reg_coy,'COY_Stage':ls_stage,'ORG_Industry':ls_indus,'ORG_Sector':ls_sector,'ORG_loca':ls_loc,'ORG_AboutMe':ls_about_me,'TimeStamp':ls_timeStamp})
        col_names = ['ORG_Name','ORG_URL','ENG_Levl','LinkedIn_URL','ORG_Image','REG_Coy','COY_Stage','ORG_Industry','ORG_Sector','ORG_loca','ORG_AboutMe','TimeStamp']
        df_data1 = df_data1[col_names]

        df_forJSON = pd.DataFrame({'ORG_Name':list_str2,'ORG_URL':list_str3,'ENG_Levl':ls_eng_levl,'LinkedIn_URL':ls_linkedin,'COY_Stage':ls_stage,'ORG_Industry':ls_indus,'ORG_Sector':ls_sector,'ORG_loca':ls_loc})
        col_namesJSON = ['ORG_Name','ORG_URL','ENG_Levl','LinkedIn_URL','COY_Stage','ORG_Industry','ORG_Sector','ORG_loca']
        df_forJSON = df_forJSON[col_namesJSON]


        #df_data1 = "df_data1"
        with open('df_data1_.csv', 'a') as f:
            df_data1.to_csv(f, header=True)

        return df_forJSON , df_data1 , list_str2,list_str3,ls_eng_levl, ls_linkedin,ls_org_img,ls_reg_coy,ls_stage,ls_indus,ls_sector,ls_loc,ls_about_me,ls_timeStamp 






    

    


"""
#print(profile_tags_list)
    print("    "*90)


    # https_tags_list = soup.find_all('a' , attrs={'href': re.compile("^https")})
    # print(https_tags_list)
    # print("    "*90)
    # http_tags_list = soup.find_all('a' , attrs={'href': re.compile("^http")})
    # print(http_tags_list)

### SAMPLE --- EMAIL --- REGEX 
<input class="form-control" data-pattern-error="Email address is invalid" data-required-error="This is a mandatory field" name="email" pattern="^([\w\.\-]+)@([\w\-]+)((\.(\w){2,10})+)$" required="" type="email"/>

"""












    #data1 = r.content.decode(encoding='latin-1') ### .encode('utf-8').decode('ascii','ignore')
    #data1 = page.content.decode('utf-8',errors='ignore').encode('latin-1','ignore')
    #print("__________Type_Data_1__",type(data1)) ### OK --- <class 'bytes'>
    #
#     textfilename = 'startUpIndia_'+dt_now+'.txt'      
#     with io.open(textfilename, 'ab') as outfile:  #'w' WRITE to FILE 
#         outfile.write(data1)
# #
