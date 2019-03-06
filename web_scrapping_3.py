import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import json

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
  spans = soup.findAll('span', attrs={'class': 'location'})
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
  spans = soup.findAll('span', attrs={'class': 'summary'})
  for span in spans:
    summaries.append(span.text.strip())
  return(summaries)

URL = "https://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=New+York&start=10"
#conducting a request of the stated URL above:
page = requests.get(URL)
#specifying a desired format of “page” using the html parser - this allows python to read the various components of the page, rather than treating it as one long string.
soup = BeautifulSoup(page.text, "html.parser")
#soup = BeautifulSoup(page.text, "lxml")
#printing soup in a more structured tree format that makes for easier reading
print(soup.prettify())


jobs=extract_job_title_from_result(soup)
#print(jobs)

companies=extract_company_from_result(soup)
#print(companies)

locations=extract_location_from_result(soup)
#print(locations)

salaries=extract_salary_from_result(soup)
#print(salaries)
extract_summary_from_result(soup)

max_results_per_city = 100

city_set = ['New+York','Chicago','San+Francisco', 'Austin', 'Seattle', 'Los+Angeles', 'Philadelphia', 'Atlanta', 'Dallas', 'Pittsburgh', 'Portland', 'Phoenix', 'Denver', 'Houston', 'Miami', 'Washington+DC', 'Boulder']

columns = ["city", "job_title", "company_name", "location", "summary", "salary"]

sample_df = pd.DataFrame(columns = columns)

field_names = ["city", "job_title", "company_name", "location", "summary", "salary"]
with open('output.json', 'a', newline='') as f_output:
    csv_output = csv.writer(f_output,field_names) #delimiter=",")
    for city in city_set:
        for start in range(0, max_results_per_city, 10):
            page = requests.get('http://www.indeed.ca/jobs?q=data+scientist,+data+analyst,+python&l=' + str(city) + '&jt=fulltime')  # + '&start=' + str(start))
            time.sleep(1)  #ensuring at least 1 second between page grabs

            soup = BeautifulSoup(page.text, 'lxml')
            for div in soup.find_all(name='div', attrs={'class':'row'}):
    #creating an empty list to hold the data for each posting
                job_post = []
    #append city name
                job_post.append(city)
    #grabbing job title
                for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
                    job_post.append(a['title']) 
    #grabbing company name
                    company = div.find_all(name='span', attrs={'class':'company'}) 
                    if len(company) > 0:
                        [job_post.append(b.text.strip()) for b in company]
                    else:
                        [job_post.append(span.text) for span in div.find_all(name='span', attrs={'class':'result-link-source'})]
    #grabbing location name
                    [job_post.append(span.text) for span in div.findAll('span', attrs={'class': 'location'})]
    #grabbing summary text
                    [job_post.append(span.text.strip()) for span in div.findAll('span', attrs={'class': 'summary'})]
    #grabbing salary
                    div_two = div.find(name='div', attrs={'class':'salarySnippet'})
                    job_post.append(div_two.text.strip() if div_two else 'Nothing found')
    #appending list of job post info to dataframe at index num
                    #sample_df.loc[len(sample_df) + 1] = job_post

#saving sample_df as a local csv file — define your own local path to save contents 
                csv_output.writerow({x: x for x in field_names})
                csv_output.writerow([job_post])

#sample_df.to_csv('output.csv', encoding='utf-8')

                
