from googleapiclient.discovery import build
import pandas as pd
import time

# ----------------------------------------------------
# 설정
# ----------------------------------------------------
# 🔑 발급받은 API 키 (보안을 위해 실제 키로 대체해주세요)
API_KEY = "AIzaSyA4VJl2K-81ERhBZRQjJe5x0E40gGgTzPs"
SEARCH_QUERY = "사용법"  # 검색할 키워드
MAX_VIDEOS = 10  # 가져올 영상 개수 (최대 50개 * 페이지 수)

# ----------------------------------------------------
# API 빌드
# ----------------------------------------------------
try:
    youtube = build("youtube", "v3", developerKey=API_KEY)
except Exception as e:
    print(f"❌ API 클라이언트 생성 실패: {e}")
    print("API 키가 올바른지 확인해주세요.")
    exit()


def search_videos(query, max_results):
    """
    키워드로 유튜브 영상 검색.
    영상 ID, 제목, 설명을 반환합니다.
    """
    print(f"🔍 '{query}' 키워드로 영상 검색 시작...")
    videos = []
    try:
        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=max_results
        )
        response = request.execute()

        for item in response["items"]:
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            # 'content' 컬럼을 위해 영상 설명을 가져옵니다.
            description = item["snippet"]["description"]
            videos.append((video_id, title, description))

        print(f"✅ 총 {len(videos)}개의 영상 정보 수집 완료.")
    except Exception as e:
        print(f"❌ 영상 검색 중 오류 발생: {e}")
    return videos


def get_comments(video_id):
    """
    영상 ID를 기반으로 댓글을 가져옵니다.
    [댓글 작성일, 댓글 내용] 리스트를 반환합니다.
    """
    comments = []
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,  # 페이지당 최대
            textFormat="plainText"
        )

        while request:
            response = request.execute()
            for item in response["items"]:
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                # 요청한 컬럼 'date', 'comment'
                date = snippet["publishedAt"]
                text = snippet["textDisplay"]
                comments.append([date, text])

            # 다음 페이지가 있는지 확인
            if 'nextPageToken' in response:
                request = youtube.commentThreads().list_next(request, response)
            else:
                break  # 다음 페이지가 없으면 종료

    except Exception as e:
        # 댓글이 비활성화된 경우(403) 등은 오류 메시지를 출력하지 않고 넘어갑니다.
        pass

    return comments


def main():
    # 1. 영상 검색 (ID, 제목, 설명)
    videos = search_videos(SEARCH_QUERY, MAX_VIDEOS)
    if not videos:
        print("검색된 영상이 없습니다.")
        return

    all_data = []  # 모든 댓글 데이터를 누적할 리스트

    print("\n💬 각 영상의 댓글 수집 시작 (시간이 걸릴 수 있습니다)...")

    # 2. 각 영상을 순회하며 댓글 수집
    for i, (video_id, title, content) in enumerate(videos):
        comments_list = get_comments(video_id)

        if not comments_list:  # 댓글 없으면 건너뛰기
            print(f"   [{i + 1}/{len(videos)}] ⚠️ 댓글 없음: {title[:30]}...")
            continue

        print(f"   [{i + 1}/{len(videos)}] ✅ 댓글 {len(comments_list)}개 수집: {title[:30]}...")

        # 3. 수집된 댓글을 all_data에 추가
        for comment_date, comment_text in comments_list:
            # 요청한 컬럼 순서: title, content, comment, date
            all_data.append([
                title,
                content,
                comment_text,
                comment_date
            ])

        # API 할당량 초과를 방지하기 위한 약간의 대기
        time.sleep(0.1)

    # 4. 모든 데이터 취합 및 저장
    if not all_data:
        print("\n모든 영상에서 수집된 댓글이 없습니다.")
        return

    print(f"\n총 {len(all_data)}개의 댓글을 수집했습니다.")
    print("데이터프레임 생성 및 파일 저장...")

    df = pd.DataFrame(all_data, columns=["title", "content", "comment", "date"])

    # 파일 이름 설정
    safe_query = SEARCH_QUERY.replace(" ", "_")
    output_pickle = f"{safe_query}_aggregated_comments.pkl"
    output_excel = f"{safe_query}_aggregated_comments.xlsx"

    # 피클 파일로 저장
    try:
        df.to_pickle(output_pickle)
        print(f"💾 피클 파일 저장 완료: {output_pickle}")
    except Exception as e:
        print(f"❌ 피클 파일 저장 실패: {e}")

    # 엑셀 파일로 저장
    try:
        df.to_excel(output_excel, index=False, engine='openpyxl')
        print(f"💾 엑셀 파일 저장 완료: {output_excel}")
    except Exception as e:
        print(f"❌ 엑셀 파일 저장 실패: {e}")
        print("   (참고: 'openpyxl' 라이브러리가 설치되었는지 확인해주세요.)")

    print("\n🎉 모든 작업 완료!")


if __name__ == "__main__":
    main()