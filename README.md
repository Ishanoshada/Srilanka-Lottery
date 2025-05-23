
# SriLanka Lottery

The `srilanka-lottery` package is a Python library designed to scrape lottery results and related information from Sri Lanka's National Lottery Board (NLB) and Development Lottery Board (DLB) websites. It provides a simple and efficient way to access lottery data, including specific draw results by draw number or date, lists of available lotteries, and the latest results for both NLB and DLB lotteries. Whether you're building a data analysis tool, a lottery result aggregator, or simply exploring lottery data, this package streamlines the process with robust web scraping capabilities.

## Features

- Retrieve specific lottery results by draw number or date for NLB and DLB lotteries.
- Scrape lists of active NLB lotteries and available DLB lotteries.
- Fetch the latest results for a specified number of draws.
- Handle cookies and session management automatically for reliable scraping.
- Well-documented functions with error handling for robust usage.
- Lightweight and easy to integrate into larger projects.

## Installation

### Prerequisites

- Python 3.6 or higher
- `pip` (Python package manager)

### Install via PyPI

To install the `srilanka-lottery` package, run the following command:

```bash
pip install srilanka-lottery
```

This will automatically install the required dependencies: `requests` and `beautifulsoup4`.

### Install from Source

If you prefer to install from the source code (e.g., for development or customization):

1. Clone the repository:
   ```bash
   git clone https://github.com/ishanoshada/Srilanka-Lottery.git
   cd Srilanka-Lottery
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install the package locally:
   ```bash
   pip install .
   ```

## Usage

The `srilanka-lottery` package provides several functions to interact with NLB and DLB lottery data. Below are detailed examples demonstrating how to use each function.

### Example 1: Scrape Lottery Names

Retrieve the list of available lotteries from DLB and active lotteries from NLB.

```python
from srilanka_lottery import scrape_dlb_lottery_names, scrape_nlb_active_lottery_names

# Scrape DLB lottery names
dlb_names = scrape_dlb_lottery_names()
print("DLB Lotteries:", dlb_names.get("DLB", dlb_names.get("error")))

# Scrape NLB active lottery names
nlb_names, session = scrape_nlb_active_lottery_names()
print("NLB Active Lotteries:", nlb_names.get("NLB_Active", nlb_names.get("error")))
```

**Example Output**:
```
DLB Lotteries: ['Ada Kotipathi', 'Jayoda', 'Lagna Wasana', ...]
NLB Active Lotteries: ['Mega Power', 'Dhana Nidhanaya', ...]
```

### Example 2: Scrape Specific Lottery Results

Fetch results for a specific draw number or date for an NLB or DLB lottery.

```python
from srilanka_lottery import scrape_nlb_result, scrape_dlb_result

# Fetch NLB result by draw number
nlb_result = scrape_nlb_result("mega-power", 2166)
print("NLB Result (Draw 2166):", nlb_result)

# Fetch NLB result by date
nlb_result_date = scrape_nlb_result("mega-power", "2025-05-01")
print("NLB Result (2025-05-01):", nlb_result_date)

# Fetch DLB result by draw number
dlb_result = scrape_dlb_result("Ada Kotipathi", 2608)
print("DLB Result (Draw 2608):", dlb_result)

# Fetch DLB result by date
dlb_result_date = scrape_dlb_result("Ada Kotipathi", "2025-05-01")
print("DLB Result (2025-05-01):", dlb_result_date)
```

**Example Output**:
```
NLB Result (Draw 2166): {'draw_number': '2166', 'date': '2025-05-01', 'letter': 'A', 'numbers': ['12', '34', '56', '78']}
NLB Result (2025-05-01): {'draw_number': '2166', 'date': '2025-05-01', 'letter': 'A', 'numbers': ['12', '34', '56', '78']}
DLB Result (Draw 2608): {'draw_info': 'Ada Kotipathi 2608', 'date_info': '2025-05-01', 'letter': 'Y', 'numbers': ['11', '22', '33', '44'], 'prize_image': ''}
DLB Result (2025-05-01): {'draw_info': 'Ada Kotipathi 2608', 'date_info': '2025-05-01', 'letter': 'Y', 'numbers': ['11', '22', '33', '44'], 'prize_image': ''}
```

### Example 3: Scrape Latest Results

Retrieve the latest results for a specified number of draws.

```python
from srilanka_lottery import scrape_nlb_latest_results, scrape_dlb_latest_results, scrape_nlb_active_lottery_names

# Get NLB session
_, session = scrape_nlb_active_lottery_names()

# Fetch latest NLB results
nlb_latest = scrape_nlb_latest_results(session, "mega-power", limit=3)
for result in nlb_latest.get("NLB_Results", []):
    print(f"NLB Draw {result['draw']} ({result['date']}): {result['letter']} {result['numbers']}")

# Fetch latest DLB results
dlb_latest = scrape_dlb_latest_results("Ada Kotipathi", limit=3)
for result in dlb_latest.get("DLB_Results", []):
    print(f"DLB Draw {result['draw']} ({result['date']}): {result['letter']} {result['numbers']}")
```

**Example Output**:
```
NLB Draw 2166 (2025-05-01): A ['12', '34', '56', '78']
NLB Draw 2165 (2025-04-30): B ['15', '25', '45', '65']
NLB Draw 2164 (2025-04-29): C ['10', '20', '30', '40']
DLB Draw 2608 (2025-05-01): Y ['11', '22', '33', '44']
DLB Draw 2607 (2025-04-30): Z ['12', '23', '34', '45']
DLB Draw 2606 (2025-04-29): X ['13', '24', '35', '46']
```

## Functions

The package includes the following functions:

- **`scrape_nlb_result(lottery_name, draw_or_date)`**: Fetch NLB lottery results by draw number (int) or date (str, YYYY-MM-DD). Returns a dictionary with draw number, date, letter, and numbers.
- **`scrape_dlb_result(lottery_name, draw_or_date)`**: Fetch DLB lottery results by draw number or date. Returns a dictionary with draw info, date, letter, numbers, and prize image URL.
- **`scrape_dlb_lottery_names()`**: Retrieve a list of available DLB lotteries. Returns a dictionary with a sorted list of names or an error message.
- **`scrape_nlb_active_lottery_names()`**: Retrieve a list of active NLB lotteries. Returns a tuple containing a dictionary with a sorted list of names or an error message and the session object.
- **`scrape_nlb_latest_results(session, lottery_name, limit=5)`**: Fetch the latest NLB lottery results up to the specified limit. Requires a session from `scrape_nlb_active_lottery_names`. Returns a dictionary with a list of results.
- **`scrape_dlb_latest_results(lottery_name, limit=5)`**: Fetch the latest DLB lottery results up to the specified limit. Returns a dictionary with a list of results.

## Supported Lotteries

### DLB Lotteries
The package supports the following DLB lotteries (as of the latest update):
- Ada Kotipathi
- Jayoda
- Lagna Wasana
- Sasiri
- Shanida
- Super Ball
- Supiri Dhana Sampatha
- Jaya Sampatha
- Kapruka

### NLB Lotteries
The package can scrape results for any active NLB lottery. Use `scrape_nlb_active_lottery_names()` to get the current list of active lotteries. Examples include:
- Mega Power
- Dhana Nidhanaya
- Mahajana Sampatha
- And more, depending on the active lotteries at the time of scraping.

## Troubleshooting

### Common Issues

- **"Result block not found" or "Request failed" errors**:
  - Ensure you have a stable internet connection.
  - The NLB or DLB website structure may have changed. Check the website manually and consider updating the package or reporting an issue.
  - The draw number or date may not exist. Verify the input parameters.

- **Cookie extraction failing**:
  - The `setCookie` function in the website’s JavaScript may have changed. Report this issue to the package maintainers.

- **Dependencies not installed**:
  - Run `pip install requests beautifulsoup4` to ensure dependencies are installed.

### Debugging Tips

- Enable verbose logging by modifying the code to print additional debug information (e.g., HTTP response status codes).
- Check the raw HTML response if parsing fails using `print(response.text)` in the relevant function.
- Test with different draw numbers or dates to isolate the issue.

## FAQ

### Q: What do I need to use this package?
A: You need Python 3.6 or higher and the `requests` and `beautifulsoup4` libraries, which are automatically installed when you install the package via pip.

### Q: Can I scrape results for any NLB lottery?
A: Yes, as long as the lottery is active. Use `scrape_nlb_active_lottery_names()` to get the current list of active lotteries.

### Q: Why am I getting an "error" key in the response?
A: The error key indicates a problem, such as an invalid lottery name, unreachable website, or missing data. Check the error message for details and ensure your inputs are correct.

### Q: Is this package legal to use?
A: This package is designed for educational and personal use to scrape publicly available data. Ensure you comply with the terms of service of the NLB and DLB websites and applicable laws in your jurisdiction.

### Q: How do I contribute to this package?
A: Contributions are welcome! See the "Contributing" section below for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions to improve the `srilanka-lottery` package! To contribute:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix.
3. Make your changes and write tests if applicable.
4. Submit a pull request with a clear description of your changes.

Please ensure your code follows the existing style and includes appropriate documentation. For major changes, open an issue first to discuss your proposal.

## Contact

For questions, bug reports, or support, please contact [ic31908@gmail.com](mailto:ic31908@gmail.com) or open an issue on the [GitHub repository](https://github.com/ishanoshada/srilanka-lottery).

## Acknowledgements

- Built with [requests](https://requests.readthedocs.io/) and [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/).
- Inspired by the need for accessible lottery data in Sri Lanka.
- Thanks to the open-source community for providing tools and resources.

**Repository Views** ![Views](https://profile-counter.glitch.me/srilottery/count.svg)

