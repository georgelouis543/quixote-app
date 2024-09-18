import httpx
import asyncio


# Asynchronous function to check the final URL of a single URL
async def check_final_url(url):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(url)
        return response.url


# Asynchronous function to process a list of URLs
async def check_urls(urls_list):
    tasks = [check_final_url(url) for url in urls_list]
    results = await asyncio.gather(*tasks)
    return results


# List of URLs to check
urls = [
    "http://example.com",
    "http://httpbin.org/redirect/1",  # This will redirect
    "http://google.com"
]

# Run the async function
asyncio.run(check_urls(urls))
