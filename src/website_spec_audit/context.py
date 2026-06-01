from dataclasses import dataclass, field
from urllib.parse import urljoin

import httpx
from lxml import html as lxml_html


@dataclass
class FetchedResource:
    url: str
    status_code: int
    headers: httpx.Headers
    text: str
    is_redirect: bool = False
    redirect_url: str | None = None


class AuditContext:
    """Shared state for a single audit run. Caches fetched resources."""

    def __init__(self, url: str, client: httpx.AsyncClient):
        self.url = url
        self.client = client
        self._cache: dict[str, FetchedResource] = {}
        self._parsed_html_cache: dict[str, lxml_html.HtmlElement] = {}

    async def fetch(self, path: str = "/", *, follow_redirects: bool = True) -> FetchedResource:
        full_url = urljoin(self.url, path)
        if full_url in self._cache:
            return self._cache[full_url]
        response = await self.client.get(full_url, follow_redirects=follow_redirects)
        resource = FetchedResource(
            url=str(response.url),
            status_code=response.status_code,
            headers=response.headers,
            text=response.text,
            is_redirect=len(response.history) > 0,
            redirect_url=str(response.url) if response.history else None,
        )
        self._cache[full_url] = resource
        return resource

    async def fetch_html(self, path: str = "/") -> lxml_html.HtmlElement:
        full_url = urljoin(self.url, path)
        if full_url in self._parsed_html_cache:
            return self._parsed_html_cache[full_url]
        resource = await self.fetch(path)
        doc = lxml_html.fromstring(resource.text)
        self._parsed_html_cache[full_url] = doc
        return doc
