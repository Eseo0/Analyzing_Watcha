# selenium의 webdriver를 사용하기 위한 import
# 웹 브라우저를 제어하고 웹 페이지를 열고 조작하는데 사용
from selenium import webdriver

# selenium으로 키를 조작하기 위한 import
from selenium.webdriver.common.keys import Keys

# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time

# 웹 페이지에서 특정 요소를 찾기 위한 import
# 웹 요소를 검색할 때 사용되는 여러 종류의 기준을 제공
from selenium.webdriver.common.by import By
    
# 데이터프레임 사용을 위한 import
import pandas as pd

# 크롤링 소요시간 계산을 위한 import
from datetime import datetime



# Chrome WebDriver 옵션 설정하기
options = webdriver.ChromeOptions() # 옵션 설정 객체 생성

options.add_argument('--headless') # 창이 나타나지 않고 백그라운드에서 실행하도록 설정
options.add_argument('disable-gpu') # 불필요한 그래픽카드 기능 제거
options.add_argument('--no-sandbox') # Chrome 보안 기능 비활성화 -> Chrome 시스템 리소스 감소로 가벼운 웹 스크래핑 작업 수행
options.add_argument('--disable-dev-shm-usage') # 공유 메모리 공간 사용 비활성화 -> 리소스 제한이 있는 환경이나 큰 웹 페이지를 다루는 경우 사용
options.add_argument('window-size=1920x1080') # pc용 사이즈
options.add_argument('--start-maximized') # 브라우저가 최대화된 상태로 실행
# User-Agent 추가 -> 사이트에서의 차단을 회피, 특정 기능이나 콘텐츠에 대한 정상적인 접근을 가능하도록
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36") 

driver = webdriver.Chrome(options=options) # 설정 적용



# 콘텐츠 id와 종류(영화 or tv프로그램)를 담을 리스트
id_type_data = [] 


# 스크롤을 끝까지 내리는 함수
def scroll_end():
    
    # 현재 스크롤 높이 
    scroll_location = driver.execute_script("return document.body.scrollHeight")
  
    while True:
    	# 현재 스크롤의 가장 아래로 내림
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
           
        # 전체 스크롤이 늘어날 때까지 대기
        time.sleep(1)
        
        # 늘어난 스크롤 높이
        scroll_height = driver.execute_script("return document.body.scrollHeight")

        # 늘어난 스크롤 위치와 이동 전 위치 같으면(더 이상 스크롤이 늘어나지 않으면) 종료
        if scroll_location == scroll_height:
        	break
    	    
        # 같지 않으면 스크롤 위치 값을 수정하여 같아질 때까지 반복
        else:
        	#스크롤 위치값을 수정
        	scroll_location = driver.execute_script("return document.body.scrollHeight")


# 왓챠에서 콘텐츠의 아이디와 종류를 가져오는 함수
def get_id_type(year, content_type):
        
    # 콘텐츠 목록에서 각 콘텐츠의 정보가 담겨있는 url을 가져온다.
    url = 'https://watcha.com/tag?ids='+ year + '&domain=' + content_type # 콘텐츠 목록 url
    
    driver.implicitly_wait(5) # 암묵적 대기, NoSuchElementException을 던지기 전에 기다리도록 함(초단위)
    driver.get(url)

    # 스크롤 끝까지 내리기
    scroll_end()
    
    # 5초 동안 대기        
    time.sleep(5)
    
    # 콘텐츠 목록에서 콘텐츠를 클릭했을 때 연결된 a태그 href 속성의 값을 가져옴(id)
    for i in range(1,12000,1): # 목록의 행
        
        try:
            for j in range(1,7,1): # 목록의 열 6개로 고정
                
                id_src = driver.find_element(By.XPATH,'//*[@id="root"]/div[1]/main/div/div[2]/section/div['+str(i)+']/div/ul/li['+str(j)+']/div/a')
                id_href = id_src.get_attribute('href') 

                id_type_data.append([id_href, content_type])
                
        except Exception: # 없는 행에 도달하면 반복문에서 탈출한다.
            break    
    
    
if __name__ == '__main__':

    # 시작 시각
    start_time = datetime.now()

    
    # 1920~2023 각 년대별 url의 ids 값을 저장한 리스트  
    # https://watcha.com/tag?ids=508871&domain=movie(1920년대)
    # https://watcha.com/tag?ids=508870&domain=movie(1930년대)
    year_list = ['508871','508870','508869','508868','508867','508866','508865','260666'
              ,'260672','260671'
              ,'508924']
    
    count = 0  # 크롤링 체크용 변수, 11(len(year_list))이면 완료
    
    
    # 1. 콘텐츠의 id와 종류 가져오기
    for y in year_list:
            get_id_type(y, 'movie')
            get_id_type(y, 'tv')
            
            count += 1
            print(str(count))
    
    
    # 2. id 값으로 콘텐츠 정보를 수집할 것이기 때문에 미리 전처리 후 저장
    
    # id값만 추출하여 리스트에 다시 저장
    for i in range(len(id_type_data)):
        split_id = id_type_data[i][0].split('/')
        id_type_data[i][0] = split_id[len(split_id)-1]
    
    # 데이터 프레임 생성
    id_type_df = pd.DataFrame(id_type_data, columns=['id', '종류'])
    
    # 중복 데이터 존재시 미리 제거
    if id_type_df.duplicated().sum() > 0:
        id_type_df.drop_duplicates(inplace=True)
    
    # csv 파일로 저장
    id_type_df.to_csv('C:/Crawling_Watcha/csv/watcha_id_type.csv',encoding='cp949', mode='w', index=False)
    
    
    # 종료 시각
    end_time = datetime.now()
    
    # 소요 시간 확인
    print(end_time-start_time)
    
    



