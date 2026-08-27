from __future__ import annotations

import html
import json
import logging
import re
from dataclasses import dataclass
from html.parser import HTMLParser as StdHTMLParser
from typing import Any, Dict, List, Optional, Tuple

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

logger = logging.getLogger(__name__)


class ParserError(Exception):
    """Base exception for parser errors."""
    pass


@dataclass
class ParsedDocument:
    """Data structure for parsed HTML content."""
    url: str
    title: str
    text: str
    meta_description: str
    meta_keywords: List[str]
    language: str
    publish_date: Optional[str]
    author: Optional[str]
    headings: List[Tuple[int, str]]
    links: List[Tuple[str, str]]
    word_count: int
    reading_time_minutes: int


class CustomHTMLParser(StdHTMLParser):
    """Internal standard library HTML parser to extract content and tags."""
    def __init__(self):
        super().__init__()
        self.text_content: List[str] = []
        self.title: str = ""
        self.meta_desc: str = ""
        self.meta_keywords: List[str] = []
        self.language: str = ""
        self.headings: List[Tuple[int, str]] = []
        self.links: List[Tuple[str, str]] = []
        
        self._in_title = False
        self._skip_tags = {'script', 'style', 'nav', 'footer', 'header', 'aside'}
        self._current_skip_tag = None
        self._skip_depth = 0
        
        self._current_heading_level = 0
        self._current_heading_text = []
        
        self._current_link_url = ""
        self._current_link_text = []
        self._in_link = False

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]):
        attr_dict = dict(attrs)
        
        if tag == "html" and "lang" in attr_dict:
            self.language = attr_dict.get("lang", "")
            
        if tag in self._skip_tags:
            self._skip_depth += 1
            if self._current_skip_tag is None:
                self._current_skip_tag = tag
            return
            
        if self._skip_depth > 0:
            return

        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = attr_dict.get("name", "").lower()
            prop = attr_dict.get("property", "").lower()
            content = attr_dict.get("content", "")
            
            if name == "description" or prop == "og:description":
                self.meta_desc = content
            elif name == "keywords":
                self.meta_keywords = [k.strip() for k in content.split(",") if k.strip()]
            elif prop == "og:title" and not self.title:
                self.title = content
                
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._current_heading_level = int(tag[1])
            self._current_heading_text = []
            
        elif tag == "a" and "href" in attr_dict:
            self._in_link = True
            self._current_link_url = attr_dict["href"] or ""
            self._current_link_text = []

        elif tag in ("p", "br", "div", "h1", "h2", "h3", "h4", "h5", "h6"):
            if self.text_content and not self.text_content[-1].endswith("\n\n"):
                self.text_content.append("\n\n")

    def handle_endtag(self, tag: str):
        if tag == self._current_skip_tag:
            self._skip_depth -= 1
            if self._skip_depth == 0:
                self._current_skip_tag = None
            return
            
        if self._skip_depth > 0:
            return
            
        if tag == "title":
            self._in_title = False
            
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            heading_str = "".join(self._current_heading_text).strip()
            if heading_str:
                self.headings.append((self._current_heading_level, heading_str))
            self._current_heading_level = 0
            
        elif tag == "a":
            self._in_link = False
            link_str = "".join(self._current_link_text).strip()
            if link_str and self._current_link_url:
                self.links.append((self._current_link_url, link_str))

    def handle_data(self, data: str):
        if self._skip_depth > 0:
            return
            
        if self._in_title:
            self.title += data
            
        if self._current_heading_level > 0:
            self._current_heading_text.append(data)
            
        if self._in_link:
            self._current_link_text.append(data)
            
        clean_data = data.strip()
        if clean_data:
            self.text_content.append(data)


class HTMLParser:
    """HTML to clean text parser with structured data extraction."""
    def __init__(self):
        pass

    def parse(self, raw_html: str, url: str) -> ParsedDocument:
        """Parse raw HTML into a structured ParsedDocument."""
        try:
            if HAS_BS4:
                return self._parse_bs4(raw_html, url)
            else:
                return self._parse_stdlib(raw_html, url)
        except Exception as e:
            logger.error(f"Error parsing HTML for {url}: {e}")
            raise ParserError(f"Failed to parse {url}") from e

    def _parse_stdlib(self, raw_html: str, url: str) -> ParsedDocument:
        """Fallback standard library parser implementation."""
        parser = CustomHTMLParser()
        parser.feed(raw_html)
        
        raw_text = "".join(parser.text_content)
        raw_text = re.sub(r'[ \t]+', ' ', raw_text)
        clean_text = re.sub(r'\n\s*\n', '\n\n', raw_text).strip()
        
        word_count = len(clean_text.split())
        reading_time = max(1, round(word_count / 200)) # 200 WPM
        
        return ParsedDocument(
            url=url,
            title=parser.title.strip(),
            text=clean_text,
            meta_description=parser.meta_desc,
            meta_keywords=parser.meta_keywords,
            language=parser.language,
            publish_date=None,
            author=None,
            headings=parser.headings,
            links=parser.links,
            word_count=word_count,
            reading_time_minutes=reading_time
        )
        
    def _parse_bs4(self, raw_html: str, url: str) -> ParsedDocument:
        """Primary parser implementation using BeautifulSoup."""
        soup = BeautifulSoup(raw_html, 'html.parser')
        
        language = soup.html.get('lang', '') if soup.html else ''
        
        title = ''
        if soup.title:
            title = soup.title.string or ''
        if not title:
            og_title = soup.find('meta', property='og:title')
            if og_title:
                title = og_title.get('content', '')
                
        meta_desc = ''
        desc_tag = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', property='og:description')
        if desc_tag:
            meta_desc = desc_tag.get('content', '')
            
        meta_keywords = []
        key_tag = soup.find('meta', attrs={'name': 'keywords'})
        if key_tag:
            content = key_tag.get('content', '')
            if content:
                meta_keywords = [k.strip() for k in content.split(',') if k.strip()]
                
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            tag.decompose()
            
        headings = []
        for i in range(1, 7):
            for h in soup.find_all(f'h{i}'):
                text = h.get_text(strip=True)
                if text:
                    headings.append((i, text))
                    
        links = []
        for a in soup.find_all('a', href=True):
            text = a.get_text(strip=True)
            if text:
                links.append((a['href'], text))
                
        text = soup.get_text(separator='\n\n', strip=True)
        text = re.sub(r'[ \t]+', ' ', text)
        clean_text = re.sub(r'\n\s*\n', '\n\n', text).strip()
        
        word_count = len(clean_text.split())
        reading_time = max(1, round(word_count / 200))
        
        return ParsedDocument(
            url=url,
            title=title.strip(),
            text=clean_text,
            meta_description=meta_desc,
            meta_keywords=meta_keywords,
            language=language,
            publish_date=None,
            author=None,
            headings=headings,
            links=links,
            word_count=word_count,
            reading_time_minutes=reading_time
        )
        
    def extract_structured_data(self, raw_html: str) -> Dict[str, Any]:
        """Extract structured data (JSON-LD, Microdata, OpenGraph) from HTML."""
        result = {'json_ld': [], 'microdata': [], 'opengraph': {}}
        try:
            if HAS_BS4:
                soup = BeautifulSoup(raw_html, 'html.parser')
            else:
                soup = None
                
            if soup:
                for script in soup.find_all('script', type='application/ld+json'):
                    try:
                        if script.string:
                            result['json_ld'].append(json.loads(script.string))
                    except json.JSONDecodeError:
                        pass
                        
                for meta in soup.find_all('meta', property=re.compile(r'^og:')):
                    prop = meta.get('property')
                    content = meta.get('content')
                    if prop and content:
                        result['opengraph'][prop[3:]] = content
            else:
                for match in re.finditer(r'<script\s+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', raw_html, re.DOTALL | re.IGNORECASE):
                    try:
                        result['json_ld'].append(json.loads(match.group(1)))
                    except json.JSONDecodeError:
                        pass
                for match in re.finditer(r'<meta\s+(?:property|name)=["\']og:([^"\']+)["\']\s+content=["\']([^"\']+)["\']', raw_html, re.IGNORECASE):
                    result['opengraph'][match.group(1)] = match.group(2)
                    
        except Exception as e:
            logger.error(f"Error extracting structured data: {e}")
            
        return result
