from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.http import JsonResponse
import threading
import time

data = []
# Create your views here.
def scrap(request):
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    amazonDriver = webdriver.Chrome(PATH)
    darazDriver = webdriver.Chrome(PATH)
    # aliexpressDriver = webdriver.Chrome(PATH)
    #     #daraz
    # #scrapDaraz(driver)
    y = threading.Thread(target=scrapDaraz,args=(darazDriver,))
    y.start()
   
    #     #amazon
    # #scrapAmazon(driver)
    x = threading.Thread(target=scrapAmazon,args=(amazonDriver,))
    x.start()
   
    #     #aliexpress
    # scrapAliExpress(aliexpressDriver)
    y.join()
    x.join()

    return JsonResponse(data,safe=False)

# def scrapAliExpress(driver):

#     global data
#     driver.get('https://www.aliexpress.com/')
#     searchBar = driver.find_element_by_name('SearchText')
#     searchBar.send_keys("Iphone 12")
#     searchBar.send_keys(Keys.RETURN)
#         #scroll down to load all the products
#     time.sleep(2)
#     driver.execute_script("window.scrollTo(0.6,document.body.scrollHeight)")
#     # JIIxO
#     # _1OUGS
#     time.sleep(4)
#     searchResults = WebDriverWait(driver,10).until(
#     EC.presence_of_element_located((By.TAG_NAME,"div[class='JIIxO']"))
#     )
#     divs = searchResults.find_elements_by_tag_name("div[class='_1OUGS']")
#     for product in divs:
#         print(product.text)
#     # count=0
    # for product in searchResults:
    #     count+=1
    # print(count)

def scrapDaraz(driver):
    #data = []
  
    global data
    driver.get("https://www.daraz.pk/")
    searchBar=driver.find_element_by_id("q")
    searchBar.send_keys("Iphone 12")
    searchBar.send_keys(Keys.RETURN)
    
    searchResults = WebDriverWait(driver,10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME,"div[class='c2prKC']"))
    )
    # print(searchResults.text)
    for product in searchResults:
        obj = {}
            #get image and product link
        div = product.find_element_by_tag_name("div[class='cRjKsc']")   
        link = div.find_element_by_tag_name('a').get_attribute('href')
        #print(link)
        obj['product_link']=link
        try:
            image = div.find_element_by_tag_name('img').get_attribute('src')
            #print(image)
            obj['product_image']=image
        except:
            print("image doesnt exist")
        finally:
                #get title
            div = product.find_element_by_tag_name("div[class='c16H9d']")
            title = div.find_element_by_tag_name("a")
            #print(title.text)
            obj['title']=title.text
                #get price
            div = product.find_element_by_tag_name("div[class='c3gUW0']")
            price = div.find_element_by_tag_name("span")
            #print(price.text)
            obj['price']=price.text
                #get ratings
            div = product.find_elements_by_tag_name("i[class*='c3dn4k']")
            stars=0
            for i in div:
                if i.get_attribute("class")=="c3dn4k c3EEAg":
                    stars+=1
            ratings=str(stars)+" out of 5 stars"
            obj['ratings']=ratings
            
        data.append(obj)


def scrapAmazon(driver):
    #data = []
    global data
    driver.get("https://www.amazon.com/")


    try:
        searchBar=driver.find_element_by_class_name('nav-search-field')
        searchBar=searchBar.find_element_by_tag_name('input')
        searchBar.send_keys("Iphone 12")
        searchBar.send_keys(Keys.RETURN)
        searchResults= WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME,"div[data-component-type='s-search-result']"))
        
        )
        WebDriverWait(driver, 2)
        for product in searchResults:
            # class="a-price-whole" -decimal -fraction
            obj = {}
            try:
                price = product.find_element_by_tag_name("div[class='a-section a-spacing-none a-spacing-top-small']")
                price = price.find_element_by_tag_name("a[class='a-size-base a-link-normal a-text-normal']")
                price = price.find_element_by_tag_name("span[class='a-price-whole']")
                #print(price.text)
                obj['price']=price.text
            except:
                print("price doesn't exists")
            finally:
                #getting title text
                try:
                    obj['title']=(product.find_element_by_tag_name("h2[class*='a-size-mini a-spacing-none a-color-base']")).text
                    #print((product.find_element_by_tag_name("h2[class*='a-size-mini a-spacing-none a-color-base']")).text)
                except:
                    print('title doesnt exists')
                finally:
                        #getting ratings info
                    try:
                        ratingsdiv = product.find_element_by_tag_name("div[class='a-row a-size-small']")
                        ratings=(ratingsdiv.find_element_by_tag_name("span"))
                        obj['ratings']=ratings.get_attribute('aria-label')
                        #print(ratings.get_attribute('aria-label'))
                    except:
                        print("span doesn't exists")
                    finally:
                        #getting link to main page and product image
                        a = product.find_element_by_tag_name("a[class='a-link-normal s-no-outline']")
                        #print(a.get_attribute('href'))
                        obj['product_link']=a.get_attribute('href')
                        image = product.find_element_by_tag_name("img[class='s-image']").get_attribute('src')
                        #print(image)
                        obj['image_link']=image
                        
            data.append(obj)
                                   
    except:
        driver.close()

    

        


