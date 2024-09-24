import requests
from datetime import datetime

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
    try:
        # "Done" 상태의 작업을 fetch
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
        response.raise_for_status()  # 오류가 발생하면 예외 발생

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
                print("Response status:", update_response.status_code)
                print("Response payload:", update_response.json())

    except Exception as e:
        print('Error fetching or deleting tasks:', e)

# 바로 실행
fetch_and_delete_done_tasks()
