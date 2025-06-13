# 목표: ./data/전력사용 디렉토리에 있는 모든 엑셀 파일 (.xls) 하나의 csv 파일로 만들기 

# 엑셀 파일에는 12행에 열 정보가 있음(년월	시도	시군구	대상가구수(호)	가구당 평균 전력 사용량(kWh)	가구당 평균 전기요금(원))

# 1. 모든 파일의 칼럼명은 같기 때문에 행 아래에 조인하면 됨

# 2. 최종 파일명: ./data/전력사용정보.csv (UTF-8 인코딩)

import pandas as pd
import os
import glob
from tqdm import tqdm
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def merge_electric_usage_data():
    """
    전력사용 디렉토리의 모든 엑셀 파일(.xls)을 하나의 CSV 파일로 합치는 함수
    """
    # 전력사용 디렉토리 경로
    input_directory = './data/전력사용'
    
    logger.info(f"=== 전력사용 데이터 합치기 시작 ===")
    logger.info(f"대상 디렉토리: {input_directory}")
    
    # 엑셀 파일 찾기
    excel_pattern = os.path.join(input_directory, "*.xls")
    excel_files = glob.glob(excel_pattern)
    excel_files.sort()  # 파일명으로 정렬
    
    logger.info(f"발견된 엑셀 파일 수: {len(excel_files)}")
    
    if len(excel_files) == 0:
        logger.error(f"디렉토리 {input_directory}에서 .xls 파일을 찾을 수 없습니다.")
        return None
    
    combined_df = pd.DataFrame()
    total_files_processed = 0
    
    # 각 엑셀 파일 처리
    for i, file_path in enumerate(tqdm(excel_files, desc="엑셀 파일 처리")):
        try:
            # 12행에 열 정보가 있으므로 11행까지 건너뛰기 (skiprows=11)
            df = pd.read_excel(file_path, skiprows=11)
            
            # 빈 행 제거
            df = df.dropna(how='all')
            
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
    output_path = './data/전력사용정보.csv'
    
    try:
        # data 디렉토리가 없으면 생성
        os.makedirs('./data', exist_ok=True)
        
        # 합쳐진 데이터를 CSV로 저장 (UTF-8 인코딩)
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
    output_path = './data/전력사용정보.csv'
    
    if os.path.exists(output_path):
        try:
            df = pd.read_csv(output_path, encoding='utf-8')
            print(f"\n=== 최종 합쳐진 파일 정보 ===")
            print(f"파일 경로: {output_path}")
            print(f"데이터 크기: 행 {len(df):,}개, 열 {len(df.columns)}개")
            print(f"컬럼 목록: {list(df.columns)}")
            
            # 각 시도별 데이터 개수 확인
            if '시도' in df.columns:
                print(f"\n시도별 데이터 개수:")
                sido_counts = df['시도'].value_counts().sort_index()
                for sido, count in sido_counts.items():
                    print(f"  {sido}: {count:,}개")
            
            print(f"\n첫 5행 미리보기:")
            print(df.head())
            
        except Exception as e:
            logger.error(f"파일 확인 중 오류 발생: {str(e)}")
    else:
        logger.warning(f"파일 {output_path}이 존재하지 않습니다.")

if __name__ == "__main__":
    # 전력사용 데이터 합치기 실행
    result_df = merge_electric_usage_data()
    
    if result_df is not None:
        # 결과 확인
        check_merged_file()
    else:
        logger.error("데이터 합치기 실패")