from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = FastAPI()

chrome_options = Options()
chrome_options.add_argument("--headless")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def get_weather(): # 오늘의 날씨 웹크롤링하는 함수
    try:
        driver.get("https://www.google.com/search?q=오늘의+날씨")
        weather = driver.find_element(By.ID, "wob_dc").text
    except:
        weather = "정보를 찾을 수 없습니다"

    return weather

def get_video_embed_url(weather): # 오늘의 날씨로 노래 추천해주는 함수
    try:
        driver.get(f'https://www.youtube.com/results?search_query={weather}날 듣기 좋은 노래')
        first_video = driver.find_element(By.CSS_SELECTOR, "a#thumbnail")  # <a> 태그 선택
        video_url = first_video.get_attribute("href")  # href 속성에서 URL 가져오기
        print(video_url)
        video_id = video_url.split("v=")[-1].split("&")[0]  # v= 뒤의 ID 추출
        embed_url = f"https://www.youtube.com/embed/{video_id}"  # 임베드 URL 생성
    except:
        embed_url = None
    finally:
        driver.quit()

    return embed_url

weather = get_weather()
embed_url = get_video_embed_url(weather)

@app.get("/", response_class=HTMLResponse)
def main():

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>오늘의 날씨</title>
    </head>
        <body>
            <h1>오늘의 날씨로 노래를 추천해줄게요!</h1>
            <p>오늘의 날씨: {weather}</p>
            <h2>추천 노래:</h2>
            <iframe width='560' height='315' src="{embed_url}" frameborder='0' allow='autoplay; encrypted-media' allowfullscreen></iframe>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
