import pandas as pd

# Load the merged pickle file
try:
    df = pd.read_pickle('/Users/harry/LG DX SCHOOL/dx-project/텍스트 마이닝/merged.pkl')

    # Replace None values with empty strings and merge 'title' and 'content'
    df['merged_content'] = df['title'].fillna('').astype(str) + ' ' + df['content'].fillna('').astype(str)
    print("'title'과 'content' 열의 None 값을 공백으로 처리하고 'merged_content'로 병합했습니다.")

    # Drop the 'date' column if it exists
    if 'date' in df.columns:
        df = df.drop(columns=['date'])
        print("'date' 열을 삭제했습니다.")
    else:
        print("'date' 열이 데이터프에임에 없습니다.")
        
    # Drop the original 'title' and 'content' columns
    df = df.drop(columns=['title', 'content'])
    print("'title' 및 'content' 열을 삭제했습니다.")

    # Save the modified DataFrame to a new pickle file
    output_path = '/Users/harry/LG DX SCHOOL/dx-project/텍스트 마이닝/merged_processed.pkl'
    df.to_pickle(output_path)

    print(f"데이터 처리가 완료되어 '{output_path}'에 저장되었습니다.")
    print("처리된 데이터의 처음 5개 행:")
    print(df.head())

except FileNotFoundError:
    print("오류: 'merged.pkl' 파일을 찾을 수 없습니다. 이전 단계의 스크립트를 먼저 실행하세요.")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")
