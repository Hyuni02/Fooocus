import requests
import os
import re
import sys
import APILoader

# 프로젝트의 루트 경로를 추가
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)


def download_model(model_id: int, dst: str) -> None:
    file_size = None
    url = f"https://api.civitai.com/v1/models/{model_id}"

    headers = {"Authorization": f"Bearer {APILoader.api}"}

    try:
        # 모델 정보 요청
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        model_data = response.json()

        # 첫 번째 버전의 다운로드 URL 가져오기
        file_info = model_data["modelVersions"][0]["files"][0]
        print('file info :', file_info)
        download_url = file_info["downloadUrl"]
        print('download url :', download_url)
        file_name = file_info["name"]
        print('file name :', file_name)

        # 파일 이름에서 특수 문자 제거
        file_name = re.sub(r'[<>:"/\\|?*\n]', '_', file_name)

        # 저장 경로 설정 (절대 경로)
        dst = os.path.abspath(dst)
        os.makedirs(dst, exist_ok=True)  # 디렉토리 생성
        save_file_path = os.path.join(dst, file_name)

        # 모델 파일 다운로드
        file_response = requests.get(download_url, headers=headers, stream=True)
        file_response.raise_for_status()

        with open(save_file_path, "wb") as file:
            for chunk in file_response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"모델이 성공적으로 다운로드되었습니다: {save_file_path}")

    except requests.exceptions.RequestException as e:
        print(f"요청 중 오류 발생: {e}")
    except KeyError as e:
        print(f"데이터 처리 중 오류 발생: {e}")
    except PermissionError as e:
        print(f"파일 저장 중 권한 오류 발생: {e}")
    except OSError as e:
        print(f"파일 저장 중 오류 발생: {e}")
