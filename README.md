# Project Roadmap

## Project Overview
- **Project Name:** Bridge Legal Project (Computer Science Intern)
- **Author:** Xuhan Xie

## Goals and Objectives
- [ ] Collect legal data(court data, civil cases, mass tort, class action) as much as possible (From Public legal resource, 
legal data company).
- [ ] Parse the data and store data into database
- [ ] Create a demo

## Planning Phase
- [ ] Identify possible legal data resources. 
- LexisNexis
- PACER (Public Access to Court Electronic Records)
- United States Supreme Court 
- United States Courts (uscourts.gov)
- [ ] 2 ways to collect data (I will implement both)
- APIs: some websites provide API interface for data downloading. We could write a program to automate downloading process. 
- Crawler techniques: some websites do not provide APIs for data downloading. Thus, we could use Python crawler to collect data from legal data resources.
- [ ] According to the data type collected and considering that legal data is mostly labeled and organized, I decide to use relational database to store data.

## Implementing Phase
- API METHOD
1. Did google research for possible public legal resources with APIs generation. In this project, take https://legiscan.com/ as an example.
2. Generated API key to get the permission for downloading.
3. Read the API User Manual to get familiar with the APIs usage. (e.g. data type, request format, response format, etc.)
4. Implemented Python program api_method.py to automate the data download and parsing.
5. According to the data collected, designed MySQL database schema to store corresponding data. For this part, there are 4 tables (Sessions, Bills, People, Amendments) in the database. 
Besides, I only stored url instead of the whole doc content or large binary files into MySQL database. 
Because relational database is not good for storing a binary large object(zip file, media file). It is slow, and large files will increase the size of the database a lot which will be hard to maintain in the future. If the file is very important, and it has to be stored,
we could upload them into file systems like Google cloud storage or AWS S3 buckets.
- 1. Make sure installed all required libraries and import them
- 2. There are 8 functions within api_method.py. 
- 3. get_session_list() will download session list json file into our current directory.
- 4. store_session() will save data into mysql database.
- 5. Pair functions like (get_people_list(), store_people()), (get_bills_list(), store_bills()), (get_amendments(), store_amendments()) perform corresponding jobs
- 6. Then, logged into mysql server. We could use SQL to manipulate tables data (see operate.sql file) to do data analysis or apply machine learning techniques such as NLP to do the TEXT analysis and understanding.
  


- WEB CRAWLER METHOD
1. Some websites may not provide APIs for data downloads. So Python crawler is another tool to deal with such situation. 
2. Take https://www.lawsuit-information-center.com/ as an example, this is a lawsuit information center which has multiple articles for
different case category. Considering that Bridge Legal mainly focusing on mass torts, I used Python crawler to collect legal articles information corresponding
to different cases(Camp Lejeune, AFFF, etc.)
3. For this method, I used Scrapy framework, which is used for web crawling.


## Risks and Mitigations
- **Risk:** [Illegal collection through python crawler for sensitive legal data may subject to litigation]
  - Mitigation: [Collecting data from public resources will minimize this risk.]

## demo link
[WebCrawler demo](https://drive.google.com/file/d/15bHViDxiNvkZOPzBr5vCR2t17rTB9N_C/view?usp=sharing)
[API_demo](https://drive.google.com/file/d/1dCmIfBTUzAM70ZOaiNgYtUJ0RER_56Vp/view?usp=sharing)