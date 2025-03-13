# Telegram Chat Analysis

This tool calculates the percentage of days you've been talking in a Telegram 1-on-1 chat over the last year.

## Features

- Analyzes your Telegram 1-on-1 chat history for the past 365 days
- Calculates what percentage of days contained at least one message
- Shows total message count and days with communication
- Interactive chat selection from your available 1-on-1 conversations

## Prerequisites

- Python 3.7 or higher
- Telegram API credentials (api_id and api_hash)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Honorisverum/telegram-chat-analysis.git
   cd telegram-chat-analysis
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the script for the first time to generate a config file:
   ```
   python telegram_chat_analysis.py
   ```

4. Edit the generated `config.ini` file with your Telegram API credentials:
   ```ini
   [Telegram]
   api_id = YOUR_API_ID
   api_hash = YOUR_API_HASH
   phone = YOUR_PHONE_NUMBER
   username = YOUR_USERNAME
   ```

   You can obtain your API credentials by:
   - Going to https://my.telegram.org/apps
   - Logging in with your phone number
   - Creating a new application if you don't have one
   - Copying the api_id and api_hash values

## Usage

1. Run the script:
   ```
   python telegram_chat_analysis.py
   ```

2. The script will display a list of your 1-on-1 chats.

3. Enter the number of the chat you want to analyze.

4. The script will process the messages and display:
   - Total messages analyzed
   - Number of days with communication
   - Percentage of days with communication over the last year

## Example Output

```
Analyzing chat with John Doe...
Analyzing messages from 2024-03-13 to 2025-03-13
Processed 100 messages so far...
Processed 200 messages so far...
Processed 300 messages so far...

--- Results ---
Total messages analyzed: 342
Days with communication: 156 out of 365 days
Percentage of days with communication: 42.74%
```

## Privacy and Security

This script runs locally on your machine and does not send any data to external servers. Your Telegram API credentials are stored locally in the `config.ini` file.

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.