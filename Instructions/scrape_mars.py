from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    # create mars_data dict to collect all the values and insert in mongo
    mars_data = {}

    # 1. visit mars.nasa.gov to scrape latest Mars news
    #print("into scrape function 1................")
    newsurl = 'https://mars.nasa.gov/news/'
    browser.visit(newsurl)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=2)
    html = browser.html

    # create a soup object from the html
  
    
    news_soup = bs(html,"html.parser")
    news_title = news_soup.find('div', class_='content_title').text
    news_p= news_soup.find('div', class_='article_teaser_body').text
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p
    print(news_p)
    # 2. Scrapping Mars Space Images - Featured Image
    #print("into scrape function 2................")
    base_url = "https:/www.jpl.nasa.gov/"
    images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(images_url)
    html = browser.html
    image_soup = bs(html,"html.parser")
    
    featured_image  = image_soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    
    featured_image_url = base_url + featured_image
    mars_data['featured_image_url']=featured_image_url
    ##     print(mars_data['featured_image_url'])
    
    
    # 3. Scrapping Mars Weather
    #print("into scrape function 3................")
    weather_url= 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(weather_url)
    soup = bs(response.text, 'lxml')
    mars_weather_temp = soup.find('div', class_='js-tweet-text-container').find("a").text
    mars_weather = soup.find('div', class_='js-tweet-text-container').text.replace(mars_weather_temp,"")
    mars_data['mars_weather']=mars_weather
    print("===============Mars Weather===========")
    print(mars_weather)
    ## print(mars_data['mars_weather'])
    
    # 4. Scrape Mars Facts
    #print("into scrape function 4................")
    marsfact_url = 'https://space-facts.com/mars'
    response = requests.get(marsfact_url)
    soup = bs(response.text, 'lxml')
    facts_table = soup.find('table', class_='tablepress tablepress-id-mars').text
    mars_data['facts_table']=facts_table
    
    ## print(mars_data['facts_table'])
    
    # 5. Collecting Mars Hemispheres data with title and pictures
    #print("into scrape function 5................")
    
    hemesphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    base_url = "https://astrogeology.usgs.gov"
    
    response = requests.get(hemesphere_url)
    soup = bs(response.text, 'lxml')
    result_set_url = soup.find_all('a', class_='itemLink product-item')
    result_set_titles = soup.find_all('h3')
    
    hemisphere_image_urls = []

    for i in range(len(result_set_url)):
        target_url_1 = result_set_url[i]
        target_url_2 = target_url_1['href']
        target_url_full = base_url+target_url_2
        #print(target_url_full)
        response = requests.get(target_url_full)
        soup = bs(response.text, 'lxml')
        result_set_url_4 = soup.find('img', class_='wide-image')['src']
        result_set_url_5=base_url+result_set_url_4
        title=result_set_titles[i].text
        print(title)
        print(result_set_url_5)
        hemisphere_image_urls.append({'title' : title, 'img_url' : result_set_url_5})

    mars_data['hemisphere_image_urls']=hemisphere_image_urls
    ##print(mars_data['hemisphere_image_urls'])


    browser.quit()
    return mars_data

