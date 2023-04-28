from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service 
from selenium import webdriver
from selenium.webdriver.common.by import By


service = Service(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(service=service, options=options)
# review를 가져오는 함수
def get_reviews(Class_name):
    
    review_list=[]
    class_name = Class_name
    text = driver.find_elements(By.CLASS_NAME,class_name)
    
    for t in text:
        review_list.append(t.text.split('좋아요')[0].replace("\n",''))
        
    return review_list   

# 별점을 가져오는 함수
def get_stars(Class_name):
    
    star_list=[]
    class_name = Class_name
    star = driver.find_elements(By.CLASS_NAME,class_name)
    
    for s in star:
        star_list.append(s.text)
        
    star_list = star_list[2:]
    
    return star_list   

# 리스트를 하나의 최종 리스트에 append하는 함수
def append_to_list(total_list, get_list):
    
    total = total_list
    get = get_list
    
    for i in get_list:
        total.append(i)
        
    return total

# '더보기'를 클릭하여 내용 전체를 크롤링 할 수 있도록 하는 함수
def unfold(class_name):
    
    fclass = class_name
    element = driver.find_elements(By.CLASS_NAME, fclass)
    
    for e in element:
        try:
            e.click()
        except:
            pass   