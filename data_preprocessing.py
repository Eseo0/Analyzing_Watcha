import pandas as pd
import numpy as np
import re # 구분자를 2개 이상으로 자르기 위한 import, 문자열에서 원하는 패턴을 검색하거나 대체하는데 사용

# 왓챠, 왓챠피디아 크롤링 데이터 전처리
# 동일한 id에 결측치 개수가 다른 행이 여러개 있을 것(하나의 csv파일에 다 저장했기때문)

#---------------------------------------------------------------------------------------------------------------------------------

# watcha_tv_info.csv 전처리(tv 프로그램의 에피소드 수와 상영시간)
# columns=['id', '에피소드 수','상영시간']
# 결측치가 없는 레코드를 모두 수집했으므로 결측치가 있는 행 drop

# 1. csv 파일 읽어오기
tv_info_df = pd.read_csv('C:/Crawling_Watcha/csv/watcha_tv_info.csv', encoding='cp949')
 
# 2. ? 값을 NaN(결측치)으로 치환
tv_info_df.replace('?', pd.NA, inplace = True)
 
# 3. 결측치가 있는 행 제거
tv_info_df.dropna(inplace = True)
 
# 4. watcha_tv_info.csv에 덮어쓰기
tv_info_df.to_csv('C:/Crawling_Watcha/csv/watcha_tv_info.csv',encoding='cp949', mode='w', index=False)

# 5. 개수 비교
id_type_df = pd.read_csv('C:/Crawling_Watcha/csv/watcha_id_type.csv', encoding='cp949') 
mask = id_type_df['종류'] == 'tv'
tv_id_type_df = id_type_df.loc[mask,:]

print('나와야 하는 tv 프로그램 수  : ' + str(tv_id_type_df['id'].count())) 
print('전처리한 tv 프로그램 수 : ' + str(tv_info_df['id'].count()))

#=================================================================================================================================

# watcha_content_info.csv 전처리
# columns=['id', '컨텐츠 정보','평균 평점','줄거리','제작진']

# 1. 결측치가 있기 때문에 한 레코드당 결측치가 제일 적은 레코드만 남기고 drop

# 1-1. csv 파일 읽어오기
content_info_df = pd.read_csv('C:/Crawling_Watcha/csv/watcha_content_info.csv', encoding='utf-8-sig')
 

# 1-2. ? 값을 NaN(결측치)으로 치환
content_info_df.replace('?', pd.NA, inplace = True)
  
# 1-3 각 id 그룹 내에서 나머지 칼럼들의 누락된 값이 가장 작은 레코드만 남도록 처리
def keep_row_with_least_nulls(group):
    
    # ID를 제외한 나머지 칼럼들에 대해 누락된 값의 개수를 계산
    null_counts = group.iloc[:, 1:].isnull().sum(axis=1)
    
    # 누락된 값의 개수가 가장 작은 인덱스를 반환
    min_null_count_idx = null_counts.idxmin()
    
    # 누락된 값이 가장 작은 레코드를 반환
    return group.loc[min_null_count_idx]

# id를 기준으로 그룹화하여 각 그룹에 대해 함수를 적용하고 결과를 저장
content_info_df = content_info_df.groupby('id').apply(keep_row_with_least_nulls).reset_index(drop=True)

# 1-4 watcha_tv_info.csv에 덮어쓰기
content_info_df.to_csv('C:/Crawling_Watcha/csv/watcha_content_info.csv',encoding='utf-8-sig', mode='w', index=False)

 

# 1-5 개수 비교
id_type_df = pd.read_csv('C:/Crawling_Watcha/csv/watcha_id_type.csv', encoding='cp949') 

print('나와야 하는 콘텐츠 수  : ' + str(id_type_df['id'].count())) 
print('전처리한 콘텐츠 수 : ' + str(content_info_df['id'].count()))

#---------------------------------------------------------------------------------------------------------------------------------

# 2. 콘텐츠 정보 split해서 재저장
# 영화와 TV프로그램의 정보가 다르므로 구분해서 처리하기 위해 merge

# 2-1 두 csv파일 merge
merge_df = pd.merge(id_type_df, content_info_df, on='id', how='outer')

# 2-2 필요한 정보만 리스트로 추출
id_data = merge_df['id'].values.tolist()
type_data = merge_df['종류'].values.tolist()
info_data = merge_df['컨텐츠 정보'].values.tolist()

print(len(id_data))
print(len(type_data))
print(len(info_data))


# 2-3 split한 데이터를 저장할 리스트
titleList = []  # 제목
release_yerList = [] # 개봉년도    
genreList = []  # 장르
contryList = [] # 국가
running_timeList = []   # 상영시간
age_gradeList = []  # 연령 등급
tv_stationList = [] # 방송국

# 연령정보 고유값
age_grade = ['전체','7세','12세','15세','청불']


# 콘텐츠 정보 split
#for i in range(10):
for i in range(len(id_data)):
    
    split_info = re.split(r' · |\n', info_data[i])
    
    
    # 연령 정보가 split리스트에 있는지 확인
    age_found = False
    for item in age_grade:
        if item in split_info:
            age_found = True
            break
    
    titleList.append(split_info[0])
    release_yerList.append(split_info[2])
    
    if type_data[i] == "tv":
        
        running_timeList.append(None)
        
        if len(split_info) >= 7: # 모든 정보가 있는 경우
        
            if age_found == True: # 방송국 정보만 없는 경우
                tv_stationList.append(split_info[3]) 
                genreList.append(split_info[4]) 
                contryList.append(split_info[5]) 
                age_gradeList.append(split_info[6]) 
            
            else:
                tv_stationList.append(split_info[3]) 
                genreList.append(split_info[4]) 
                contryList.append(split_info[5]) 
                age_gradeList.append(None) 
            
        elif len(split_info) == 6:
            
            if age_found == True: # 방송국 정보만 없는 경우
                tv_stationList.append(None) 
                genreList.append(split_info[3]) 
                contryList.append(split_info[4]) 
                age_gradeList.append(split_info[5])
            
            else: # 연령 등급이 없는 경우
                tv_stationList.append(split_info[3]) 
                genreList.append(split_info[4]) 
                contryList.append(split_info[5]) 
                age_gradeList.append(None)
            
            
        else: #len(split_info) == 5:
            
            tv_stationList.append(None) # 방송국 정보가 없고
            
            if age_found == True: # 국가정보가 없는 경우
                genreList.append(split_info[3]) 
                contryList.append(None) 
                age_gradeList.append(split_info[4])
                
            else: # 연령 등급이 없는 경우
                genreList.append(split_info[3]) 
                contryList.append(split_info[4]) 
                age_gradeList.append(None)
                
                
    else: # 영화인 경우
        
        tv_stationList.append(None)
        
        if len(split_info) >= 7: # 모든 정보가 있는 경우
        
            genreList.append(split_info[3]) 
            contryList.append(split_info[4]) 
            running_timeList.append(split_info[5])   
            
            if age_found == True: # 연령 등급이 있는 경우(7 or 10)
                age_gradeList.append(split_info[6])
                
            else: # 연령 등급이 없는 경우(9)
                age_gradeList.append(None)
 
        elif len(split_info) == 6:
            
            if age_found == True: # 상영시간만 없는 경우
                genreList.append(split_info[3]) 
                contryList.append(split_info[4]) 
                running_timeList.append(None)
                age_gradeList.append(split_info[5])
            
            else: # 연령 등급이 없는 경우
                genreList.append(split_info[3]) 
                contryList.append(split_info[4]) 
                running_timeList.append([split_info[5]])
                age_gradeList.append(None)
                
        
        else: #len(split_info) == 5, 상영시간과 연령정보가 없는 경우
            
            genreList.append(split_info[3]) 
            contryList.append(split_info[4]) 
            running_timeList.append(None)
            age_gradeList.append(None)
                
        

# merged_df에 merge
# 데이터프레임 생성
split_df = pd.DataFrame({
    'id': id_data,
    '제목': titleList,
    '개봉년도': release_yerList,
    '장르': genreList,
    '국가': contryList,
    '상영시간': running_timeList,
    '연령등급': age_gradeList,
    '방송국': tv_stationList,
})

merge2_df = pd.merge(merge_df, split_df, on='id', how='outer')
merge2_df.drop(labels='컨텐츠 정보',axis=1, inplace=True)

print(merge2_df.count())
print(merge2_df.head(5))   

merge2_df.to_csv('C:/Crawling_Watcha/csv/split_merge.csv',encoding='utf-8-sig', mode='w', index=False)


#=================================================================================================================================

# 모든 데이터 합치기
tv_info_df = pd.read_csv('C:/Crawling_Watcha/csv/watcha_tv_info.csv', encoding='cp949')
content_info_df = pd.read_csv('C:/Crawling_Watcha/csv/split_merge.csv', encoding='utf-8-sig')

final_df = pd.merge(content_info_df, tv_info_df, on='id', how='outer')

# 조건에 따라 상영시간_y와 상영시간 칼럼 값 합치기
final_df['상영시간'] = final_df.apply(lambda x: x['상영시간_y'] if x['종류'] == 'tv' else x['상영시간_x'], axis=1)
final_df.drop(['상영시간_x', '상영시간_y'], axis=1, inplace=True)

# 밀린 데이터 drop
drop_id = ['m5GX0v2','mOlEGLd','mOVvmLg','tR4JKKy','tR72L5x']
final_df = final_df.drop(final_df[final_df['id'].isin(drop_id)].index)

# '연령 등급' 열의 누락 데이터를 바로 앞에 있는 값으로 치환
final_df['연령등급'].fillna(method='ffill', inplace=True)

# '평균 평점' 열의 누락 데이터를 바로 앞에 있는 값으로 치환
final_df['평균 평점'].fillna(method='ffill', inplace=True)

# 결측치를 'unknown'으로 변경
final_df.fillna('unknown', inplace=True)

# 국가와 장르의 첫번째 값만 남기기
final_df['국가'] = final_df['국가'].apply(lambda x: x.split(",")[0])
final_df['장르'] = final_df['장르'].apply(lambda x: x.split("/")[0])

# 상영시간 칼럼에서 '[', ']', '"' 문자 제거하는 함수 정의
def remove_characters(text):
    text = text.replace('[', '').replace(']', '').replace("'", '')
    return text

# 상영시간 칼럼에 함수 적용하여 문자 제거 후 업데이트
final_df['상영시간'] = final_df['상영시간'].apply(remove_characters)

# '종류' 열의 값을 변경
final_df['종류'] = final_df['종류'].apply(lambda x: 'TV 프로그램' if x == 'tv' else '영화' if x == 'movie' else x)

final_df.to_csv('C:/Crawling_Watcha/csv/watcha.csv',encoding='utf-8-sig', mode='w', index=False)











