# selenium의 webdriver를 사용하기 위한 import
# 웹 브라우저를 제어하고 웹 페이지를 열고 조작하는데 사용
from selenium import webdriver

# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time

# 웹 페이지에서 특정 요소를 찾기 위한 import
# 웹 요소를 검색할 때 사용되는 여러 종류의 기준을 제공
from selenium.webdriver.common.by import By
    
# 데이터프레임 사용을 위한 import
import pandas as pd

# 무작위 수를 추출하기 위한 import
import random

# 크롤링 소요 시간을 위한 import
from datetime import datetime



# Chrome WebDriver 옵션 설정하기
options = webdriver.ChromeOptions() # 옵션 설정 객체 생성

options.add_argument('--headless') # 창이 나타나지 않고 백그라운드에서 실행하도록 설정
options.add_argument('disable-gpu') # 불필요한 그래픽카드 기능 제거
options.add_argument('--no-sandbox') # Chrome 보안 기능 비활성화 -> Chrome 시스템 리소스 감소로 가벼운 웹 스크래핑 작업 수행
options.add_argument('--disable-dev-shm-usage') # 공유 메모리 공간 사용 비활성화 -> 리소스 제한이 있는 환경이나 큰 웹 페이지를 다루는 경우 사용
options.add_argument('window-size=1920x1080') # pc용 사이즈
options.add_argument('--start-maximized') # 브라우저가 최대화된 상태로 실행
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")



# 누락된 id를 담을 리스트
missing_id = []

# 누락 데이터 수집 시작 플래그 
miss_flag = False



# 왓챠에서 tv 프로그램의 에피소드 수(1화 기준)와 상영시간을 가져오는 함수
def get_tv_rtime_epnum(id_data):
    
    # 데이터를 10개씩 csv에 저장
    batch_size = 100 
    start_i = 0 # 시작 인덱스
    end_i = batch_size # 끝 인덱스
    
    tv_id_info = [] # TV 프로그램의 에피소드 수와 상영시간을 담을 리스트
    no_such_flag = False # NoSuchElementException 발생 유무 플래그, 발생하지 않은 상태
    
    
    for i in range(int(len(id_data)/batch_size) + 1): 
        print(i)
        
        # 100개의 데이터 크롤링 후 WebDriver 인스턴스를 종료하고 새로운 인스턴스를 생성 -> 메모리 사용량을 줄이고 잠재적인 문제를 방지하기 위해
        driver = webdriver.Chrome(options=options) 
            
        for i in range(start_i, end_i):
                
            print(i) 
                
            try:
                # tv 프로그램
                url = 'https://watcha.com/contents/' + id_data[i] + '?tab=episode_info'
                
                driver.implicitly_wait(5) # 암묵적 대기, NoSuchElementException을 던지기 전에 기다리도록 함(초단위)
                driver.get(url)
                
                try:
                    epi_num = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/main/section/section/section/div[1]/div/span[2]').text
                
                except Exception: # NoSuchElementException 발생
                    no_such_flag = True 
                    epi_num = "?"
                
                try:
                    running_time = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/main/section/section/section/article[1]/div/div[2]/div/span').text
                
                except Exception:
                    no_such_flag = True
                    running_time = "?"
                
                
                if no_such_flag == True and miss_flag == True: # 누락 데이터 처리시 누락 아이디 리스트에 추가
                    missing_id.append(id_data[i])

                    no_such_flag = False # 플래그 초기화
                
                    
                tv_id_info.append([id_data[i], epi_num, running_time])
                    
            except IndexError: # 인덱스 범위 초과 예외처리
                break
                 
                                    
        if start_i == 0 and miss_flag == False: # 맨 처음 csv 생성이면서, 누락 데이터 처리가 아닌 경우
            # csv 파일로 저장
            tv_info_df = pd.DataFrame(tv_id_info, columns=['id', '에피소드 수','상영시간'])
            tv_info_df.to_csv('C:/Crawling_Watcha/csv/watcha_tv_info.csv',encoding='cp949', mode='w', index=False)
            
            tv_id_info.clear() # 다음 10개를 저장하기 위해 리셋
            
            start_i = start_i + batch_size
            end_i = end_i + batch_size
                
            driver.quit()
            
        else: 
            # csv 파일에 추가
            tv_info_df = pd.DataFrame(tv_id_info)
            tv_info_df.to_csv('C:/Crawling_Watcha/csv/watcha_tv_info.csv',encoding='cp949', mode='a', header=False, index=False)
                
            tv_id_info.clear()
                
            start_i = start_i + batch_size
            end_i = end_i + batch_size
            
        
            driver.quit() # Selenium WebDriver를 종료
                
            
        # 봇으로 간주되지 않도록 랜덤 시간동안 대기        
        num = random.randint(1, 5)
        time.sleep(num)



if __name__ == '__main__':
    
    # 시작 시각
    start_time = datetime.now()
    

    # 1. csv 파일에서 tv 프로그램 id만 가져오기
    id_type_df = pd.read_csv('C:/Crawling_Watcha/csv/watcha_id_type.csv', encoding='cp949') 
    
    mask = id_type_df['종류'] == 'tv'
    id_df = id_type_df.loc[mask,:]
    print(id_df['id'].count()) #3222
 
    id_data = id_df['id'].values.tolist()
    
    
    # 2. tv프로그램 정보 가져오기
    get_tv_rtime_epnum(id_data)
    
    # 2-1. 전체 크롤링(첫번째 크롤링)한 내용 백업
    first_tv_info = pd.read_csv('C:/Crawling_Watcha/csv/watcha_tv_info.csv', encoding='cp949')
    first_tv_info.to_csv('C:/Crawling_Watcha/csv/watcha_tv_info_first.csv',encoding='cp949', mode='w', index=False)


    # 3. 누락 데이터 id 가져오기
    df = pd.read_csv('C:/Crawling_Watcha/csv/watcha_tv_info.csv', encoding='cp949')

    # 칼럼 둘 중 하나라도 '?'로 표시된 값을 가진 행 추출
    miss_df = df[(df['에피소드 수'] == '?') | (df['상영시간'] == '?')]
    print(miss_df.count())
    missing_id = miss_df['id'].values.tolist()


    # 4. 누락된 tv프로그램 정보 다시 가져오기(크롤링 재시도)
    # 요소가 존재하지 않거나, 네트워크 또는 서버의 응답 처리 속도가 늦어 누락된 경우를 처리
    count = 1       # 누락 데이터 수집 시도 횟수
    miss_flag = True  # 누락 데이터 수집 시작
    
    for i in range(10): 
        
        if len(missing_id) == 0: # 누락된 데이터가 없는 경우
            break
            
        # csv 파일로 저장(개수 확인용)
        missing_id_df = pd.DataFrame(missing_id, columns=['id'])
        missing_id_df.to_csv('C:/Crawling_Watcha/csv/watcha_tv_missing_' + str(count) + '.csv',encoding='cp949', mode='w', index=False)
        
        r_missing_id = missing_id[:]  # 기존 누락 데이터를 저장하는 리스트
        missing_id.clear()  # 줄어든 누락 데이터를 새로 저장하기 위해 리스트 비우기
        
        count = count + 1 
        
        get_tv_rtime_epnum(r_missing_id)
    
    
    # 종료 시각
    end_time = datetime.now()
    
    # 소요 시간 확인
    print(end_time-start_time)
    

   
