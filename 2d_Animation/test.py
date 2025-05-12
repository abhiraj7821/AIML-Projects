import asyncio
import httpx
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

# LlamaIndex imports
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.schema import Document

SITEMAP_URL = "https://manim.readthedocs.io/sitemap.xml"

async def fetch_sitemap_urls(sitemap_url: str) -> list[str]:
    async with httpx.AsyncClient() as client:
        response = await client.get(sitemap_url)
        if response.status_code != 200:
            raise Exception("Failed to fetch sitemap")
        sitemap_content = response.text

    urls = []
    for line in sitemap_content.split('\n'):
        if '<loc>' in line:
            url = line.split('<loc>')[1].split('</loc>')[0].strip()
            urls.append(url)
    return urls

def process_result(result):
    content_preview = None
    if result.markdown:
        clean_text = ' '.join(result.markdown.split())
        content_preview = clean_text[:150] + '...' if len(clean_text) > 150 else clean_text

    internal_links_count = len(result.links.get("internal", [])) if result.links else None
    external_links_count = len(result.links.get("external", [])) if result.links else None

    return {
        "url": result.url,
        "status_code": result.status_code,
        "content_preview": content_preview,
        "metadata": result.metadata,
        "internal_links_count": internal_links_count,
        "external_links_count": external_links_count
    }

async def main():
    urls = await fetch_sitemap_urls(SITEMAP_URL)
    if not urls:
        print("No URLs found in sitemap.")
        return

    first_url = urls[0]
    print(f"Crawling: {first_url}")

    browser_config = BrowserConfig(headless=True, verbose=False)
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        check_robots_txt=True,
        stream=False
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(first_url, config=run_config)

    if not result.success:
        print(f"Failed to crawl {first_url}")
        return

    processed = process_result(result)

    print("\nCrawl Result:")
    for k, v in processed.items():
        print(f"{k}: {v}")

    # Step 1: Create LlamaIndex Document
    doc = Document(
        text=result.markdown,
        metadata={"source": result.url}
    )

    # Step 2: Create Vector Index
    print("\nCreating LlamaIndex VectorStoreIndex...")
    index = VectorStoreIndex.from_documents([doc])

    # Step 3: Persist Index
    index.storage_context.persist(persist_dir="manim_index")
    print("Index saved to ./manim_index")

    # Step 4: Query the Index
    storage_context = StorageContext.from_defaults(persist_dir="manim_index")
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()

    question = "How do I install Manim?"
    print(f"\nQuerying index: {question}")
    response = query_engine.query(question)
    print("Answer:\n", response)

if __name__ == "__main__":
    asyncio.run(main())