# Anvil Console - Market Hub Management Tool

A secure, feature-rich console application for managing and monitoring your Market Hub Anvil application.

## Features

- 🔐 **Secure API Key Management** - Uses dotenv for secure credential storage
- 📊 **Real-time Dashboard** - System statistics and health monitoring
- 🗄️ **Database Management** - Test connections, view stats, import/export data
- ⚡ **Task Execution** - Manually trigger scheduled tasks
- 📝 **Log Viewer** - View and analyze application logs
- 🔔 **Discord Integration** - Send test notifications
- 🎨 **Rich UI** - Beautiful console interface with tables and progress indicators

## Prerequisites

- Python 3.8 or higher
- Anvil application with Uplink enabled
- Access to your Anvil app's uplink key

## Installation

1. **Clone or download the Market Hub project**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Copy `env.example` to `.env`:
     ```bash
     cp env.example .env
     ```
   - Edit `.env` and add your Anvil uplink key:
     ```
     ANVIL_UPLINK_KEY=your_actual_uplink_key_here
     ```
   - (Optional) Add Discord webhook URL for notifications

4. **Add server module to Anvil:**
   - Copy the contents of `anvil_server_module.py`
   - In your Anvil app, create a new Server Module
   - Paste the code and save

## Getting Your Anvil Uplink Key

1. Open your Anvil app in the Anvil IDE
2. Click on the gear icon (⚙️) in the left sidebar
3. Select "Uplink" from the settings menu
4. Click "Enable server uplink for this app"
5. Copy the Server Uplink key
6. Paste it into your `.env` file

## Usage

### Starting the Console

```bash
python Anvil_Console.py
```

### Main Menu Options

1. **📊 View Dashboard**
   - Displays system statistics
   - Shows API health status
   - Connection status and environment info

2. **🔍 Test Database Connection**
   - Verifies database connectivity
   - Tests read/write operations
   - Displays operation results

3. **⚡ Run Scheduled Task**
   - Manually trigger any scheduled task:
     - Fetch Economic Events
     - Fetch News Articles
     - Process AI Analysis
     - Update Technical Indicators
     - Send Discord Notifications
     - Clean Old Data

4. **📝 View Logs**
   - Display recent application logs
   - Color-coded by severity level
   - Shows timestamp, level, and message

5. **💾 Data Management**
   - Export tables to CSV
   - Import data from CSV (coming soon)
   - View detailed database statistics
   - Backup database (coming soon)

6. **🔔 Send Test Notification**
   - Tests Discord webhook integration
   - Sends formatted test message

7. **🔄 Refresh Statistics**
   - Updates all dashboard metrics
   - Re-checks API health

## Environment Configuration

### Required Variables

- `ANVIL_UPLINK_KEY` - Your Anvil app's uplink key (required)

### Optional Variables

- `DISCORD_WEBHOOK_URL` - Discord webhook for notifications
- `ENVIRONMENT` - Environment name (development/production)
- `DEBUG_MODE` - Enable debug logging (true/false)

## Security Best Practices

1. **Never commit `.env` file to version control**
   - The `.gitignore` file is configured to exclude it
   - Always use `.env.example` as a template

2. **Rotate API keys regularly**
   - Update both `.env` and Anvil app settings

3. **Use environment-specific keys**
   - Different keys for development/production

4. **Monitor access logs**
   - Check `anvil_console.log` for unusual activity

## Troubleshooting

### Connection Issues

1. **"ANVIL_UPLINK_KEY not found"**
   - Ensure `.env` file exists
   - Check the key name is correct
   - Verify no extra spaces or quotes

2. **"Connection failed"**
   - Verify the uplink key is correct
   - Check internet connectivity
   - Ensure Anvil app has uplink enabled

3. **"Database test failed"**
   - Verify server module is installed in Anvil
   - Check table names match your app
   - Ensure proper permissions

### Discord Notifications

1. **"Discord webhook not configured"**
   - Add `DISCORD_WEBHOOK_URL` to `.env`

2. **"Failed to send notification"**
   - Verify webhook URL is correct
   - Check Discord server permissions

## Development

### Adding New Features

1. **New Menu Items:**
   - Add to `choices` list in `main_menu()`
   - Create corresponding method
   - Add server-side support if needed

2. **New Statistics:**
   - Update `gather_statistics()` method
   - Add display logic to `display_dashboard()`

3. **New Tasks:**
   - Add to task list in `run_scheduled_tasks()`
   - Create server function in Anvil

### Logging

The console creates `anvil_console.log` with detailed information:
- Connection events
- Error traces
- Task execution results
- API interactions

## File Structure

```
market-hub/
├── .env                    # Your API keys (git-ignored)
├── .gitignore             # Git ignore rules
├── env.example            # Template for .env
├── requirements.txt       # Python dependencies
├── Anvil_Console.py       # Main console application
├── anvil_server_module.py # Anvil server code
├── README_CONSOLE.md      # This file
├── ProjectOverview.md     # Project documentation
└── ProjectPlanner.md      # Development plan
```

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review `anvil_console.log` for errors
3. Verify Anvil app configuration
4. Check Anvil documentation at https://anvil.works/docs

## License

Part of the Market Hub project - see main project documentation for license details.
