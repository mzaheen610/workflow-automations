# Desktop Automations

A collection of automation scripts for macOS, including a Telegram-based screenshot monitoring bot.

## Projects

### 1. ScreenSpy - Remote Desktop Monitoring via Telegram

ScreenSpy is a Python automation tool that captures your desktop screen at regular intervals and sends the screenshots directly to your Telegram chat. This is useful for remote monitoring, time tracking, activity logging, or keeping a visual record of your work sessions.

## ScreenSpy Features

- **Automated Screenshots**: Captures full desktop screenshots at configurable intervals (default: every 5 seconds)
- **Telegram Delivery**: Sends screenshots directly to your Telegram account via a bot
- **Persistent Monitoring**: Runs continuously in the background
- **Organized Storage**: Saves screenshots locally in a `Screenshots/` folder for archival
- **Error Handling**: Displays clear error messages if configuration is missing or Telegram API fails
- **Lightweight**: Minimal resource usage, runs efficiently on macOS

## System Requirements

- **macOS** (tested on macOS with Python 3.10+)
- **Python 3.10 or higher**
- **Internet connection** (for Telegram API communication)
- **pip** (Python package manager, usually comes with Python)

## Prerequisites Setup

### 1. Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Start a conversation and send `/newbot`
3. Follow the prompts to name your bot (e.g., "ScreenSpy Bot")
4. BotFather will provide a **Bot Token** that looks like: `123456789:ABCdefGHIjklmnoPQRstuvWXYZ`
5. Copy this token—you'll need it in the configuration step

### 2. Get Your Telegram Chat ID

1. In Telegram, search for **@userinfobot**
2. Start a conversation with it
3. It will reply with your personal **Chat ID** (a number like `778370786`)
4. Save this ID—you'll need it for the configuration

## Installation

### Step 1: Clone or Download the Repository

```bash
cd /path/to/your/desired/directory
git clone <repository-url>
cd Automations
```

Or download the files manually to your preferred location.

### Step 2: Create a Python Virtual Environment

Navigate to the project directory and create a virtual environment:

```bash
cd /path/to/Automations
python3 -m venv venv
```

### Step 3: Activate the Virtual Environment

```bash
source venv/bin/activate
```

You should see `(venv)` appear in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `pyautogui` - Screenshot and screen automation
- `requests` - HTTP requests to Telegram API
- `schedule` - Job scheduling for recurring screenshots
- `python-dotenv` - Environment variable management
- `pillow` - Image processing (dependency of pyautogui)
- `pyscreeze` - Screen capture (dependency of pyautogui)

## Configuration

### Create a `.env` File

In the project root directory, create a file named `.env` with your Telegram credentials:

```env
TELEGRAM_BOT_API=YOUR_BOT_TOKEN_HERE
CHAT_ID=YOUR_CHAT_ID_HERE
```

**Example:**
```env
TELEGRAM_BOT_API=123456789:ABCdefGHIjklmnoPQRstuvWXYZ
CHAT_ID=778370786
```

⚠️ **Important Security Note**: 
- Never commit the `.env` file to version control
- Keep your bot token and chat ID private
- If accidentally exposed, revoke the token via @BotFather and create a new one

### Optional Configuration

You can adjust the screenshot interval in `screenspy.py` by modifying this line:

```python
schedule.every(5).seconds.do(send_screenshot)
```

Change `5` to your desired interval in seconds. Examples:
- `60` = every minute
- `300` = every 5 minutes
- `1800` = every 30 minutes

## Usage

### Running ScreenSpy

1. **Activate the virtual environment** (if not already active):
   ```bash
   source venv/bin/activate
   ```

2. **Start the monitoring**:
   ```bash
   python3 screenspy.py
   ```

3. **You should see**:
   ```
   Monitoring started...
   ```

4. **Screenshots will be sent** to your Telegram chat at the configured interval

### Stopping ScreenSpy

Press `Ctrl+C` in the terminal to stop the script.

### Running in Background (Optional)

To run ScreenSpy as a background process even after closing the terminal:

```bash
nohup python3 screenspy.py > screenspy.log 2>&1 &
```

To stop it later:
```bash
pkill -f screenspy.py
```

### Using launchd (macOS Auto-Start)

To run ScreenSpy automatically when your Mac starts:

1. Create a file `~/Library/LaunchAgents/com.screenspy.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.screenspy</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/Automations/screenspy.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
        <string>/path/to/Automations/screenspy.log</string>
    <key>StandardErrorPath</key>
        <string>/path/to/Automations/screenspy_error.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
```

2. Replace `/path/to/Automations/` with your actual project path

3. Load the service:
```bash
launchctl load ~/Library/LaunchAgents/com.screenspy.plist
```

4. To unload:
```bash
launchctl unload ~/Library/LaunchAgents/com.screenspy.plist
```

## Troubleshooting

### "TELEGRAM_BOT_API is not set"

**Cause**: The `TELEGRAM_BOT_API` environment variable is missing from your `.env` file.

**Solution**:
1. Verify you have a `.env` file in the project root
2. Check that it contains: `TELEGRAM_BOT_API=YOUR_TOKEN`
3. Restart the script

### "TELEGRAM_CHAT_ID or CHAT_ID is not set"

**Cause**: Neither `TELEGRAM_CHAT_ID` nor `CHAT_ID` is configured.

**Solution**:
1. Add `CHAT_ID=YOUR_CHAT_ID` to your `.env` file
2. Restart the script

### "FileNotFoundError: No such file or directory"

**Cause**: The `Screenshots/` folder doesn't exist or the script can't write to it.

**Solution**:
```bash
mkdir -p Screenshots
chmod 755 Screenshots
```

### Screenshots Not Appearing in Telegram

**Possible causes**:
1. Bot token or chat ID is incorrect—run the test command below
2. Telegram API is blocked by firewall/network
3. Bot doesn't have permissions to message the chat

**Test command**:
```bash
python3 << 'EOF'
import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TELEGRAM_BOT_API')
chat_id = os.getenv('CHAT_ID')

# Test bot connectivity
response = requests.get(f'https://api.telegram.org/bot{token}/getMe')
print(f"Bot check: {response.json()}")

# Send test message
msg = requests.post(f'https://api.telegram.org/bot{token}/sendMessage',
                    data={'chat_id': chat_id, 'text': 'Test message'})
print(f"Test message sent: {msg.json()}")
EOF
```

### High CPU Usage

**Cause**: Screenshot interval is too short.

**Solution**: Increase the interval in `screenspy.py`. Change:
```python
schedule.every(5).seconds.do(send_screenshot)
```
to a longer interval like `schedule.every(60).seconds.do(send_screenshot)`

## Project Structure

```
Automations/
├── screenspy.py           # Main ScreenSpy script
├── requirements.txt       # Python dependencies
├── .env                   # Configuration (not in git)
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── venv/                 # Virtual environment (not in git)
└── Screenshots/          # Saved screenshots folder
    ├── screenshot_1776160855.png
    ├── screenshot_1776160862.png
    └── ...
```

## Security Considerations

- **Never share your `.env` file** or commit it to version control
- **Rotate your bot token** if you suspect it's been compromised
- **Use `python-dotenv`** to keep credentials out of your code
- **Limit screenshot frequency** to manage storage and bandwidth
- **Review TOS**: Check Telegram's terms of service for bot usage policies

## Customization Ideas

- **Filter sensitive windows**: Modify `screenspy.py` to skip certain applications
- **Compress images**: Add PIL/Pillow compression to reduce file size
- **Add annotations**: Include timestamps, system info on screenshots
- **Slack/Discord integration**: Modify the script to send to other services
- **Selective capture**: Capture only specific monitor or region instead of full screen

## Performance Tips

- Increase screenshot interval for better battery life
- Use lower image quality/resolution to reduce file size
- Archive old screenshots regularly to manage storage
- Monitor memory usage: `ps aux | grep python`

## License

Open for personal use. Modify as needed for your workflow.

## Support

If you encounter issues:
1. Check this README's Troubleshooting section
2. Verify all environment variables are set correctly
3. Run the test commands to isolate the problem
4. Check that your Telegram bot and chat ID are correct