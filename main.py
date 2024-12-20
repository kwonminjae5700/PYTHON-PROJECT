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

weather = get_weather()

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
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
