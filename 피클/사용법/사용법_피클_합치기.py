import os
import pickle
import pandas as pd

# 설정
pickle_dir = '/Users/harry/LG DX SCHOOL/dx-project/피클/사용법'
output_filename = '사용법_merged.pkl'
output_path = os.path.join(pickle_dir, output_filename)
columns_to_keep = ['title', 'content', 'comment']

# 병합할 피클 파일 목록 가져오기
pickle_files = [f for f in os.listdir(pickle_dir) if f.endswith('.pkl') and f != output_filename]

# 데이터프레임들을 저장할 리스트
df_list = []

# 각 피클 파일을 순회하며 데이터프레임으로 변환 후 리스트에 추가
for pkl_file in pickle_files:
    file_path = os.path.join(pickle_dir, pkl_file)
    with open(file_path, 'rb') as f:
        try:
            data = pickle.load(f)
            # 데이터가 리스트 형태일 경우 데이터프레임으로 변환
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, pd.DataFrame):
                df = data
            else:
                print(f"'{pkl_file}'의 데이터 형식이 리스트 또는 데이터프레임이 아니므로 건너뜁니다.")
                continue
            df_list.append(df)
            print(f"'{pkl_file}' 로드 완료.")
        except Exception as e:
            print(f"'{pkl_file}' 로드 중 오류 발생: {e}")

# 모든 데이터프레임 병합
if df_list:
    merged_df = pd.concat(df_list, ignore_index=True)
    
    # 존재하는 컬럼만 선택
    existing_columns = [col for col in columns_to_keep if col in merged_df.columns]
    missing_columns = set(columns_to_keep) - set(existing_columns)
    if missing_columns:
        print(f"다음 컬럼이 없어 제외합니다: {list(missing_columns)}")

    final_df = merged_df[existing_columns]

    # 결과를 새 피클 파일로 저장
    with open(output_path, 'wb') as f:
        pickle.dump(final_df, f)

    print(f"\n병합 완료. 총 {len(final_df)}개의 행이 '{output_path}'에 저장되었습니다.")
    print("결과 데이터프레임 정보:")
    final_df.info()
    print("\n상위 5개 행:")
    print(final_df.head())
else:
    print("병합할 데이터가 없습니다.")
