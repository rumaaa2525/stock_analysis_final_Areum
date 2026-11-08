import os
import glob
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

def parse_html_file(file_path):
    """HTML 파일 1개를 읽어 종목코드, 날짜, 종가 등을 추출하는 함수"""
    try:
        with open(file_path, 'r', encoding='euc-kr', errors='ignore') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        
        path_parts = file_path.split(os.sep)
        date_str = path_parts[-2]
        code_str = path_parts[-1].replace('.html', '')
        
        price_elem = soup.find('em', {'class': 'no_up'}) or soup.find('em', {'class': 'no_down'})
        close_price = int(price_elem.text.replace(',', '')) if price_elem else None
        
        return {
            'date': date_str,
            'code': code_str,
            'close': close_price
        }
    except Exception as e:
        return None

if __name__ == '__main__':
    print("🚀 원본 HTML 아카이브 테스트 파싱 시작...")
    base_path = '/mnt/data/stock'
    # 2024년 폴더 중 최근 3일치만 테스트 스캔
    date_folders = sorted(glob.glob(os.path.join(base_path, '2024*')))[-3:]
    
    parsed_records = []
    for folder in tqdm(date_folders, desc="Processing Folders"):
        html_files = glob.glob(os.path.join(folder, '*.html'))
        for fpath in html_files:
            rec = parse_html_file(fpath)
            if rec:
                parsed_records.append(rec)
                
    df_result = pd.DataFrame(parsed_records)
    
    os.makedirs('data/processed', exist_ok=True)
    df_result.to_csv('data/processed/stock_sample.csv', index=False)
    print(f"✅ 정제 완료! 총 {len(df_result):,}건 저장 완료 (data/processed/stock_sample.csv)")
