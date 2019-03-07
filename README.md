# Web-Scrapping-Python
Requisites: 
<br><br>
pip install requests<br>
pip install bs4 or pip install beautifulsoup4 <br>
pip install pandas pip install lxml or  pip install html5lib <br>
<br>

<br>
Note:
<br>
1) After running the program, we will obtain the squeezed text. We can copy  and paste  it in a text file.( I have saved as Output_Web_Scrapping.txt)<br>
<br>
2)It will take some time to create the json file. Until process ends , dont kill that. ( I have stored the results in IndeedData.json)<br>
<br>
3) IndeedData.json has very small data because I have not mentioned Attributes. 
<br>                       
<pre>job_post_object = {
                            "job_title": div.find(name="a").text.encode('utf-8'),
                            "company": div.find(name="span").text.encode('utf-8'),
                            "location": div.find(name="span").text.encode('utf-8'),
                            "summary": div.find(name='span').text.encode('utf-8'),
                            "salary": div.find(name="div").text.encode('utf-8')
                    } </pre>
<br>
But if I mention Attributes like this,
<br>
<pre>job_post_object = {
                            "job_title": div.find(name="a", attrs={"data-tn-element":"jobTitle"}).text.encode('utf-8'),
                            "company": div.find(name="span", attrs={"class":"company"}).text.encode('utf-8'),
                            "location": div.find(name="span", attrs={"class": "location"}).text.encode('utf-8'),
                            "summary": div.find(name='span').text.encode('utf-8'),
                            "salary": div.find(name="div").text.encode('utf-8')
                    } 
</pre>                    
 <br>
 I get "error object has no attribute text" which means that the given URL is not user-friendly.  So we can use an alternative URL.
