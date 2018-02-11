from django.shortcuts import render, HttpResponse, redirect
import scraper
from operator import itemgetter
  # the index function is called when root is visited
def index(request):
    return render(request, 'first_app/index.html')

def results(request):
  context = {}
  if request.method == 'POST':
    keyword = request.POST['keyword'].title()
    city = request.POST['city'].title()
    salary_dict, rating_dict = process(request, keyword, city)
    if len(salary_dict)==0 or len(rating_dict)==0:
      context = {
        'flag' : "Not_found",
        'error': "Oops! Your search for %s in %s does not match any jobs. Please try again."%(keyword,city)
      }
      return render(request, 'first_app/results.html', context)
    context = {
  'salary_dict' : salary_dict,
  'rating_dict' : rating_dict,
  'keyword': keyword,
  'city': city
  }
  return render(request, 'first_app/results.html', context)

def process(request, keyword, city):
  scraped_data = scraper.parse(keyword, city)
  # location = scraper.getLocation()
  #print location
  if scraped_data is None:
    #error = "Your search for %s, in %s does not match any jobs"%(keyword,city)
    salary_dict = []
    rating_dict = []
    return salary_dict, rating_dict
  salary_dict = []
  rating_dict = []
  #for data in scraped_data:
  if scraped_data:
    for d in scraped_data:
      if len(d['Rating'])>0:
        rating_dict.append({'Company': d['Company'], 'Rating': d['Rating'],'Url': d['Url'], 'Location': d['Location'], 'Salary': d['Salary'], 'Name': d['Name']})
      if len(d['Salary'])>0:
        salary_dict.append({'Company': d['Company'], 'Rating': d['Rating'], 'Int_Salary': int(d['Salary'].split('-')[1][1:-1]),'Salary': d['Salary'],'Url': d['Url'], 'Location': d['Location'], 'Name': d['Name']})
    rating_dict = sorted(rating_dict, key=itemgetter('Rating'), reverse=True)
    salary_dict = sorted(salary_dict, key=itemgetter('Int_Salary'), reverse=True)
    return salary_dict, rating_dict
  else:
    print "Your search for %s, in %s does not match any jobs"%(keyword,city)
