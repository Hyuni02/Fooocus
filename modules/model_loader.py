import os
import sys
from urllib.parse import urlparse
from typing import Optional

# 프로젝트의 루트 경로를 추가
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

def load_file_from_url(
        url: str,
        *,
        model_dir: str,
        progress: bool = True,
        file_name: Optional[str] = None,
) -> str:
    """Download a file from `url` into `model_dir`, using the file present if possible.

    Returns the path to the downloaded file.
    """
    domain = os.environ.get("HF_MIRROR", "https://huggingface.co").rstrip('/')
    url = str.replace(url, "https://huggingface.co", domain, 1)
    os.makedirs(model_dir, exist_ok=True)
    if not file_name:
        parts = urlparse(url)
        file_name = os.path.basename(parts.path)
    cached_file = os.path.abspath(os.path.join(model_dir, file_name))
    if not os.path.exists(cached_file):
        print(f'Downloading: "{url}" to {cached_file}\n')
        from torch.hub import download_url_to_file
        if 'civitai' in url:
            from civitai.CivitaiDownloader import download_model
            model_id = url.split('/')[-1]
            download_model(model_id, cached_file)
        else:
            download_url_to_file(url, cached_file, progress=progress)
    return cached_file
