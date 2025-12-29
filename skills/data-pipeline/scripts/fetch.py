#!/usr/bin/env python3
"""
Data fetching module for ETL pipelines.

Source: Derived from anthropics/skills PR #151 (geepers agent system)
"""

import json
import time
from typing import Any, Dict, List, Optional
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import ssl


class DataFetcher:
    """Fetch data from various sources (HTTP APIs, files, etc.)."""

    def __init__(
        self,
        base_url: str = "",
        auth_token: str = "",
        max_retries: int = 3,
        timeout: int = 30,
        headers: Dict[str, str] = None,
    ):
        """
        Initialize the data fetcher.

        Args:
            base_url: Base URL for API requests
            auth_token: Authentication token (Bearer or API key)
            max_retries: Maximum retry attempts on failure
            timeout: Request timeout in seconds
            headers: Additional request headers
        """
        self.base_url = base_url.rstrip("/") if base_url else ""
        self.auth_token = auth_token
        self.max_retries = max_retries
        self.timeout = timeout
        self.headers = headers or {}
        self._session = None

    def _make_request(
        self,
        url: str,
        method: str = "GET",
        data: Any = None,
        headers: Dict[str, str] = None,
    ) -> Dict:
        """Make an HTTP request with retry logic."""
        request_headers = {**self.headers, **(headers or {})}

        if self.auth_token:
            if len(self.auth_token) < 50:  # Likely an API key
                request_headers["X-API-Key"] = self.auth_token
            else:  # Likely a Bearer token
                request_headers["Authorization"] = f"Bearer {self.auth_token}"

        if data is not None:
            if isinstance(data, dict):
                request_headers["Content-Type"] = "application/json"
                body = json.dumps(data).encode("utf-8")
            else:
                body = data
        else:
            body = None

        last_error = None

        for attempt in range(self.max_retries):
            try:
                req = Request(url, data=body, headers=request_headers, method=method)

                ctx = ssl.create_default_context()
                with urlopen(req, timeout=self.timeout, context=ctx) as response:
                    content = response.read().decode("utf-8")
                    content_type = response.headers.get("Content-Type", "")

                    if "application/json" in content_type:
                        return {"status": response.status, "data": json.loads(content)}
                    else:
                        return {"status": response.status, "data": content}

            except HTTPError as e:
                last_error = f"HTTP Error {e.code}: {e.reason}"
                if e.code >= 500:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    raise Exception(f"Request failed: {last_error}")

            except URLError as e:
                last_error = f"URL Error: {e.reason}"
                time.sleep(2 ** attempt)
                continue

            except Exception as e:
                last_error = str(e)
                continue

        raise Exception(f"Max retries exceeded. Last error: {last_error}")

    def get(self, endpoint: str, params: Dict[str, str] = None) -> Dict:
        """
        Fetch data from a single endpoint.

        Args:
            endpoint: API endpoint (will be appended to base_url)
            params: Query parameters

        Returns:
            Response data as dictionary

        Examples:
            >>> fetcher = DataFetcher(base_url="https://api.example.com")
            >>> data = fetcher.get("/users/123")
        """
        url = f"{self.base_url}{endpoint}"

        if params:
            query = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"{url}?{query}"

        return self._make_request(url, method="GET")

    def post(self, endpoint: str, data: Dict = None) -> Dict:
        """POST data to an endpoint."""
        url = f"{self.base_url}{endpoint}"
        return self._make_request(url, method="POST", data=data)

    def batch_get(self, endpoints: List[str]) -> List[Dict]:
        """
        Fetch data from multiple endpoints.

        Args:
            endpoints: List of API endpoints

        Returns:
            List of response data

        Examples:
            >>> results = fetcher.batch_get(["/users/1", "/users/2", "/users/3"])
        """
        results = []
        for endpoint in endpoints:
            try:
                results.append(self.get(endpoint))
            except Exception as e:
                results.append({"error": str(e), "endpoint": endpoint})
        return results

    def paginate(
        self,
        endpoint: str,
        page_size: int = 100,
        max_pages: int = 100,
        key: str = "data",
    ) -> List[Dict]:
        """
        Fetch all pages from a paginated API.

        Args:
            endpoint: API endpoint
            page_size: Number of items per page
            max_pages: Maximum pages to fetch
            key: Key for extracting data from response

        Returns:
            All items from all pages

        Examples:
            >>> all_items = fetcher.paginate("/items", page_size=50)
        """
        all_items = []
        page = 1

        while page <= max_pages:
            params = {"page": page, "page_size": page_size}
            response = self.get(endpoint, params=params)

            if key in response.get("data", {}):
                items = response["data"][key]
            elif isinstance(response.get("data"), list):
                items = response["data"]
            else:
                items = response.get("data", {}).get("items", response.get("data", []))

            if not items:
                break

            all_items.extend(items)
            page += 1

            # Rate limiting
            time.sleep(0.1)

        return all_items


def fetch_from_url(url: str, output: str = None, method: str = "GET") -> Dict:
    """
    Simple URL fetcher for CLI use.

    Args:
        url: Full URL to fetch
        output: Optional output file path
        method: HTTP method

    Returns:
        Response data
    """
    fetcher = DataFetcher()
    result = fetcher._make_request(url, method=method)

    if output:
        with open(output, "w", encoding="utf-8") as f:
            if isinstance(result["data"], (dict, list)):
                json.dump(result["data"], f, indent=2, ensure_ascii=False)
            else:
                f.write(result["data"])
        print(f"Data saved to {output}")

    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fetch data from URLs")
    parser.add_argument("url", help="URL to fetch")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--method", "-m", default="GET", help="HTTP method")
    parser.add_argument("--token", "-t", help="Authentication token")
    parser.add_argument("--base-url", "-b", help="Base URL for relative endpoints")
    parser.add_argument("--retries", type=int, default=3, help="Max retries")
    parser.add_argument("--batch", nargs="+", help="Batch fetch multiple endpoints")

    args = parser.parse_args()

    if args.batch:
        fetcher = DataFetcher(
            base_url=args.base_url or "",
            auth_token=args.token or "",
            max_retries=args.retries
        )
        results = fetcher.batch_get(args.batch)
        for i, result in enumerate(results):
            print(f"Endpoint {i+1}: {result}")
    else:
        if args.base_url:
            fetcher = DataFetcher(
                base_url=args.base_url,
                auth_token=args.token or "",
                max_retries=args.retries
            )
            # Extract endpoint from full URL
            endpoint = args.url.replace(args.base_url, "")
            result = fetcher.get(endpoint)
        else:
            result = fetch_from_url(args.url, output=args.output, method=args.method)

        print(json.dumps(result, indent=2, ensure_ascii=False))
