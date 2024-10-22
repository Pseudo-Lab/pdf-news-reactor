from google.cloud import storage
from dotenv import load_dotenv

load_dotenv(override=True)


def upload_to_gcs(bucket_name: str, source_file_name: str, destination_blob_name: str):
    """GCS에 파일을 업로드하는 함수 (google-cloud-storage 2.18.2 기준)

    Args:
        bucket_name (str): 업로드할 GCS 버킷 이름
        source_file_name (str): 로컬 파일 경로
        destination_blob_name (str): GCS에 저장될 파일 경로
    """
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


# 사용 예시
if __name__ == "__main__":
    bucket_name = "dwlee-news"
    source_file_name = "/home/dwlee.dev0/pdf-news-reactor/crawling/naver_news.html"
    destination_blob_name = "naver_news.html"

    upload_to_gcs(bucket_name, source_file_name, destination_blob_name)
