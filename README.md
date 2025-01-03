# Bahamas News Web Scraper

A simple web scraper that collects news articles from three Bahamian news websites:
- Our News
- ZNS Bahamas
- Eyewitness News

## Requirements

- Python 3.x
- Internet connection

## Setup Instructions

1. **Download the Files**
   - Save these three files in the same folder:
     - `web_scraper.py`
     - `check_dependencies.py`
     - `README.md`

2. **Install Required Packages**
   - Open your terminal/command prompt
   - Navigate to the folder containing the files
   - Run this command to install required packages:
   ```
   python check_dependencies.py
   ```

## How to Use

1. **Run the Scraper**
   - Open your terminal/command prompt
   - Navigate to the folder containing the files
   - Run this command:
   ```
   python web_scraper.py
   ```

2. **Enter the Date**
   - When prompted, enter a date in this format: YYYY-MM-DD
   - Example: 2024-01-15

3. **View Results**
   - The program will create a CSV file named `news_articles_YYYY-MM-DD.csv`
   - You can open this file with Excel or any spreadsheet program
   - The results will show:
     - Source (which news website)
     - Article title
     - Article link

## Example Output

The program will show you:
- How many articles it found from each news source
- The total number of articles
- Where it saved the results

## Troubleshooting

If you get any errors:
1. Make sure you have Python installed
2. Check your internet connection
3. Verify you entered the date in the correct format (YYYY-MM-DD)
4. Try running `check_dependencies.py` again

## Need Help?

If you're having problems:
1. Make sure all files are in the same folder
2. Check that you're typing the commands exactly as shown
3. Verify your internet connection is working 