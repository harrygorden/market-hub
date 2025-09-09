#!/usr/bin/env python3
"""
Anvil Console - Market Hub Management Tool
A secure uplink console for managing and monitoring the Market Hub Anvil application.
"""

import os
import sys
import time
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from contextlib import contextmanager

# Third-party imports
import anvil.server
from anvil.tables import app_tables
import anvil.tables.query as q
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box
from rich.text import Text
import questionary
import requests
import psutil

# Load environment variables
load_dotenv()

# Console setup
console = Console()

# Logging setup
logging.basicConfig(
    level=logging.DEBUG if os.getenv('DEBUG_MODE', 'false').lower() == 'true' else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('anvil_console.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AnvilConsole:
    """Main console application for Market Hub management."""
    
    def __init__(self):
        """Initialize the Anvil Console application."""
        self.uplink_key = os.getenv('ANVIL_UPLINK_KEY')
        self.discord_webhook = os.getenv('DISCORD_WEBHOOK_URL')
        self.environment = os.getenv('ENVIRONMENT', 'development')
        self.connected = False
        self.connection_start = None
        self.stats = {}
        
        # Validate API key
        if not self.uplink_key:
            console.print("[bold red]Error:[/bold red] ANVIL_UPLINK_KEY not found in .env file")
            console.print("Please copy env.example to .env and add your Anvil uplink key")
            sys.exit(1)
    
    @contextmanager
    def anvil_connection(self):
        """Context manager for Anvil connection."""
        try:
            console.print("[yellow]Connecting to Anvil...[/yellow]")
            anvil.server.connect(self.uplink_key, quiet=False)
            self.connected = True
            self.connection_start = datetime.now()
            console.print("[green]✓ Connected to Anvil successfully[/green]")
            yield
        except Exception as e:
            console.print(f"[red]✗ Connection failed: {e}[/red]")
            logger.error(f"Connection error: {e}")
            raise
        finally:
            if self.connected:
                anvil.server.disconnect()
                self.connected = False
                console.print("[yellow]Disconnected from Anvil[/yellow]")
    
    def gather_statistics(self) -> Dict[str, Any]:
        """Gather system and application statistics."""
        stats = {
            'timestamp': datetime.now().isoformat(),
            'environment': self.environment,
            'system': {},
            'database': {},
            'api_health': {}
        }
        
        # System statistics
        try:
            stats['system'] = {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent,
                'python_version': sys.version.split()[0],
                'uptime': str(datetime.now() - self.connection_start) if self.connection_start else 'N/A'
            }
        except Exception as e:
            logger.error(f"Error gathering system stats: {e}")
        
        # Database statistics (when connected)
        if self.connected:
            try:
                # Get table counts
                stats['database'] = anvil.server.call('get_database_stats')
            except Exception as e:
                logger.error(f"Error getting database stats: {e}")
                stats['database'] = {'error': str(e)}
        
        # API health checks
        stats['api_health'] = self.check_api_health()
        
        return stats
    
    def check_api_health(self) -> Dict[str, str]:
        """Check health of external APIs."""
        health = {}
        
        # Check Events API
        try:
            response = requests.get(
                'https://nfs.faireconomy.media/ff_calendar_thisweek.json',
                timeout=5
            )
            health['events_api'] = 'OK' if response.status_code == 200 else f'Error: {response.status_code}'
        except Exception as e:
            health['events_api'] = f'Error: {str(e)[:30]}'
        
        # Check Discord webhook (if configured)
        if self.discord_webhook:
            health['discord'] = 'Configured'
        else:
            health['discord'] = 'Not configured'
        
        return health
    
    def display_dashboard(self):
        """Display the main dashboard with statistics."""
        console.clear()
        
        # Gather statistics
        stats = self.gather_statistics()
        self.stats = stats
        
        # Create layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        
        # Header
        header_text = Text("Market Hub Console", style="bold white on blue", justify="center")
        layout["header"].update(Panel(header_text, box=box.DOUBLE))
        
        # Body - split into columns
        layout["body"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )
        
        # System Stats Table
        system_table = Table(title="System Status", box=box.ROUNDED)
        system_table.add_column("Metric", style="cyan")
        system_table.add_column("Value", style="white")
        
        for key, value in stats.get('system', {}).items():
            system_table.add_row(key.replace('_', ' ').title(), str(value))
        
        layout["body"]["left"].update(Panel(system_table, title="System", border_style="blue"))
        
        # API Health Table
        api_table = Table(title="API Health", box=box.ROUNDED)
        api_table.add_column("Service", style="cyan")
        api_table.add_column("Status", style="white")
        
        for service, status in stats.get('api_health', {}).items():
            color = "green" if "OK" in status or "Configured" in status else "red"
            api_table.add_row(service.replace('_', ' ').title(), f"[{color}]{status}[/{color}]")
        
        layout["body"]["right"].update(Panel(api_table, title="External Services", border_style="blue"))
        
        # Footer
        footer_text = f"Environment: {self.environment} | Connected: {'Yes' if self.connected else 'No'}"
        layout["footer"].update(Panel(footer_text, box=box.ROUNDED))
        
        console.print(layout)
    
    def test_database_connection(self):
        """Test database connection and operations."""
        console.print("\n[cyan]Testing Database Connection...[/cyan]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Testing...", total=4)
            
            try:
                # Test 1: List tables
                progress.update(task, description="Checking available tables...")
                result = anvil.server.call('list_tables')
                progress.update(task, advance=1)
                console.print(f"  ✓ Found {len(result)} tables")
                
                # Test 2: Test read operation
                progress.update(task, description="Testing read operations...")
                test_read = anvil.server.call('test_read_operation')
                progress.update(task, advance=1)
                console.print(f"  ✓ Read operation successful")
                
                # Test 3: Test write operation
                progress.update(task, description="Testing write operations...")
                test_write = anvil.server.call('test_write_operation')
                progress.update(task, advance=1)
                console.print(f"  ✓ Write operation successful")
                
                # Test 4: Get statistics
                progress.update(task, description="Gathering statistics...")
                stats = anvil.server.call('get_database_stats')
                progress.update(task, advance=1)
                console.print(f"  ✓ Statistics retrieved")
                
                console.print("\n[green]All database tests passed![/green]")
                
            except Exception as e:
                console.print(f"\n[red]Database test failed: {e}[/red]")
                logger.error(f"Database test error: {e}")
    
    def run_scheduled_tasks(self):
        """Manually trigger scheduled tasks."""
        console.print("\n[cyan]Available Scheduled Tasks:[/cyan]")
        
        tasks = [
            "Fetch Economic Events",
            "Fetch News Articles",
            "Process AI Analysis",
            "Update Technical Indicators",
            "Send Discord Notifications",
            "Clean Old Data",
            "Back to Main Menu"
        ]
        
        choice = questionary.select(
            "Select a task to run:",
            choices=tasks
        ).ask()
        
        if choice == "Back to Main Menu":
            return
        
        console.print(f"\n[yellow]Running: {choice}...[/yellow]")
        
        try:
            task_map = {
                "Fetch Economic Events": "fetch_events",
                "Fetch News Articles": "fetch_news",
                "Process AI Analysis": "process_ai_analysis",
                "Update Technical Indicators": "update_technicals",
                "Send Discord Notifications": "send_notifications",
                "Clean Old Data": "clean_old_data"
            }
            
            task_name = task_map.get(choice)
            if task_name:
                result = anvil.server.call(f'run_task_{task_name}')
                console.print(f"[green]✓ Task completed successfully[/green]")
                if result:
                    console.print(f"Result: {result}")
            
        except Exception as e:
            console.print(f"[red]✗ Task failed: {e}[/red]")
            logger.error(f"Task execution error: {e}")
    
    def view_logs(self):
        """View application logs."""
        console.print("\n[cyan]Recent Logs:[/cyan]")
        
        try:
            logs = anvil.server.call('get_recent_logs', limit=20)
            
            log_table = Table(box=box.SIMPLE)
            log_table.add_column("Time", style="dim")
            log_table.add_column("Level")
            log_table.add_column("Message")
            
            for log in logs:
                level_color = {
                    'ERROR': 'red',
                    'WARNING': 'yellow',
                    'INFO': 'green',
                    'DEBUG': 'dim'
                }.get(log.get('level', 'INFO'), 'white')
                
                log_table.add_row(
                    log.get('timestamp', ''),
                    f"[{level_color}]{log.get('level', '')}[/{level_color}]",
                    log.get('message', '')
                )
            
            console.print(log_table)
            
        except Exception as e:
            console.print(f"[red]Error fetching logs: {e}[/red]")
            logger.error(f"Log fetch error: {e}")
    
    def data_management(self):
        """Data management utilities."""
        console.print("\n[cyan]Data Management Options:[/cyan]")
        
        options = [
            "Export Data to CSV",
            "Import Data from CSV",
            "Backup Database",
            "Clear Cache",
            "Database Statistics",
            "Back to Main Menu"
        ]
        
        choice = questionary.select(
            "Select an option:",
            choices=options
        ).ask()
        
        if choice == "Back to Main Menu":
            return
        
        try:
            if choice == "Export Data to CSV":
                table_name = questionary.text("Enter table name to export:").ask()
                filename = f"{table_name}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                result = anvil.server.call('export_table_to_csv', table_name)
                with open(filename, 'w') as f:
                    f.write(result)
                console.print(f"[green]✓ Exported to {filename}[/green]")
                
            elif choice == "Database Statistics":
                stats = anvil.server.call('get_detailed_database_stats')
                console.print(Panel(json.dumps(stats, indent=2), title="Database Statistics"))
                
            else:
                console.print(f"[yellow]Feature '{choice}' coming soon![/yellow]")
                
        except Exception as e:
            console.print(f"[red]Operation failed: {e}[/red]")
            logger.error(f"Data management error: {e}")
    
    def send_test_notification(self):
        """Send a test notification to Discord."""
        if not self.discord_webhook:
            console.print("[yellow]Discord webhook not configured[/yellow]")
            return
        
        console.print("[cyan]Sending test notification...[/cyan]")
        
        try:
            payload = {
                "content": "Test notification from Market Hub Console",
                "embeds": [{
                    "title": "System Status",
                    "description": "This is a test notification",
                    "color": 5814783,
                    "fields": [
                        {"name": "Environment", "value": self.environment, "inline": True},
                        {"name": "Time", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "inline": True}
                    ],
                    "footer": {"text": "Market Hub Console"}
                }]
            }
            
            response = requests.post(self.discord_webhook, json=payload)
            
            if response.status_code == 204:
                console.print("[green]✓ Test notification sent successfully[/green]")
            else:
                console.print(f"[red]✗ Failed to send notification: {response.status_code}[/red]")
                
        except Exception as e:
            console.print(f"[red]Error sending notification: {e}[/red]")
            logger.error(f"Notification error: {e}")
    
    def main_menu(self):
        """Display and handle the main menu."""
        while True:
            console.print("\n" + "="*50)
            console.print("[bold cyan]Market Hub Console - Main Menu[/bold cyan]")
            console.print("="*50)
            
            choices = [
                "📊 View Dashboard",
                "🔍 Test Database Connection",
                "⚡ Run Scheduled Task",
                "📝 View Logs",
                "💾 Data Management",
                "🔔 Send Test Notification",
                "🔄 Refresh Statistics",
                "❌ Exit"
            ]
            
            choice = questionary.select(
                "Select an option:",
                choices=choices
            ).ask()
            
            if choice.startswith("📊"):
                self.display_dashboard()
            elif choice.startswith("🔍"):
                self.test_database_connection()
            elif choice.startswith("⚡"):
                self.run_scheduled_tasks()
            elif choice.startswith("📝"):
                self.view_logs()
            elif choice.startswith("💾"):
                self.data_management()
            elif choice.startswith("🔔"):
                self.send_test_notification()
            elif choice.startswith("🔄"):
                console.print("[yellow]Refreshing statistics...[/yellow]")
                self.display_dashboard()
            elif choice.startswith("❌"):
                console.print("[yellow]Exiting...[/yellow]")
                break
            
            if not choice.startswith("❌"):
                input("\nPress Enter to continue...")
    
    def run(self):
        """Main entry point for the console application."""
        console.print(Panel.fit(
            "[bold cyan]Market Hub Console[/bold cyan]\n"
            f"Environment: {self.environment}\n"
            "Initializing...",
            border_style="blue"
        ))
        
        try:
            with self.anvil_connection():
                # Display initial dashboard
                self.display_dashboard()
                
                # Start main menu loop
                self.main_menu()
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted by user[/yellow]")
        except Exception as e:
            console.print(f"\n[red]Fatal error: {e}[/red]")
            logger.exception("Fatal error in main loop")
            sys.exit(1)


def main():
    """Entry point for the application."""
    app = AnvilConsole()
    app.run()


if __name__ == "__main__":
    main()
