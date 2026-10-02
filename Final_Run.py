# ============================================================
# RUN CRAWLER
# ============================================================
from crawler import crawl  
from Fast_API import app  
import uvicorn

if __name__ == "__main__":

    seed_urls = [
        "https://www.python.org/"
    ]

    print("Starting crawler...")

    crawl(
        seed_urls,
        max_pages=100
    )

    print()
    print("Crawling complete.")
    print()
    print("Starting search server...")

   

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )