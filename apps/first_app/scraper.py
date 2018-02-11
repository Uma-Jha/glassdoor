from lxml import html, etree
import requests
import re
import os
import sys
import argparse
import json
import urllib2
from exceptions import ValueError

def parse(keyword, place):

	headers = {	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				'accept-encoding': 'gzip, deflate, sdch, br',
				'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
				'referer': 'https://www.glassdoor.com/',
				'upgrade-insecure-requests': '1',
				'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
				'Cache-Control': 'no-cache',
				'Connection': 'keep-alive'
	}

	location_headers = {
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.01',
		'accept-encoding': 'gzip, deflate, sdch, br',
		'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
		'referer': 'https://www.glassdoor.com/',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
		'Cache-Control': 'no-cache',
		'Connection': 'keep-alive'
	}
	data = {"term": place,
			"maxLocationsToReturn": 10}

	location_url = "https://www.glassdoor.co.in/findPopularLocationAjax.htm?"
	try:
		# Getting location id for search location
		location_response = requests.post(location_url, headers=location_headers, data=data).json()
		place_id = location_response[0]['locationId']
		job_litsting_url = 'https://www.glassdoor.com/Job/jobs.htm'
		# Form data to get job results
		data = {
			'clickSource': 'searchBtn',
			'sc.keyword': keyword,
			'locT': 'C',
			'locId': place_id,
			'jobType': ''
		}

		job_listings = []
		if place_id:
			response = requests.post(job_litsting_url, headers=headers, data=data)
			# extracting data from
			parser = html.fromstring(response.text)
			# Making absolute url
			base_url = "https://www.glassdoor.com"
			parser.make_links_absolute(base_url)

			XPATH_ALL_JOB = '//li[@class="jl"]'
			XPATH_NAME = './/a/text()'
			XPATH_JOB_URL = './/a/@href'
			XPATH_LOC = './/span[@class="subtle loc"]/text()'
			XPATH_COMPANY = './/div[@class="flexbox empLoc"]/div/text()'
			XPATH_SALARY = './/span[@class="green small"]/text()'
			XPATH_RATING = './/span[@class="compactStars "]/text()'

			listings = parser.xpath(XPATH_ALL_JOB)
			for job in listings:
				raw_job_name = job.xpath(XPATH_NAME)
				raw_job_url = job.xpath(XPATH_JOB_URL)
				raw_lob_loc = job.xpath(XPATH_LOC)
				raw_company = job.xpath(XPATH_COMPANY)
				raw_salary = job.xpath(XPATH_SALARY)
				raw_rating = job.xpath(XPATH_RATING)
				# Cleaning data
				job_name = ''.join(raw_job_name).encode("ascii","ignore") if raw_job_name else None
				job_location = ''.join(raw_lob_loc) if raw_lob_loc else None
				raw_state = re.findall(",\s?(.*)\s?", job_location)
				state = ''.join(raw_state).strip()
				raw_city = job_location.replace(state, '')
				city = raw_city.replace(',', '').strip()
				company = ''.join(raw_company).encode("ascii","ignore").strip()
				salary = ''.join(raw_salary).strip()
				rating = ''.join(raw_rating).strip()
				job_url = raw_job_url[0] if raw_job_url else None

				jobs = {
					"Name": job_name,
					"Company": company,
					"State": state,
					"City": city,
					"Salary": salary,
					"Rating": rating,
					"Location": job_location,
					"Url": job_url
				}
				job_listings.append(jobs)

			return job_listings
		else:
			print "location id not available"

	except:
		print "Failed to load locations"

if __name__ == "__main__":
	keyword = 'software developer'
	place = 'san francisco'
	print "Fetching job details"
	#scraped_data = parse(keyword, place)
	print "Writing data to output file"
	#print scraped_data
	salary_dict = []
	rating_dict = []
	#for data in scraped_data:
	if scraped_data:
		for d in scraped_data:
			if len(d['Rating'])>0:
				rating_dict.append({'Company': d['Company'], 'Rating': d['Rating']})
			if len(d['Salary'])>0:
				salary_dict.append({'Company': d['Company'], 'Int_Salary': int(d['Salary'].split('-')[1][1:-1]),'Salary': d['Salary']})
		rating_dict = sorted(rating_dict, key=itemgetter('Rating'), reverse=True)
		salary_dict = sorted(salary_dict, key=itemgetter('Int_Salary'), reverse=True)
	else:
		print "Your search for %s, in %s does not match any jobs"%(keyword,place)

def getLocation():
	f = urllib2.urlopen('http://freegeoip.net/json/')
	json_string = f.read()
	f.close()
	location = json.loads(json_string)
	print(location)
	location_city = location['city']
	location_state = location['region_name']
	location_country = location['country_name']
	location_zip = location['zip_code']
	

