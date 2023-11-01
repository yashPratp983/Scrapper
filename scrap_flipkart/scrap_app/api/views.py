from selenium import webdriver
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

@csrf_exempt
def Navigate(request):
    if (request.method=="POST"):
        
        body=request.body.decode("utf-8")
        body=json.loads(body)

        print(body)
        driver = webdriver.Chrome()
        driver.get('https://www.flipkart.com/')
        driver.find_element(By.CLASS_NAME,'_30XB9F').click()
        driver.find_element(By.CLASS_NAME,'Pke_EE').send_keys(body['name'])
        driver.find_element(By.CLASS_NAME,'Pke_EE').send_keys(Keys.ENTER)
        cnt=0
        page=1
        answer=[]
        
        while(cnt<=int(body['quantity'])):
            ele1=driver.find_elements(By.CLASS_NAME,'_2kHMtA')  
            cur_url=driver.current_url

            for i in ele1:
                try:
                    title=i.find_element(By.CLASS_NAME,'_4rR01T').text
                    i.find_element(By.CLASS_NAME,'_4rR01T').click()
                    pag=driver.switch_to.window(driver.window_handles[-1])
                    # return back to main window
                    price=driver.find_element(By.CLASS_NAME,'_30jeq3').text
                    rating=driver.find_element(By.CLASS_NAME,'_2d4LTz').text
                    answer.append({"title":title,"price":price,"rating":rating,"reviews":[]})
                    div_element=driver.find_element(By.CLASS_NAME,'_3UAT2v')
                    span_element=div_element.find_element(By.TAG_NAME,'span')
                    span_element.click()
                    #wait for the element to load
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'col._2wzgFH.K0kLPL')))
                    
                    pg=1
                    cnt2=0
                    while(cnt2<int(body['reviews'])):
                        url=driver.current_url
                        try:
                            ele=driver.find_elements(By.CLASS_NAME,'col._2wzgFH.K0kLPL')
                            if len(ele)==0:
                                break
                            for j in ele:
                                try:
                                    review=j.find_element(By.CLASS_NAME,'row').text
                                    rate=j.find_element(By.CLASS_NAME,'row').find_element(By.CLASS_NAME,'_3LWZlK').text
                                    detail=j.find_element(By.CLASS_NAME,'t-ZTKy').find_element(By.TAG_NAME,'div').text
                                    answer[-1]["reviews"].append({"review":review,"rating":rate,"detail":detail})
                                    cnt2+=1
                                except NoSuchElementException:
                                    print(NoSuchElementException)   
                            pg+=1
                            if(pg==2):
                                url=url+"&page="+str(pg)
                            else:
                                #find last index of '='
                                ind=url.rfind('=')
                                url=url[:ind+1]+str(pg)

                            driver.get(url)
                        except NoSuchElementException:
                            break
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0]) 
                    cnt+=1
                    if cnt>int(body['quantity']):
                        break
                except NoSuchElementException:
                    print("in except")
            if(len(ele1)<24):
                 break
            page+=1
            if page==2:
                cur_url=cur_url+"&page="+str(page)
            else:
                ind=cur_url.rfind('=')
                cur_url=cur_url[:ind+1]+str(page)
            driver.get(cur_url)
           
        print(len(answer))
        return HttpResponse(json.dumps(answer),content_type="application/json")
        
        
    
