# Email-Collection-and-Creation-Service

Utilizes requests, OpenAI and pandas to look through URL's passed to it. And pulls details about the website, and any emails associated with it for mass marketing and cold emailing needs. 

Emails are located in several ways. Once by general scraping measures for emails, utilizing both pandas and requests. And another scraping for names.

For the name option the names are searched on the website, attaching a validaty BOOL to it. The more valid names being names found from the Tags and Sitemap about the team, writer or authors. And non-valid coming from the website that don't exist in the Sitemap/Tag Space. 

Due to names being fairly subjective, a csv of birth names is added to track on any similar name from the search. Utilizing the difflib library to compare whats found and to the csv within a specific threshold

In the data folder, all results will be stored from the running of the scripts. 

Ensures Proper Set Up: 
  1. pip install -r requirements, setup a virtual enviorment here if you want
  2. go into data/required_data to setup example email prompt as well as modify the configs. 
  3. in that same folder add your api keys for hunter.io and chat gpt
  5. run file from main


