from __future__ import annotations

import asyncio
import logging
import re
import time
import urllib.parse
import urllib.robotparser
from dataclasses import dataclass, field
from typing import AsyncGenerator, Dict, List, Optional, Set, Tuple

try:
    import aiohttp
except ImportError:
    aiohttp = None

logger = logging.getLogger(__name__)


class CrawlerError(Exception):
    """Base exception for crawler errors."""
    pass


class FetchError(CrawlerError):
    """Exception raised when fetching a URL fails."""
    pass


@dataclass
class CrawlConfig:
    """Configuration for the WebCrawler."""
    max_concurrent: int = 50
    delay_between_requests: float = 0.5
    max_depth: int = 3
    max_pages: int = 10000
    user_agent: str = "H11-AGI-Crawler/1.0"
    respect_robots_txt: bool = True
    timeout: float = 30.0
    allowed_domains: Optional[List[str]] = None
    blocked_domains: Optional[List[str]] = None


@dataclass
class CrawlResult:
    """Represents the result of a single URL crawl."""
    url: str
    status_code: int
    content_type: str
    raw_html: str
    headers: Dict[str, str]
    crawl_time: float
    depth: int
    discovered_urls: Set[str] = field(default_factory=set)


class RobotsChecker:
    """Parses and caches robots.txt per domain."""
    def __init__(self, user_agent: str):
        self.user_agent = user_agent
        self.cache: Dict[str, urllib.robotparser.RobotFileParser] = {}
        self.lock = asyncio.Lock()

    async def is_allowed(self, url: str) -> bool:
        """Check if the URL is allowed to be fetched."""
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc
        scheme = parsed.scheme
        if not domain or not scheme:
            return False

        robots_url = f"{scheme}://{domain}/robots.txt"

        async with self.lock:
            if domain not in self.cache:
                parser = urllib.robotparser.RobotFileParser()
                parser.set_url(robots_url)
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(robots_url, timeout=10.0) as resp:
                            if resp.status == 200:
                                text = await resp.text()
                                parser.parse(text.splitlines())
                except Exception as e:
                    logger.debug(f"Failed to fetch robots.txt for {domain}: {e}")
                self.cache[domain] = parser

            parser = self.cache[domain]

        return parser.can_fetch(self.user_agent, url)


class URLFrontier:
    """Priority queue with deduplication and domain-level rate limiting."""
    def __init__(self, config: CrawlConfig):
        self.config = config
        self.queue: asyncio.PriorityQueue[Tuple[int, str, int]] = asyncio.PriorityQueue()
        self.seen: Set[str] = set()
        self.domain_last_access: Dict[str, float] = {}
        self.lock = asyncio.Lock()
        self.pages_crawled = 0

    def _normalize_url(self, url: str) -> str:
        """Normalize URL for deduplication."""
        parsed = urllib.parse.urlparse(url)
        return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, parsed.query, ''))

    def _is_domain_allowed(self, domain: str) -> bool:
        """Check if the domain is permitted by configuration."""
        if self.config.blocked_domains and domain in self.config.blocked_domains:
            return False
        if self.config.allowed_domains and domain not in self.config.allowed_domains:
            return False
        return True

    async def add_url(self, url: str, depth: int, priority: int = 0) -> bool:
        """Add a new URL to the frontier."""
        if self.pages_crawled >= self.config.max_pages:
            return False
        if depth > self.config.max_depth:
            return False

        normalized = self._normalize_url(url)
        parsed = urllib.parse.urlparse(normalized)
        domain = parsed.netloc

        if not self._is_domain_allowed(domain):
            return False

        async with self.lock:
            if normalized in self.seen:
                return False
            self.seen.add(normalized)
            await self.queue.put((priority, normalized, depth))
            return True

    async def get_next(self) -> Optional[Tuple[str, int]]:
        """Get the next URL to fetch, respecting rate limits."""
        while True:
            if self.queue.empty():
                return None
            
            async with self.lock:
                priority, url, depth = await self.queue.get()
                parsed = urllib.parse.urlparse(url)
                domain = parsed.netloc
                
                now = time.time()
                last_access = self.domain_last_access.get(domain, 0)
                elapsed = now - last_access
                
                if elapsed < self.config.delay_between_requests:
                    await self.queue.put((priority, url, depth))
                    self.queue.task_done()
                else:
                    self.domain_last_access[domain] = time.time()
                    self.pages_crawled += 1
                    return url, depth
            
            await asyncio.sleep(0.1)

    def mark_done(self):
        """Mark the last fetched task as done."""
        self.queue.task_done()


class WebCrawler:
    """Async web crawler."""
    def __init__(self, config: CrawlConfig):
        self.config = config
        self.frontier = URLFrontier(config)
        self.robots_checker = RobotsChecker(config.user_agent)
        # Using a simple regex to extract links from href attributes
        self.href_pattern = re.compile(r'href=[\'"]?([^\'" >]+)')

    async def crawl_single(self, url: str, session: aiohttp.ClientSession, depth: int) -> CrawlResult:
        """Fetch a single URL and extract links."""
        if self.config.respect_robots_txt:
            if not await self.robots_checker.is_allowed(url):
                raise FetchError(f"URL {url} is blocked by robots.txt")

        retries = 3
        backoff = 1.0

        for attempt in range(retries):
            try:
                start_time = time.time()
                async with session.get(url, timeout=self.config.timeout) as response:
                    content_type = response.headers.get("Content-Type", "")
                    if "text/html" not in content_type:
                        raise FetchError(f"Skipping non-HTML content type: {content_type}")
                    
                    raw_html = await response.text()
                    crawl_time = time.time() - start_time
                    
                    discovered_urls = set()
                    for match in self.href_pattern.finditer(raw_html):
                        href = match.group(1)
                        joined = urllib.parse.urljoin(url, href)
                        parsed = urllib.parse.urlparse(joined)
                        if parsed.scheme in ("http", "https"):
                            discovered_urls.add(joined)

                    return CrawlResult(
                        url=url,
                        status_code=response.status,
                        content_type=content_type,
                        raw_html=raw_html,
                        headers=dict(response.headers),
                        crawl_time=crawl_time,
                        depth=depth,
                        discovered_urls=discovered_urls
                    )
            except Exception as e:
                if attempt == retries - 1:
                    raise FetchError(f"Failed to fetch {url} after {retries} attempts: {e}")
                await asyncio.sleep(backoff)
                backoff *= 2

        raise FetchError("Unexpected error")

    async def crawl(self, seed_urls: List[str]) -> AsyncGenerator[CrawlResult, None]:
        """Main crawl loop starting from seed URLs."""
        for url in seed_urls:
            await self.frontier.add_url(url, depth=0)

        semaphore = asyncio.Semaphore(self.config.max_concurrent)
        
        async with aiohttp.ClientSession(headers={"User-Agent": self.config.user_agent}) as session:
            tasks = set()
            
            while True:
                while len(tasks) < self.config.max_concurrent:
                    item = await self.frontier.get_next()
                    if not item:
                        break
                    
                    url, depth = item
                    
                    async def fetch_task(u: str, d: int) -> Tuple[str, Optional[CrawlResult], Optional[Exception]]:
                        async with semaphore:
                            try:
                                res = await self.crawl_single(u, session, d)
                                return u, res, None
                            except Exception as ex:
                                return u, None, ex
                    
                    task = asyncio.create_task(fetch_task(url, depth))
                    tasks.add(task)
                
                if not tasks:
                    break
                
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                tasks = pending
                
                for t in done:
                    u, result, error = t.result()
                    if result:
                        for new_url in result.discovered_urls:
                            await self.frontier.add_url(new_url, result.depth + 1)
                        yield result
                    elif error:
                        logger.warning(f"Error crawling {u}: {error}")
                    self.frontier.mark_done()
