# 목표 ./data/아파트, ./data/연립다세대  두 디렉토리에 있느 24개의 CSV 파일을 하나로 합치기

# CSV 인코딩: UTF-8

# 모두 1번째 줄부터 15번째 줄까지는 데이터를 설명하는 내용이니 제거 필요(16번쨰 줄이 열 정보)

# 모두 속성은 같으니 그대로 행 아래에 조인하면 됨

# 최종 파일명: ./data/주거실거래정보.csv  

import pandas as pd
import os
import glob
from tqdm import tqdm
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def merge_housing_data():
    """
    아파트와 연립다세대 디렉토리의 CSV 파일들을 하나로 합치는 함수
    """
    # 데이터 디렉토리 목록
    directories = ['./data/아파트', './data/연립다세대']
    
    combined_df = pd.DataFrame()
    total_files_processed = 0
    
    for directory in directories:
        logger.info(f"\n=== {directory} 디렉토리 처리 시작 ===")
        
        # 해당 디렉토리의 CSV 파일들 찾기
        csv_pattern = os.path.join(directory, "*.csv")
        csv_files = glob.glob(csv_pattern)
        csv_files.sort()  # 파일명으로 정렬
        
        logger.info(f"발견된 CSV 파일 수: {len(csv_files)}")
        
        for i, file_path in enumerate(tqdm(csv_files, desc=f"{os.path.basename(directory)} 파일 처리")):
            try:
                # 16번째 줄부터 읽기 (skiprows=15로 1-15줄 건너뛰기)
                df = pd.read_csv(file_path, encoding='utf-8', skiprows=15)
                
                logger.info(f"파일 {os.path.basename(file_path)} 읽기 완료 - 행: {len(df)}, 열: {len(df.columns)}")
                
                # 첫 번째 파일인 경우 기준 데이터프레임으로 사용
                if total_files_processed == 0:
                    combined_df = df.copy()
                    logger.info(f"첫 번째 파일의 컬럼: {list(df.columns)}")
                else:
                    # 나머지 파일들은 행으로 추가
                    combined_df = pd.concat([combined_df, df], ignore_index=True)
                
                total_files_processed += 1
                logger.info(f"현재까지 누적 행 수: {len(combined_df)}")
                
            except Exception as e:
                logger.error(f"파일 {file_path} 처리 중 오류 발생: {str(e)}")
                continue
    
    # 결과 저장
    output_path = './data/주거실거래정보.csv'
    
    try:
        # data 디렉토리가 없으면 생성
        os.makedirs('./data', exist_ok=True)
        
        # 합쳐진 데이터를 CSV로 저장
        combined_df.to_csv(output_path, index=False, encoding='utf-8')
        
        logger.info(f"\n=== 합치기 작업 완료 ===")
        logger.info(f"처리된 파일 수: {total_files_processed}")
        logger.info(f"최종 데이터 크기: 행 {len(combined_df):,}개, 열 {len(combined_df.columns)}개")
        logger.info(f"저장된 파일: {output_path}")
        
        return combined_df
        
    except Exception as e:
        logger.error(f"파일 저장 중 오류 발생: {str(e)}")
        return None

def check_merged_file():
    """
    합쳐진 파일의 정보를 확인하는 함수
    """
    output_path = './data/주거실거래정보.csv'
    
    if os.path.exists(output_path):
        try:
            df = pd.read_csv(output_path, encoding='utf-8')
            print(f"\n=== 최종 합쳐진 파일 정보 ===")
            print(f"파일 경로: {output_path}")
            print(f"데이터 크기: 행 {len(df):,}개, 열 {len(df.columns)}개")
            print(f"컬럼 목록: {list(df.columns)}")
            print(f"\n첫 5행 미리보기:")
            print(df.head())
            
        except Exception as e:
            logger.error(f"파일 확인 중 오류 발생: {str(e)}")
    else:
        logger.warning(f"파일 {output_path}이 존재하지 않습니다.")

if __name__ == "__main__":
    # 주거 실거래 데이터 합치기 실행
    result_df = merge_housing_data()
    
    if result_df is not None:
        # 결과 확인
        check_merged_file()
    else:
        logger.error("데이터 합치기 실패")

