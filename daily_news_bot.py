import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

# 깃허브 Secrets(환경 변수)에서 토큰과 Chat ID를 안전하게 불러옵니다.
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def get_categorized_news(query, limit=3):
    # ... (이하 나머지 코드는 기존과 완벽히 동일하게 유지) ...

def get_categorized_news(query, limit=3):
    """특정 키워드의 뉴스를 검색하고 정제하여 반환합니다."""
    url = f"https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("item")
        
        news_list = []
        count = 0
        
        for item in items:
            title = item.title.text
            link = item.link.text
            
            # 단순 사진 기사나 인사 동정 등 질이 떨어지는 기사 1차 필터링
            if "포토" in title or "인사]" in title or "부고]" in title:
                continue
                
            news_list.append(f"🔹 <a href='{link}'>{title}</a>")
            count += 1
            
            if count >= limit:
                break
                
        return "\n".join(news_list)
    except Exception as e:
        return f"뉴스 크롤링 오류: {e}"

def generate_report():
    """수집한 뉴스를 카테고리별로 나누어 보고서 양식으로 조립합니다."""
    # 한국 시간 기준 오늘 날짜 가져오기
    tz_kr = pytz.timezone('Asia/Seoul')
    today_str = datetime.now(tz_kr).strftime('%Y년 %m월 %d일')

    # 카테고리별 검색어 분리
    market_news = get_categorized_news("부동산 OR 아파트 OR 집값 동향", limit=4)
    tax_news = get_categorized_news("양도세 OR 보유세 OR 종부세 개편", limit=3)

    # 보고서 텍스트 템플릿
    report = f"""
📋 <b>[일일 부동산 및 세금 동향 보고서]</b>
📅 {today_str}

🏠 <b>[시장 동향: 부동산 / 아파트 / 집값]</b>
{market_news}

💰 <b>[조세 정책: 양도세 / 보유세 등]</b>
{tax_news}

💡 <i>오늘도 성공적인 하루 보내세요!</i>
"""
    return report.strip()

def send_telegram_report():
    """완성된 보고서를 텔레그램으로 전송합니다."""
    print("보고서를 생성하여 텔레그램으로 전송합니다...")
    report_message = generate_report()
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": report_message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True # 링크 미리보기 방지 (메시지가 너무 길어지는 것 방지)
    }
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("✅ 텔레그램 보고서 전송 완료!")
    else:
        print(f"❌ 전송 실패: {response.text}")

if __name__ == "__main__":
    send_telegram_report()