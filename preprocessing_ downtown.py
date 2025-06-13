# 목표: 현재 디렉토리에 있는 데이터 하나의 큰 csv파일로  합치기(03, 06, 09, 12 총 4개개)

# 인코딩 정보: UTF-8

# 1. 파일 명에 지역명과 월 정보 붙어 있음. 

# 2. 월 정보가 같은 파일끼리 합치기(행 아래에 그대로 조인 ) -> 결국 전국 모든 정보가 합쳐짐짐

# 3. 최종 파일명: 상가(상권)정보_03.csv, 상가(상권)정보_06.csv, 상가(상권)정보_09.csv, 상가(상권)정보_12.csv 총 4개 

import pandas as pd
import os
import glob
import re
from tqdm import tqdm
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def merge_files_by_month():
    """
    ./data/상가 디렉토리의 상가 정보 CSV 파일들을 월별로 합쳐서 ./data에 저장하는 함수
    """
    # 입력 디렉토리와 출력 디렉토리 설정
    input_dir = os.path.join(".", "data", "상가")
    output_dir = os.path.join(".", "data")
    
    # 디렉토리 존재 확인
    if not os.path.exists(input_dir):
        logger.error(f"입력 디렉토리가 존재하지 않습니다: {input_dir}")
        return
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"출력 디렉토리 생성: {output_dir}")
    
    logger.info(f"입력 디렉토리: {input_dir}")
    logger.info(f"출력 디렉토리: {output_dir}")
    
    # CSV 파일 패턴 찾기 (지역명_월.csv 형태)
    csv_pattern = os.path.join(input_dir, "소상공인시장진흥공단_상가(상권)정보_*_*.csv")
    csv_files = glob.glob(csv_pattern)
    logger.info(f"발견된 CSV 파일 개수: {len(csv_files)}")
    
    if len(csv_files) == 0:
        logger.warning(f"입력 디렉토리에서 CSV 파일을 찾을 수 없습니다: {csv_pattern}")
        return
    
    # 월별로 파일들을 그룹화
    month_groups = {}
    
    for file in csv_files:
        # 파일명에서 월 정보 추출 (마지막 _뒤의 숫자.csv)
        filename = os.path.basename(file)
        match = re.search(r'_(\d{2})\.csv$', filename)
        if match:
            month = match.group(1)
            if month not in month_groups:
                month_groups[month] = []
            month_groups[month].append(file)
            logger.info(f"파일 {filename} -> {month}월 그룹에 추가")
    
    logger.info(f"발견된 월별 그룹: {list(month_groups.keys())}")
    
    # 각 월별로 파일 합치기
    for month in sorted(month_groups.keys()):
        files_in_month = month_groups[month]
        logger.info(f"\n{month}월 파일 합치기 시작 - 총 {len(files_in_month)}개 파일")
        
        combined_df = pd.DataFrame()
        
        # 각 파일을 읽어서 합치기
        for i, file in enumerate(tqdm(files_in_month, desc=f"{month}월 파일 처리")):
            try:
                # UTF-8 인코딩으로 파일 읽기
                df = pd.read_csv(file, encoding='utf-8')
                logger.info(f"파일 {os.path.basename(file)} 읽기 완료 - 행: {len(df)}, 열: {len(df.columns)}")
                
                # 첫 번째 파일인 경우 컬럼 정보 저장
                if i == 0:
                    combined_df = df.copy()
                    logger.info(f"첫 번째 파일의 컬럼: {list(df.columns)}")
                else:
                    # 나머지 파일들은 행으로 추가 (concat 사용)
                    combined_df = pd.concat([combined_df, df], ignore_index=True)
                
                logger.info(f"현재까지 누적 행 수: {len(combined_df)}")
                
            except Exception as e:
                logger.error(f"파일 {os.path.basename(file)} 처리 중 오류 발생: {str(e)}")
                continue
        
        # 합쳐진 데이터프레임을 ./data 디렉토리에 새 파일로 저장
        output_filename = os.path.join(output_dir, f"상가(상권)정보_{month}.csv")
        try:
            combined_df.to_csv(output_filename, index=False, encoding='utf-8')
            logger.info(f"{output_filename} 저장 완료 - 최종 행: {len(combined_df)}, 열: {len(combined_df.columns)}")
            
            # 메모리 정리
            del combined_df
            
        except Exception as e:
            logger.error(f"{output_filename} 저장 중 오류 발생: {str(e)}")
    
    logger.info("\n모든 월별 파일 합치기 작업 완료!")

def check_merged_files():
    """
    ./data 디렉토리에 합쳐진 파일들의 정보를 확인하는 함수
    """
    output_dir = os.path.join(".", "data")
    merged_pattern = os.path.join(output_dir, "상가(상권)정보_*.csv")
    merged_files = glob.glob(merged_pattern)
    
    if len(merged_files) == 0:
        logger.warning(f"합쳐진 파일을 찾을 수 없습니다: {merged_pattern}")
        return
    
    for file in merged_files:
        try:
            df = pd.read_csv(file, encoding='utf-8')
            logger.info(f"{os.path.basename(file)}: 행 {len(df):,}개, 열 {len(df.columns)}개")
        except Exception as e:
            logger.error(f"{os.path.basename(file)} 확인 중 오류: {str(e)}")

if __name__ == "__main__":
    # 월별 파일 합치기 실행
    merge_files_by_month()
    
    # 결과 확인
    print("\n=== 합쳐진 파일 정보 ===")
    check_merged_files()
