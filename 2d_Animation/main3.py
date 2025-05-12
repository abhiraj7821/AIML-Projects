from fastapi import FastAPI, HTTPException
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, CrawlerMonitor, DisplayMode, MemoryAdaptiveDispatcher
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class CrawlResponse(BaseModel):
    url: str
    status_code: int
    content_preview: str | None = None
    metadata: dict | None = None
    internal_links_count: int | None = None
    external_links_count: int | None = None

@app.post("/crawl", response_model=CrawlResponse)
async def crawl_url(url: HttpUrl):
    browser_config = BrowserConfig(headless=True, verbose=False)
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        check_robots_txt=True,
        stream=False
    )

    dispatcher = MemoryAdaptiveDispatcher(
        memory_threshold_percent=70.0,
        check_interval=1.0,
        max_session_permit=10,
        monitor=CrawlerMonitor(
            display_mode=DisplayMode.DETAILED
        )
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        results = await crawler.arun_many(
            urls=[str(url)],
            config=run_config,
            dispatcher=dispatcher
        )
        
        if not results or not results[0].success:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to crawl {url}: {results[0].error_message if results else 'Unknown error'}"
            )
        
        return process_result(results[0])

def process_result(result) -> CrawlResponse:
    """
    Process a successful crawl result and return structured data.
    
    Args:
        result: CrawlResult object containing page data and metadata
    """
    content_preview = None
    if result.markdown:
        clean_text = ' '.join(result.markdown.split())
        content_preview = clean_text[:150] + '...' if len(clean_text) > 150 else clean_text

    internal_links_count = len(result.links.get("internal", [])) if result.links else None
    external_links_count = len(result.links.get("external", [])) if result.links else None

    return CrawlResponse(
        url=result.url,
        status_code=result.status_code,
        content_preview=content_preview,
        metadata=result.metadata,
        internal_links_count=internal_links_count,
        external_links_count=external_links_count
    )