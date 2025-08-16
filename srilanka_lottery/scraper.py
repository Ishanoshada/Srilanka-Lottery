import requests
from bs4 import BeautifulSoup
import re

def extract_cookie_from_script(html_content):
    """Extract cookie name and value from JavaScript setCookie function.

    Args:
        html_content (str): HTML content containing the setCookie JavaScript function.

    Returns:
        tuple: Cookie name and value, or (None, None) if not found.
    """
    pattern = r"setCookie\(['\"]([^'\"]+)['\"],['\"]([^'\"]+)['\"],\d+\)"
    match = re.search(pattern, html_content)
    if match:
        return match.group(1), match.group(2)
    return None, None

def get_nlb_session():
    """Get session with required cookies for NLB scraping.

    Returns:
        requests.Session: Configured session with cookies.
    """
    url = "https://www.nlb.lk/lotteries"
    session = requests.Session()
    try:
        initial_response = session.get(url, timeout=10)
        initial_response.raise_for_status()
        cookie_name, cookie_value = extract_cookie_from_script(initial_response.text)
        if cookie_name and cookie_value:
            session.cookies.set(cookie_name, cookie_value, domain="www.nlb.lk", path="/")
        return session
    except Exception as e:
        print("Failed to set up session:", e)
        return session

def scrape_nlb_result(lottery_name, draw_or_date):
    """Fetch results from NLB using either draw number or date.

    Args:
        lottery_name (str): Name of the NLB lottery (e.g., 'mega-power').
        draw_or_date (int or str): Draw number (int) or date (str, YYYY-MM-DD).

    Returns:
        dict: Lottery result with draw number, date, letter, and numbers.
    """
    session = get_nlb_session()
    draw_segment = str(draw_or_date).lower()
    url = f"https://www.nlb.lk/results/{lottery_name.lower()}/{draw_segment}"
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        draw_block = soup.find('div', class_='lresult')
        if not draw_block:
            return {"error": "Result block not found"}

        draw_text = draw_block.find('h1')
        draw_number = draw_block.find('p', string=re.compile(r"Draw No"))
        draw_date = draw_block.find('p', string=re.compile(r"Date:"))

        draw_info = draw_text.get_text(strip=True) if draw_text else "Draw info not found"
        draw_no = draw_number.get_text(strip=True).replace("Draw No.:", "").strip() if draw_number else ""
        date = draw_date.get_text(strip=True).replace("Date:", "").strip() if draw_date else ""

        number_tags = draw_block.select('ol.B li')
        numbers = [li.text.strip() for li in number_tags if 'More' not in li.get('class', [])]
        letter = ""
        if number_tags:
            for li in number_tags:
                if 'Letter' in li.get('class', []):
                    letter = li.text.strip()
                    numbers.remove(letter)
                    break

        return {
            "draw_number": draw_no,
            "date": date,
            "letter": letter,
            "numbers": numbers
        }
    except requests.RequestException as e:
        return {"error": f"Request failed: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}
    finally:
        session.close()

def scrape_dlb_result(lottery_name, draw_or_date):
    """Fetch results from DLB using either draw number or date.

    Args:
        lottery_name (str): Name of the DLB lottery (e.g., 'Ada Kotipathi').
        draw_or_date (int or str): Draw number (int) or date (str, YYYY-MM-DD).

    Returns:
        dict: Lottery result with draw info, date, letter, numbers, and prize image URL.
    """
    dlb_lottery_ids = {
        "Ada Kotipathi": 11,
        "Jayoda": 6,
        "Lagna Wasana": 2,
        "Sasiri": 13,
        "Shanida": 5,
        "Super Ball": 3,
        "Supiri Dhana Sampatha": 17,
        "Jaya Sampatha": 8,
        "Kapruka": 12
    }

    lottery_id = dlb_lottery_ids.get(lottery_name)
    if not lottery_id:
        return {"error": f"Lottery {lottery_name} not found in DLB lottery list."}

    draw_segment = str(draw_or_date).lower()
    url = "https://www.dlb.lk/home/popup"
    payload = {
        "lottery": lottery_id,
        "lotteryNo": draw_segment if draw_segment.isdigit() else "",
        "datepicker1": draw_segment if not draw_segment.isdigit() else "",
        "lastsegment": "en"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.dlb.lk/home/en"
    }

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        draw_info_tag = soup.find('h2', class_='lot_m_re_heading')
        draw_info = draw_info_tag.text.strip() if draw_info_tag else "Draw info not found"

        date_info_tag = soup.find('h3', class_='lot_m_re_date')
        date_info = date_info_tag.text.strip() if date_info_tag else "Date not found"

        letter_tag = soup.find('h6', class_='eng_letter')
        letter = letter_tag.text.strip() if letter_tag else ""

        numbers = [tag.text.strip() for tag in soup.find_all('h6', class_='number_shanida number_circle')]

        prize_img_tag = soup.select_one('#resultPo img')
        prize_img_url = prize_img_tag['src'] if prize_img_tag else ""

        return {
            "draw_info": draw_info,
            "date_info": date_info,
            "letter": letter,
            "numbers": numbers,
            "prize_image": prize_img_url
        }
    except requests.RequestException as e:
        return {"error": f"Request failed: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}

def scrape_dlb_lottery_names():
    """Scrape available lottery names from DLB website.

    Returns:
        dict: Dictionary with list of DLB lottery names or error message.
    """
    url = "https://www.dlb.lk/lottery/en"
    session = requests.Session()
    try:
        initial_response = session.get(url, timeout=10)
        initial_response.raise_for_status()
        cookie_name, cookie_value = extract_cookie_from_script(initial_response.text)
        if cookie_name and cookie_value:
            session.cookies.set(cookie_name, cookie_value, domain="www.dlb.lk", path="/")
            response = session.get(url, timeout=10)
            response.raise_for_status()
        else:
            response = initial_response

        soup = BeautifulSoup(response.text, 'html.parser')
        lottery_elements = soup.find_all('h2', class_='inner_heading_lot')
        lottery_names = [element.text.strip() for element in lottery_elements]
        return {"DLB": sorted(set(lottery_names))} if lottery_names else {"error": "No DLB lottery names found"}
    except requests.RequestException as e:
        return {"error": f"Failed to scrape DLB: {str(e)}"}
    finally:
        session.close()

def scrape_nlb_active_lottery_names():
    """Scrape active lottery names from NLB website.

    Returns:
        tuple: Dictionary with list of active NLB lottery names or error message, and session.
    """
    url = "https://www.nlb.lk/lotteries"
    session = requests.Session()
    try:
        initial_response = session.get(url, timeout=10)
        initial_response.raise_for_status()
        cookie_name, cookie_value = extract_cookie_from_script(initial_response.text)
        if cookie_name and cookie_value:
            session.cookies.set(cookie_name, cookie_value, domain="www.nlb.lk", path="/")
            response = session.get(url, timeout=10)
            response.raise_for_status()
        else:
            response = initial_response

        soup = BeautifulSoup(response.text, 'html.parser')
        active_section = soup.find('h1', string='Active Lotteries')
        if not active_section:
            return {"error": "Active Lotteries section not found"}, session

        ul = active_section.find_next('ul', class_='col4 gap20 list')
        if not ul:
            return {"error": "Active lotteries list not found"}, session

        lottery_names = []
        for li in ul.find_all('li'):
            div = li.find('div')
            if div:
                h3_tag = div.find('h3')
                if h3_tag and h3_tag.text.strip():
                    lottery_names.append(h3_tag.text.strip())

        return {"NLB_Active": sorted(set(lottery_names))} if lottery_names else {"error": "No active NLB lottery names found"}, session
    except requests.RequestException as e:
        return {"error": f"Failed to scrape NLB: {str(e)}"}, session

def scrape_nlb_latest_results(session, lottery_name, limit=5):
    """Scrape the latest results for a given NLB lottery.

    Args:
        session (requests.Session): Session with configured cookies.
        lottery_name (str): Name of the NLB lottery.
        limit (int): Maximum number of results to return.

    Returns:
        dict: Dictionary with list of results or error message.
    """
    url = f"https://www.nlb.lk/results/{lottery_name.lower()}"
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table_rows = soup.select('table tbody tr')
        results = []

        for row in table_rows[:limit]:
            columns = row.find_all('td')
            if len(columns) >= 2:
                draw_block = columns[0]
                draw_number = draw_block.find('b').text.strip()
                draw_date = draw_block.get_text(separator=' ', strip=True).replace(draw_number, '').strip()

                number_list = columns[1].select('ol.B li')
                numbers = []
                letter = ""
                for li in number_list:
                    li_text = li.text.strip()
                    if "Letter" in li.get("class", []):
                        letter = li_text
                    elif li_text.isdigit():
                        numbers.append(li_text)

                results.append({
                    "draw": draw_number,
                    "date": draw_date,
                    "letter": letter,
                    "numbers": numbers
                })

        return {"NLB_Results": results}
    except requests.RequestException as e:
        return {"error": f"Failed to fetch NLB results: {str(e)}"}
    finally:
        session.close()


def scrape_dlb_latest_results(lottery_name, limit=5):
   
    dlb_lottery_ids = {
        "Ada Kotipathi": 11,
        "Jayoda": 6,
        "Lagna Wasana": 2,
        "Sasiri": 13,
        "Shanida": 5,
        "Super Ball": 3,
        "Supiri Dhana Sampatha": 17,
        "Jaya Sampatha": 8,
        "Kapruka": 12
    }

    lottery_id = dlb_lottery_ids.get(lottery_name)
    if not lottery_id:
        return {"error": f"Lottery {lottery_name} not found in DLB lottery list."}

    url = "https://www.dlb.lk/result/pagination_re"
    session = requests.Session()
    results = []
    page = 0
    max_pages = 1000  # Large enough for ~1500 results

    try:
        while len(results) < limit and page < max_pages:
            previous_length = len(results)
            payload = {
                "pageId": page,
                "resultID": 14761,  # Verify if dynamic resultID is needed
                "lotteryID": lottery_id,
                "lastsegment": "en"
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.dlb.lk/result/en"
            }

            response = session.post(url, data=payload, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            rows = soup.select("tr")

            if not rows:
                #logging.info(f"No results found on page {page} for {lottery_name}")
                break

            for row in rows:
                if len(results) >= limit:
                    break
                columns = row.find_all("td")
                if len(columns) >= 2:
                    draw_text = columns[0].get_text(strip=True)
                    match = re.match(r"(\d+)\s+\|\s+(.*)", draw_text)
                    if not match:
                        continue
                    draw_number, draw_date = match.groups()

                    numbers = [li.text.strip() for li in columns[2].select("li") if li.text.strip()]
                    letter = next((li.text.strip() for li in columns[2].select("li.res_eng_letter")), "")
                    # Filter out non-numeric values
                    numbers = [n for n in numbers if n.isdigit()]

                    results.append({
                        "draw": draw_number,
                        "date": draw_date,
                        "letter": letter,
                        "numbers": numbers
                    })

            if len(results) == previous_length:
                #logging.info(f"No new results added on page {page} for {lottery_name}")
                break

            page += 1

        #logging.info(f"Fetched {len(results)} results for {lottery_name}")
        return {"DLB_Results": results}
    except requests.RequestException as e:
        #logging.error(f"Failed to fetch DLB results for {lottery_name}: {e}")
        return {"error": f"Failed to fetch DLB results: {str(e)}"}
    finally:
        session.close()