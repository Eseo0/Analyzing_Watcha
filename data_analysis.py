import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic' # 한국어 텍스트에 폰트 지정

# csv 파일 읽어오기
watcha = pd.read_csv('C:/Crawling_Watcha/csv/watcha.csv', encoding='utf-8-sig')

# 데이터 정보 확인
watcha.info()

#-----------------------------------------------------------------------------------------------------------------

# 1. 종류별 작품 수

ax = sns.countplot(data=watcha, x='종류')

# 각 막대 위에 수치 표시 (정수형태로)
for p in ax.patches:
    height = p.get_height()  # 막대의 높이(데이터 개수)
    ax.text(p.get_x() + p.get_width() / 2., height, f'{int(height)}', ha='center', va='bottom')

plt.ylabel('작품 수')  # y축 이름 설정
plt.title('왓챠 종류별 작품 수') # 제목 추가

plt.show() # 시각화된 plot 보여줌

#-----------------------------------------------------------------------------------------------------------------

# 2. 제작 국가별 작품 수(상위 15개)

# 2-1 전체

# 전체 종류 중 제작 국가별 작품 수 상위 15개 확인
print(watcha['국가'].value_counts().head(15))

# 국가별 작품 수 계산 후 정렬
country_counts = watcha['국가'].value_counts().head(15).sort_values(ascending=False)

# 가로 막대 그래프로 시각화
plt.figure(figsize=(10, 6))  # 그래프 크기 설정
sns.barplot(x=country_counts.values, y=country_counts.index, palette='viridis')

# 각 막대 안에 수치 표시
for index, value in enumerate(country_counts):
    plt.text(value, index, str(value), va='center', ha='left', fontsize=10, color='black')

plt.xlabel('작품 수')  
plt.ylabel('국가')  
plt.title('제작 국가별 작품 수 Top 15')  

plt.show()

# 2-2 영화

# 종류가 영화인 부분만 가져옴
movie = watcha[watcha['종류'] == '영화']

# 영화 중 제작 국가별 작품 수 상위 15개 확인
print(movie['국가'].value_counts().head(15))

# 국가별 작품 수 계산 후 정렬
country_counts = movie['국가'].value_counts().head(15).sort_values(ascending=False)

# 가로 막대 그래프로 시각화
plt.figure(figsize=(10, 6))  # 그래프 크기 설정
sns.barplot(x=country_counts.values, y=country_counts.index, palette='viridis')

# 각 막대 안에 수치 표시
for index, value in enumerate(country_counts):
    plt.text(value, index, str(value), va='center', ha='left', fontsize=10, color='black')
    
plt.xlabel('작품 수')  # x축 레이블 설정
plt.ylabel('국가')  # y축 레이블 설정
plt.title('제작 국가별 영화 작품 수 Top 15')  # 그래프 제목 설정
plt.show()  # 그래프 표시

# 2-3 TV 프로그램

# 종류가 tv 프로그램인 부분만 가져옴
tv = watcha[watcha['종류'] == 'TV 프로그램']

# tv 프로그램 중 제작 국가별 작품 수 상위 15개 확인
print(tv['국가'].value_counts().head(15))

# 국가별 작품 수 계산 후 정렬
country_counts = tv['국가'].value_counts().head(15).sort_values(ascending=False)

# 가로 막대 그래프로 시각화
plt.figure(figsize=(10, 6))  # 그래프 크기 설정
sns.barplot(x=country_counts.values, y=country_counts.index, palette='viridis')

# 각 막대 안에 수치 표시
for index, value in enumerate(country_counts):
    plt.text(value, index, str(value), va='center', ha='left', fontsize=10, color='black')
    
plt.xlabel('작품 수')  # x축 레이블 설정
plt.ylabel('국가')  # y축 레이블 설정
plt.title('제작 국가별 TV 프로그램 작품 수 Top 15')  # 그래프 제목 설정
plt.show()  # 그래프 표시

#-----------------------------------------------------------------------------------------------------------------

# 3. 장르별 작품 수

# 3-1 영화

# 영화만 필터링
movie = watcha[watcha['종류'] == '영화']

# 영화의 장르별 작품 수 계산
genre_counts = movie['장르'].value_counts()

# 작품 수의 비율 계산
genre_percentages = genre_counts / genre_counts.sum() * 100

# 1% 미만인 장르들을 '기타'로 통합
threshold = 1  # 임계치 설정
other_genres = genre_percentages[genre_percentages < threshold].index
movie.loc[movie['장르'].isin(other_genres), '장르'] = '기타'

# 다시 장르별 작품 수 계산
new_genre_counts = movie['장르'].value_counts()

# 새로운 작품 수의 비율 계산
new_genre_percentages = new_genre_counts / new_genre_counts.sum() * 100

# 가장 많은 비율을 차지하는 조각 강조를 위해 explode 설정
max_index = new_genre_percentages.idxmax()
explode = [0.1 if label == max_index else 0 for label in new_genre_percentages.index]

# 원 그래프 그리기 (크기 조절 및 텍스트 설정)
plt.figure(figsize=(20, 20))  # 그래프 크기 설정
patches, texts, autotexts = plt.pie(new_genre_percentages, labels=new_genre_percentages.index,
                                    autopct='%1.1f%%', startangle=90, pctdistance=0.85, labeldistance=1.1, explode=explode)
plt.title('장르별 영화 작품 수 비율', fontsize=20)  # 그래프 제목 설정

# 텍스트 사이즈 설정
for text in texts + autotexts:
    text.set_fontsize(15)

plt.show()  # 그래프 표시


# 3-2 TV 프로그램

# TV 프로그램만 필터링
tv = watcha[watcha['종류'] == 'TV 프로그램']

# TV 프로그램의 장르별 작품 수 계산
genre_counts = tv['장르'].value_counts()

# 작품 수의 비율 계산
genre_percentages = genre_counts / genre_counts.sum() * 100

# 1% 미만인 장르들을 '기타'로 통합
threshold = 1  # 임계치 설정
other_genres = genre_percentages[genre_percentages < threshold].index
tv.loc[tv['장르'].isin(other_genres), '장르'] = '기타'

# 다시 장르별 작품 수 계산
new_genre_counts = tv['장르'].value_counts()

# 새로운 작품 수의 비율 계산
new_genre_percentages = new_genre_counts / new_genre_counts.sum() * 100

# 가장 많은 비율을 차지하는 조각 강조를 위해 explode 설정
max_index = new_genre_percentages.idxmax()
explode = [0.1 if label == max_index else 0 for label in new_genre_percentages.index]

# 원 그래프 그리기 (크기 조절 및 텍스트 설정)
plt.figure(figsize=(20, 20))  # 그래프 크기 설정
patches, texts, autotexts = plt.pie(new_genre_percentages, labels=new_genre_percentages.index,
                                    autopct='%1.1f%%', startangle=90, pctdistance=0.85, labeldistance=1.1, explode=explode)
plt.title('장르별 TV 프로그램 작품 수 비율', fontsize=20)  # 그래프 제목 설정

# 텍스트 사이즈 설정
for text in texts + autotexts:
    text.set_fontsize(15)

plt.show()  # 그래프 표시

#-----------------------------------------------------------------------------------------------------------------

# 4. 개봉년도 구간별 작품 수

# 개봉년도별 작품 수 확인
print(watcha['개봉년도'].unique)

# 1920년대부터 2020년대까지 10년 단위로 구간 설정
bins = [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2030]

# 개봉년도를 각 구간으로 나누기
watcha['연도_구간'] = pd.cut(watcha['개봉년도'], bins=bins, labels=['1920년대', '1930년대', '1940년대', '1950년대', '1960년대', '1970년대', '1980년대', '1990년대', '2000년대', '2010년대', '2020년대'])

# 각 구간별 작품 수 계산
yearly_counts_grouped = watcha['연도_구간'].value_counts().sort_index()

# 바 그래프 그리기
plt.figure(figsize=(12, 6))  # 그래프 크기 설정
ax = sns.barplot(x=yearly_counts_grouped.index, y=yearly_counts_grouped.values, palette='viridis')  # 바 그래프 생성

# 각 막대 위에 수치 표시 (정수형태로)
for p in ax.patches:
    height = p.get_height()  # 막대의 높이(데이터 개수)
    ax.text(p.get_x() + p.get_width() / 2., height, f'{int(height)}', ha='center', va='bottom')

plt.xlabel('연도 구간')  # x축 레이블 설정
plt.ylabel('작품 수')  # y축 레이블 설정
plt.title('개봉년도 구간별 작품 수')  # 그래프 제목 설정
plt.grid(axis='y')  # y축 기준으로만 격자 표시
plt.show()  # 그래프 표시

#-----------------------------------------------------------------------------------------------------------------

# 5. 연령 등급별 작품 수

# 5-1 전체

ax = sns.countplot(data=watcha, x='연령등급')

# 각 막대 위에 수치 표시 (정수형태로)
for p in ax.patches:
    height = p.get_height()  # 막대의 높이(데이터 개수)
    ax.text(p.get_x() + p.get_width() / 2., height, f'{int(height)}', ha='center', va='bottom')

plt.ylabel('작품 수')  # y축 이름 설정
plt.title('연령등급별 작품 수') # 제목 추가

plt.show() # 시각화된 plot 보여줌


# 5-2 영화

# 영화만 필터링
movie = watcha[watcha['종류'] == '영화']

ax = sns.countplot(data=movie, x='연령등급')

# 각 막대 위에 수치 표시 (정수형태로)
for p in ax.patches:
    height = p.get_height()  # 막대의 높이(데이터 개수)
    ax.text(p.get_x() + p.get_width() / 2., height, f'{int(height)}', ha='center', va='bottom')

plt.ylabel('작품 수')  # y축 이름 설정
plt.title('연령등급별 영화 작품 수') # 제목 추가

plt.show() # 시각화된 plot 보여줌


# 5-3 tv 프로그램

# 영화만 필터링
tv = watcha[watcha['종류'] == 'TV 프로그램']

ax = sns.countplot(data=tv, x='연령등급')

# 각 막대 위에 수치 표시 (정수형태로)
for p in ax.patches:
    height = p.get_height()  # 막대의 높이(데이터 개수)
    ax.text(p.get_x() + p.get_width() / 2., height, f'{int(height)}', ha='center', va='bottom')

plt.ylabel('작품 수')  # y축 이름 설정
plt.title('연령등급별 TV 프로그램 작품 수') # 제목 추가

plt.show() # 시각화된 plot 보여줌

#-----------------------------------------------------------------------------------------------------------------

# 7. 평균 평점 4.3 이상의 작품 분석

# '평균 평점' 열의 데이터를 숫자(float) 타입으로 변환
watcha['평균 평점'] = watcha['평균 평점'].astype(float)

# 평균 평점이 4.3 이상인 행 추출
content_4_3 = watcha[watcha['평균 평점'] >= 4.3]

# 7-1 종류별
ax = sns.countplot(data=content_4_3, x='종류')

# 각 막대 위에 수치 표시 (정수형태로)
for p in ax.patches:
    height = p.get_height()  # 막대의 높이(데이터 개수)
    ax.text(p.get_x() + p.get_width() / 2., height, f'{int(height)}', ha='center', va='bottom')

plt.ylabel('작품 수')  # y축 이름 설정
plt.title('종류별 작품 수(평균 평점 4.3 이상)') # 제목 추가

plt.show() # 시각화된 plot 보여줌

# 7-2 연령등급별
ax = sns.countplot(data=content_4_3, x='연령등급')

# 각 막대 위에 수치 표시 (정수형태로)
for p in ax.patches:
    height = p.get_height()  # 막대의 높이(데이터 개수)
    ax.text(p.get_x() + p.get_width() / 2., height, f'{int(height)}', ha='center', va='bottom')

plt.ylabel('작품 수')  # y축 이름 설정
plt.title('연령등급별 작품 수(평균 평점 4.3 이상)') # 제목 추가

plt.show() # 시각화된 plot 보여줌

# 7-3 장르별

genre_counts = content_4_3['장르'].value_counts()
print(genre_counts)

# 작품 수의 비율 계산
genre_percentages = genre_counts / genre_counts.sum() * 100

# 2% 미만인 장르들을 '기타'로 통합
threshold = 1  # 임계치 설정
other_genres = genre_percentages[genre_percentages < threshold].index
content_4_3.loc[content_4_3['장르'].isin(other_genres), '장르'] = '기타'

# 다시 장르별 작품 수 계산
new_genre_counts = content_4_3['장르'].value_counts()

# 새로운 작품 수의 비율 계산
new_genre_percentages = new_genre_counts / new_genre_counts.sum() * 100

# 가장 많은 비율을 차지하는 조각 강조를 위해 explode 설정
max_index = new_genre_percentages.idxmax()
explode = [0.1 if label == max_index else 0 for label in new_genre_percentages.index]

# 원 그래프 그리기 (크기 조절 및 텍스트 설정)
plt.figure(figsize=(26, 26))  # 그래프 크기 설정
patches, texts, autotexts = plt.pie(new_genre_percentages, labels=new_genre_percentages.index,
                                    autopct='%1.1f%%', startangle=90, pctdistance=0.85, labeldistance=1.1, explode=explode)
plt.title('장르별 작품 수 비율(평균 평점 4.3 이상)', fontsize=20)  # 그래프 제목 설정

# 텍스트 사이즈 설정
for text in texts + autotexts:
    text.set_fontsize(17)

plt.show()  # 그래프 표시

# 7-4 제작 국가별

# 제작 국가별 작품 수 계산 후 정렬
country_counts = content_4_3['국가'].value_counts().sort_values(ascending=False)

# 가로 막대 그래프로 시각화
plt.figure(figsize=(10, 6))  # 그래프 크기 설정
sns.barplot(x=country_counts.values, y=country_counts.index, palette='viridis')

# 각 막대 안에 수치 표시
for index, value in enumerate(country_counts):
    plt.text(value, index, str(value), va='center', ha='left', fontsize=10, color='black')
    
plt.xlabel('작품 수')  # x축 레이블 설정
plt.ylabel('국가')  # y축 레이블 설정
plt.title('제작 국가별 작품 수(평균 평점 4.3 이상)')  # 그래프 제목 설정
plt.show()  # 그래프 표시


# 7-5 개봉년도별

# 개봉년도별 작품 수 확인
print(content_4_3['개봉년도'].unique)

# 1920년대부터 2020년대까지 10년 단위로 구간 설정
bins = [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2030]

# 개봉년도를 각 구간으로 나누기
content_4_3['연도_구간'] = pd.cut(content_4_3['개봉년도'], bins=bins, labels=['1920년대', '1930년대', '1940년대', '1950년대', '1960년대', '1970년대', '1980년대', '1990년대', '2000년대', '2010년대', '2020년대'])

# 각 구간별 작품 수 계산
yearly_counts_grouped = content_4_3['연도_구간'].value_counts().sort_index()

# 바 그래프 그리기
plt.figure(figsize=(12, 6))  # 그래프 크기 설정
ax = sns.barplot(x=yearly_counts_grouped.index, y=yearly_counts_grouped.values, palette='viridis')  # 바 그래프 생성

# 각 막대 위에 수치 표시 (정수형태로)
for p in ax.patches:
    height = p.get_height()  # 막대의 높이(데이터 개수)
    ax.text(p.get_x() + p.get_width() / 2., height, f'{int(height)}', ha='center', va='bottom')

plt.xlabel('연도 구간')  # x축 레이블 설정
plt.ylabel('작품 수')  # y축 레이블 설정
plt.title('개봉년도 구간별 작품 수(평균 평점 4.3 이상)')  # 그래프 제목 설정
plt.grid(axis='y')  # y축 기준으로만 격자 표시
plt.show()  # 그래프 표시








