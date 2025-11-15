import pickle

# Define the paths to the pickle files
pickle_file1_path = '/Users/harry/LG DX SCHOOL/dx-project/텍스트 마이닝/블라인드_샤워_838.pkl'
pickle_file2_path = '/Users/harry/LG DX SCHOOL/dx-project/텍스트 마이닝/네이버 카페_샤워_736.pkl'
merged_pickle_path = '/Users/harry/LG DX SCHOOL/dx-project/텍스트 마이닝/merged.pkl'

# Load the data from the first pickle file
with open(pickle_file1_path, 'rb') as f:
    data1 = pickle.load(f)

# Load the data from the second pickle file
with open(pickle_file2_path, 'rb') as f:
    data2 = pickle.load(f)

# Merge the data (assuming the data are lists)
merged_data = data1 + data2

# Save the merged data to a new pickle file
with open(merged_pickle_path, 'wb') as f:
    pickle.dump(merged_data, f)

print(f"'{pickle_file1_path}'와 '{pickle_file2_path}'의 데이터가 성공적으로 병합되어 '{merged_pickle_path}'에 저장되었습니다.")
