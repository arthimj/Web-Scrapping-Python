import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import simplejson as json
import threading

def extract_job_title_from_result(soup):
    jobs = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
            jobs.append(a["title"])
    return(jobs)
        
def extract_company_from_result(soup): 
  companies = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    company = div.find_all(name="span", attrs={"class":"company"})
    if len(company) > 0:
      for b in company:
        companies.append(b.text.strip())
    else:
      sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
      for span in sec_try:
          companies.append(span.text.strip())
  return(companies)

def extract_location_from_result(soup): 
  locations = []
  spans = soup.findAll("span", attrs={"class": "location"})
  for span in spans:
    locations.append(span.text)
  return(locations)

def extract_salary_from_result(soup): 
  salaries = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    try:
      salaries.append(div.find('nobr').text)
    except:
      try:
        div_two = div.find(name="div", attrs={"class":"sjcl"})
        div_three = div_two.find("div")
        salaries.append(div_three.text.strip())
      except:
        salaries.append("Nothing_found")
  return(salaries)

def extract_summary_from_result(soup): 
  summaries = []
  spans = soup.findAll("span", attrs={"class": "summary"})
  for span in spans:
    summaries.append(span.text.strip())
  return(summaries)

URL = "https://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=New+York&start=10"

page = requests.get(URL)
soup = BeautifulSoup(page.text, "html.parser")

print(soup.prettify())


if __name__ == "__main__": 
  
    t1 = threading.Thread(target=extract_job_title_from_result, args=(soup,)) 
    t2 = threading.Thread(target=extract_company_from_result, args=(soup,)) 
    t3 = threading.Thread(target=extract_location_from_result,args=(soup,))
    t4 = threading.Thread(target=extract_salary_from_result,args=(soup,))
    t5 = threading.Thread(target=extract_summary_from_result,args=(soup,))
    
    
    t1.start() 
    t2.start()
    t3.start()
    t4.start()
    t5.start() 
  
    
    t1.join() 
    t2.join()
    t3.join()
    t4.join()
    t5.join()
  

    page = requests.get(URL,timeout=5)  # + '&start=' + str(start))
    time.sleep(1)  
    soup = BeautifulSoup(page.text, 'lxml')
    job_post = []
    for div in soup.find_all(name='div', attrs={'class':'row'}):
        job_post_object = {
                            "job_title": div.find(name="a").text.encode('utf-8'),
                            "company": div.find(name="span").text.encode('utf-8'),
                            "location": div.find(name="span").text.encode('utf-8'),
                            "summary": div.find(name='span').text.encode('utf-8'),
                            "salary": div.find(name="div").text.encode('utf-8')
                    }                
        job_post.append(job_post_object)
    with open('IndeedData.json', 'w') as outfile:
        json.dump(job_post, outfile)
        outfile.write('\n')
        

                
