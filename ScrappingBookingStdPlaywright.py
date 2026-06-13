import asyncio
import os
import urllib.parse
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def scrape_booking():
    browser=None
    try:
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                page = await context.new_page()
                # Set extra headers to look more like a real browser
                await page.set_extra_http_headers({
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Referer': 'https://www.booking.com/',
                })
            except Exception as e:
                print(f"[ERROR] Failed to launch browser: {e}")
                return []

            query = 'New York'
            search_params = {
                'ss': query,
                'ssne': query,
                'ssne_untouched': query,
                'efdco': '1',
                'label': 'gen173nr-10CAEoggI46AdIM1gEaGyIAQGYATO4ARfIAQzYAQPoAQH4AQGIAgGoAgG4Ap-_ttEGwAIB0gIkOTg3NzQ4YzktMzMwOC00ZDkwLWJmMTMtZmRhMjM0ZGUyODE12AIB4AIB',
                'aid': '304142',
                'lang': 'en-us',
                'sb': '1',
                'src_elem': 'sb',
                'src': 'searchresults',
                'dest_id': '20088325',
                'dest_type': 'city',
                'checkin': '2026-06-13',
                'checkout': '2026-06-15',
                'group_adults': '2',
                'no_rooms': '1',
                'group_children': '0',
            }
            search_url = 'https://www.booking.com/searchresults.html?' + urllib.parse.urlencode(search_params)

            # Navigate to the search URL - use domcontentloaded to avoid waiting for all resources
            try:
                response = await page.goto(search_url, timeout=30000, wait_until='domcontentloaded')
                status = response.status if response else 'No response'
                print(f"[INFO] Navigated to {search_url} with status: {status}")
                print(f"[INFO] Final URL after navigation: {page.url}")
            except Exception as e:
                print(f"[ERROR] Failed to navigate to {search_url}: {e}")
                return []
            
            # Wait for page to render
            await asyncio.sleep(3)
            
            # If redirected to city page, go back to search results
            if '/city/' in page.url or '/searchresults' not in page.url:
                print(f"[WARNING] Detected redirect to {page.url}. Attempting to navigate back to search results...")
                try:
                    response = await page.goto(search_url, timeout=30000, wait_until='domcontentloaded')
                    print(f"[INFO] Re-navigated to search URL. Current URL: {page.url}")
                    await asyncio.sleep(2)
                except Exception as e:
                    print(f"[ERROR] Failed to re-navigate: {e}")

                
            
            # Cookie pop-up handling: try several common selectors and continue if none match
            try:
                print(await page.title())
                print(page.url)
                selectors = [
                    '#onetrust-accept-btn-handler',
                    'button[aria-label="Accept cookies"]',
                    'button:has-text("Accept")',
                    'button:has-text("I agree")',
                ]
                clicked = False
                for sel in selectors:
                    try:
                        await page.wait_for_selector(sel, timeout=3000)
                        await page.click(sel)
                        print(f"[INFO] Accepted cookies with selector: {sel}")
                        clicked = True
                        break
                    except Exception:
                        # try next selector
                        continue

                if not clicked:
                    print("[INFO] No cookie popup found or none of the selectors matched")
            except Exception as e:
                # Non-fatal: log and continue scraping even if cookie handling failed
                print(f"[ERROR] Failed to handle cookie pop-up: {e}")



            # Debug output
            print("URL:", page.url)
            print("Title:", await page.title())

            locator = page.locator('[data-testid="property-card"]')

            print("Count:", await locator.count())

            # wait for the main content to load
            try:
                await page.wait_for_selector('[data-testid="property-card"]', timeout=20000)
            except Exception as e:
                print(f"[ERROR] Main content did not load in time: {e}")
                return []
            
            
            
            # Scroll
            try:
                print("[INFO] Scrolling to load more hotels...")
                await page.mouse.wheel(0, 4000)
                await asyncio.sleep(2)

                await page.evaluate("""
                    (async () => {
                        await new Promise((resolve) => {
                            let totalHeight = 0;
                            let distance = 100;
                            let timer = setInterval(() => {
                                let scrollHeight = document.body.scrollHeight;
                                window.scrollBy(0, distance);
                                totalHeight += distance;
                                if (totalHeight >= scrollHeight) {
                                    clearInterval(timer);
                                    resolve();
                                }
                            }, 100);
                        });
                    })()
                """)
            except Exception as e:
                print(f"[WARNING] Scrolling failed: {e}")

            # Parse
            try:
                content = await page.content()
            
                soup = BeautifulSoup(content, "html.parser")
            
                hotels = soup.select('[data-testid="property-card"]')
            
                print(f"[INFO] Found {len(hotels)} hotel cards")
            
                results = []
            
                for hotel in hotels:
                    name_elem = hotel.select_one('[data-testid="title"]')
                    price_elem = hotel.select_one('[data-testid="price-and-discounted-price"]')
            
                    name = (
                        name_elem.get_text(strip=True)
                        if name_elem
                        else "N/A"
                    )
            
                    price = (
                        price_elem.get_text(strip=True)
                        if price_elem
                        else "N/A"
                    )
            
                    results.append({
                        "name": name,
                        "price": price
                    })
            
                print(f"[INFO] Successfully extracted {len(results)} hotels")
            
                if not results:
                    print("[INFO] No hotels found or failed to extract hotel information")
                else:
                    print("\n" + "=" * 80)
            
                    for i, result in enumerate(results, 1):
                        print(
                            f"{i}. {result['name']} - {result['price']}"
                        )
            
                    print("=" * 80)
            
                return results
            
            except Exception as e:
                print(f"[ERROR] Failed to parse content: {e}")
                return []
            # Output
            if not results:
                print("[INFO] No hotels found or failed to extract hotel information")  
            
            for i,result in enumerate(results):
                print(f"{i+1}. {result['name']} - {result['price']}")
            return results
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
        return []
    finally:
        if browser:
            try:
                await browser.close()
            except Exception as e:
                print(f"[WARNING] Failed to close browser: {e}")


asyncio.run(scrape_booking())