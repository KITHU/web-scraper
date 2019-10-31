from bs4 import BeautifulSoup as bs
import csv
import requests
import schedule
import time


def scrap_remotive_dev():
    # web url
    remotive_website = 'https://remotive.io/remote-jobs/software-dev'

    # get all the html from the url
    res = requests.get(remotive_website)

    # use Beautifulsoup
    soup = bs(res.text,'html.parser')

    remotive = "https://remotive.io"
    arr=[]     #hold all the job dics
    job = {}   #
    stacks=[]
    dev = soup.find_all(class_='job-details')
    for jobs in dev:
        for title in jobs.select('.position'):
            job['title'] = title.get_text(strip=True)
            link = [a['href'] for a in title.find_all('a', href=True)]
            job['link'] = remotive + link[0]
        for company in jobs.select('.company'):
            job['company'] = company.get_text(strip=True)
        for tags in jobs.select('.job-tag'):
            stacks.append(tags.get_text(strip=True))
        job['stacks']=stacks
        arr.append(job)
        stacks=[]
        job = {}
    return arr

with open('jobs_from_remotive.csv', mode='w') as csv_file:
    fieldnames = ['title', 'link', 'company', 'stacks']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for dicts in scrap_remotive_dev():
        writer.writerow(dicts)

schedule.every().day.at("10:30").do(scrap_remotive_dev)

while True:
    schedule.run_pending()
    time.sleep(1)


