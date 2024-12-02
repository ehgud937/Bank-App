# news/utils.py
import requests
from bs4 import BeautifulSoup
import datetime
from .models import NewsArticle, NewsKeyword
from django.utils import timezone
import pytz

class NaverNewsCrawler:
    def __init__(self):
        self.base_url = "https://news.naver.com/main/list.naver"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
        }
    def get_finance_news(self, page=1):
        print("Fetching news...")
        params = {
            'mode': 'LS2D',
            'mid': 'sec',
            'sid1': '101',  # 경제 섹션
            'sid2': '259',  # 금융 섹션
            'page': page
        }
        
        try:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            articles = []
            for article in soup.select('.type06_headline li, .type06 li'):
                try:
                    # 기사 정보 추출
                    title_tag = article.select_one('dt:not(.photo) a, dt.photo a')
                    title = title_tag.text.strip()  # title 추출
                    url = title_tag['href']
                    
                    press = article.select_one('.writing').text.strip()
                    thumbnail = article.select_one('dt.photo img')
                    thumbnail_url = thumbnail['src'] if thumbnail else None
                    
                    article_info = self._get_article_detail(url)
                    
                    if article_info:
                        articles.append({
                            'title': article_info['title'],  # title 포함
                            'content': article_info['content'],
                            'url': url,
                            'press': press,
                            'published_at': article_info['date'],
                            'thumbnail_url': thumbnail_url,
                            'category': '금융'
                        })
                        
                except Exception as e:
                    print(f"Error processing article: {e}")
                    continue
                    
            return articles
            
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

    def _get_article_detail(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 제목 추출
            title = ""
            title_selectors = [
                '#articleTitle',
                '.media_end_head_headline',
                '#content > div.end_ct > div > h2',
                '.news_headline h4',
                '.article_info h3'
            ]
            
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title = title_elem.text.strip()
                    break

            # 본문 추출        
            content = ""
            content_elem = soup.select_one('#dic_area')
            if content_elem:
                for tag in content_elem.select('script, style, link, span._reserved_video_area'):
                    tag.decompose()
                content = content_elem.get_text(strip=True)
            
            # 날짜 추출 - timezone 적용
            date = None
            date_elem = soup.select_one('.media_end_head_info_datestamp ._ARTICLE_DATE_TIME')
            if date_elem and 'data-date-time' in date_elem.attrs:
                date_text = date_elem['data-date-time']
                naive_date = datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S')  # datetime.datetime 사용
                # KST 시간대 적용
                korea_timezone = pytz.timezone('Asia/Seoul')
                date = korea_timezone.localize(naive_date)
            else:
                # 현재 시간에 시간대 정보 추가
                date = timezone.now()
                
            if not content:
                return None
                
            return {
                'title': title,
                'content': content,
                'date': date
            }
                
        except Exception as e:
            print(f"Error getting article detail for {url}: {str(e)}")
            return None
    
    def update_news(self):
        """뉴스 업데이트 및 키워드 분석"""
        print("Starting update_news...")  # 디버깅용
        articles = self.get_finance_news()
        print(f"Found {len(articles)} articles")  # 디버깅용
        
        created_count = 0
        for article_data in articles:
            try:
                # 중복 체크
                exists = NewsArticle.objects.filter(url=article_data['url']).exists()
                print(f"Processing article: {article_data['title'][:30]}... Exists: {exists}")  # 디버깅용
                
                if not exists:
                    NewsArticle.objects.create(
                        title=article_data['title'],
                        content=article_data['content'],
                        url=article_data['url'],
                        press=article_data['press'],
                        published_at=article_data['published_at'],
                        thumbnail_url=article_data['thumbnail_url'],
                        category=article_data['category']
                    )
                    created_count += 1
                    
                    # 키워드 추출 및 업데이트
                    keywords = self._extract_keywords(article_data['title'])
                    for keyword in keywords:
                        keyword_obj, _ = NewsKeyword.objects.get_or_create(
                            keyword=keyword
                        )
                        keyword_obj.count += 1
                        keyword_obj.save()
                        
            except Exception as e:
                print(f"Error processing article: {e}")  # 디버깅용
                continue
        
        print(f"Created {created_count} new articles")  # 디버깅용
        return created_count

    def _extract_keywords(self, text):
        import re
        from collections import Counter 

        # 불용어 사전
        stop_words = {
            '기자', '뉴스', '신문', '속보', '단독', '특종', '취재', '보도',
            '있다', '하다', '이다', '되다', '않다', '없다', '말다',
            '년도', '월', '일', '이번', '오늘', '내일', '어제',
            '한다', '했다', '됐다', '된다', '하는', '에서', '으로',
            '것으로', '것이다', '이라고', '이라며',
            '금융', '은행', '증권', '보험', '투자', '주식', '채권',
            '펀드', '저축', '예금', '적금', '대출', '운영', '진행',
            '출발', '개장', '특별', '최대', '지원', '접수'
        }

        try:
            text = re.sub(r'[^\w\s]', ' ', text)
            text = re.sub(r'\d+', '', text)
            
            # 단어 분리
            words = text.split()
            
            # 2글자 이상이고 불용어가 아닌 단어만 선택
            filtered_words = [
                word for word in words 
                if len(word) >= 2 and word not in stop_words
            ]

            # 연속된 단어 조합으로 복합어 생성 (2단어)
            compound_words = []
            for i in range(len(filtered_words)-1):
                compound = filtered_words[i] + filtered_words[i+1]
                if len(compound) >= 4:  # 4글자 이상인 복합어만 선택
                    compound_words.append(compound)

            # 단일 키워드와 복합 키워드 결합
            all_keywords = filtered_words + compound_words

            # 빈도수 기반 상위 키워드 추출
            keyword_counter = Counter(all_keywords)
            
            # 가중치 부여
            weighted_keywords = {}
            for word, count in keyword_counter.items():
                # 기본 가중치 = 출현 빈도
                weight = count
                
                # 제목에 있는 키워드에 가중치 부여
                if word in text:
                    weight *= 1.5
                    
                # 복합어에 추가 가중치
                if len(word) >= 4:
                    weight *= 1.2
                    
                weighted_keywords[word] = weight

            # 상위 5개 키워드 반환
            return sorted(
                weighted_keywords.keys(),
                key=lambda x: weighted_keywords[x],
                reverse=True
            )[:5]

        except Exception as e:
            print(f"Error in keyword extraction: {e}")
            words = [w for w in text.split() if len(w) >= 2]
            return list(set(words))[:3]