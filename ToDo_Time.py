import requests
import schedule
import time
from datetime import datetime
from keep_alive import keep_alive

keep_alive()

# Notion API 설정
NOTION_API_KEY = 'secret_lgpdsy2Qp6THVp6HC5UcB966IBWEJpElgEl9G66WNcj'
DATABASE_ID = '1acc99af8b0f4ae78edc34720cb10330'

# Notion API 요청 헤더
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def fetch_and_delete_done_tasks():
    # 현재 시간을 가져옵니다.
    now = datetime.now()

    # 원하는 시간 범위 체크 (예: 오전 2시 33분에만 실행)
    if (18 <= now.hour < 20):
        print("Task executed at:", now)

        # 여기에서 실제 작업 로직을 수행합니다.
        query_payload = {
            "filter": {
                "property": "Status",
                "status": {
                    "equals": "Done"
                }
            }
        }

        response = requests.post(
            f'https://api.notion.com/v1/databases/{DATABASE_ID}/query',
            headers=headers,
            json=query_payload)

        # 응답 상태코드 체크
        if response.status_code == 200:
            items = response.json().get("results", [])
            print(f'Found {len(items)} done tasks to archive.')

            for item in items:
                page_id = item['id']
                # 작업 아카이빙
                update_payload = {"archived": True}
                update_response = requests.patch(
                    f'https://api.notion.com/v1/pages/{page_id}',
                    headers=headers,
                    json=update_payload)

                if update_response.status_code == 200:
                    print(f'Archived task: {page_id}')
                else:
                    print(f"Failed to archive task: {page_id}")
        else:
            print("Failed to fetch tasks:", response.status_code)
    else:
        print("Outside of time range:", now)

# 매 1분마다 fetch_and_delete_done_tasks 함수를 실행
schedule.every().minute.do(fetch_and_delete_done_tasks)

# 계속해서 스케줄을 체크하도록 메인 루프가 필요합니다.
while True:
    schedule.run_pending()
    time.sleep(1)
