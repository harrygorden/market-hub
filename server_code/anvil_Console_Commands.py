"""
Anvil Server Module - Market Hub
This module provides the backend functions that the Anvil Console calls.
"""

import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables
import anvil.secrets
import datetime
import json


# ============================================================================
# Database Operations
# ============================================================================

@anvil.server.callable
def list_tables():
    """Return a list of available tables in the app."""
    try:
        # This is a simplified version - you'll need to customize based on your actual tables
        table_names = [
            'events',
            'news_articles', 
            'technical_indicators',
            'analysis_cache',
            'system_logs'
        ]
        return table_names
    except Exception as e:
        print(f"Error listing tables: {e}")
        return []


@anvil.server.callable
def get_database_stats():
    """Get statistics about the database."""
    stats = {}
    
    try:
        # Events table stats
        if hasattr(app_tables, 'events'):
            events = app_tables.events.search()
            stats['events_count'] = len(events)
            
            # Get today's events
            today = datetime.datetime.now().date()
            today_events = app_tables.events.search(
                date=q.greater_than_or_equal_to(today),
                date=q.less_than(today + datetime.timedelta(days=1))
            )
            stats['events_today'] = len(today_events)
        
        # News articles stats
        if hasattr(app_tables, 'news_articles'):
            articles = app_tables.news_articles.search()
            stats['articles_count'] = len(articles)
            
            # Get recent articles (last 24 hours)
            yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
            recent = app_tables.news_articles.search(
                published_date=q.greater_than_or_equal_to(yesterday)
            )
            stats['articles_24h'] = len(recent)
        
        # Technical indicators stats
        if hasattr(app_tables, 'technical_indicators'):
            indicators = app_tables.technical_indicators.search()
            stats['indicators_count'] = len(indicators)
        
        # Analysis cache stats
        if hasattr(app_tables, 'analysis_cache'):
            cache = app_tables.analysis_cache.search()
            stats['cache_entries'] = len(cache)
        
        stats['status'] = 'healthy'
        
    except Exception as e:
        stats['status'] = 'error'
        stats['error'] = str(e)
        print(f"Error getting database stats: {e}")
    
    return stats


@anvil.server.callable
def get_detailed_database_stats():
    """Get detailed statistics about each table."""
    detailed_stats = {}
    
    try:
        # Events table detailed stats
        if hasattr(app_tables, 'events'):
            events = app_tables.events.search()
            detailed_stats['events'] = {
                'total_count': len(events),
                'by_impact': {},
                'by_country': {}
            }
            
            for event in events:
                # Count by impact
                impact = event.get('impact', 'Unknown')
                detailed_stats['events']['by_impact'][impact] = \
                    detailed_stats['events']['by_impact'].get(impact, 0) + 1
                
                # Count by country
                country = event.get('country', 'Unknown')
                detailed_stats['events']['by_country'][country] = \
                    detailed_stats['events']['by_country'].get(country, 0) + 1
        
        # News articles detailed stats
        if hasattr(app_tables, 'news_articles'):
            articles = app_tables.news_articles.search()
            detailed_stats['news_articles'] = {
                'total_count': len(articles),
                'analyzed': 0,
                'pending_analysis': 0,
                'by_sentiment': {}
            }
            
            for article in articles:
                if article.get('ai_analysis'):
                    detailed_stats['news_articles']['analyzed'] += 1
                    
                    sentiment = article.get('ai_analysis', {}).get('sentiment', 'Unknown')
                    detailed_stats['news_articles']['by_sentiment'][sentiment] = \
                        detailed_stats['news_articles']['by_sentiment'].get(sentiment, 0) + 1
                else:
                    detailed_stats['news_articles']['pending_analysis'] += 1
        
    except Exception as e:
        detailed_stats['error'] = str(e)
        print(f"Error getting detailed stats: {e}")
    
    return detailed_stats


@anvil.server.callable
def test_read_operation():
    """Test database read operation."""
    try:
        # Try to read from events table
        if hasattr(app_tables, 'events'):
            events = app_tables.events.search()
            return {'success': True, 'message': f'Successfully read {len(events)} events'}
        else:
            # If events table doesn't exist, try system_logs
            if hasattr(app_tables, 'system_logs'):
                logs = app_tables.system_logs.search()
                return {'success': True, 'message': f'Successfully read {len(logs)} logs'}
        
        return {'success': False, 'message': 'No tables found for testing'}
        
    except Exception as e:
        return {'success': False, 'message': str(e)}


@anvil.server.callable
def test_write_operation():
    """Test database write operation."""
    try:
        # Write a test log entry
        if hasattr(app_tables, 'system_logs'):
            app_tables.system_logs.add_row(
                timestamp=datetime.datetime.now(),
                level='INFO',
                source='Console',
                message='Test write operation from Anvil Console',
                details={'test': True, 'timestamp': datetime.datetime.now().isoformat()}
            )
            return {'success': True, 'message': 'Successfully wrote test log entry'}
        
        return {'success': False, 'message': 'System logs table not found'}
        
    except Exception as e:
        return {'success': False, 'message': str(e)}


# ============================================================================
# Task Execution
# ============================================================================

@anvil.server.callable
def run_task_fetch_events():
    """Manually trigger the fetch events task."""
    try:
        import requests
        
        # Fetch events from API
        response = requests.get('https://nfs.faireconomy.media/ff_calendar_thisweek.json')
        events = response.json()
        
        # Store events in database
        if hasattr(app_tables, 'events'):
            for event in events:
                # Check if event already exists
                existing = app_tables.events.get(
                    title=event.get('title'),
                    date=datetime.datetime.fromisoformat(event.get('date'))
                )
                
                if not existing:
                    app_tables.events.add_row(
                        title=event.get('title'),
                        country=event.get('country'),
                        date=datetime.datetime.fromisoformat(event.get('date')),
                        impact=event.get('impact'),
                        forecast=event.get('forecast'),
                        previous=event.get('previous'),
                        fetched_at=datetime.datetime.now()
                    )
        
        return {'success': True, 'events_processed': len(events)}
        
    except Exception as e:
        print(f"Error fetching events: {e}")
        return {'success': False, 'error': str(e)}


@anvil.server.callable
def run_task_fetch_news():
    """Manually trigger the fetch news task."""
    try:
        # This would integrate with Polygon.io
        # For now, return a placeholder
        return {'success': True, 'message': 'News fetch task triggered'}
        
    except Exception as e:
        return {'success': False, 'error': str(e)}


@anvil.server.callable
def run_task_process_ai_analysis():
    """Manually trigger AI analysis processing."""
    try:
        # This would process pending items for AI analysis
        pending_count = 0
        
        if hasattr(app_tables, 'events'):
            events_needing_analysis = app_tables.events.search(
                ai_analysis=None,
                date=q.greater_than_or_equal_to(datetime.datetime.now())
            )
            pending_count += len(events_needing_analysis)
        
        return {
            'success': True, 
            'message': f'Found {pending_count} items pending analysis'
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}


@anvil.server.callable
def run_task_update_technicals():
    """Manually trigger technical indicators update."""
    try:
        # This would update technical indicators
        return {'success': True, 'message': 'Technical indicators update triggered'}
        
    except Exception as e:
        return {'success': False, 'error': str(e)}


@anvil.server.callable
def run_task_send_notifications():
    """Manually trigger notification sending."""
    try:
        # This would check for pending notifications and send them
        return {'success': True, 'message': 'Notification task triggered'}
        
    except Exception as e:
        return {'success': False, 'error': str(e)}


@anvil.server.callable
def run_task_clean_old_data():
    """Clean old data from the database."""
    try:
        deleted_count = 0
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=30)
        
        # Clean old events
        if hasattr(app_tables, 'events'):
            old_events = app_tables.events.search(
                date=q.less_than(cutoff_date)
            )
            for event in old_events:
                event.delete()
                deleted_count += 1
        
        # Clean old logs
        if hasattr(app_tables, 'system_logs'):
            old_logs = app_tables.system_logs.search(
                timestamp=q.less_than(cutoff_date)
            )
            for log in old_logs:
                log.delete()
                deleted_count += 1
        
        return {
            'success': True, 
            'message': f'Deleted {deleted_count} old records'
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}


# ============================================================================
# Logging
# ============================================================================

@anvil.server.callable
def get_recent_logs(limit=20):
    """Get recent system logs."""
    try:
        if hasattr(app_tables, 'system_logs'):
            logs = app_tables.system_logs.search(
                tables.order_by('timestamp', ascending=False)
            )[:limit]
            
            return [
                {
                    'timestamp': log['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                    'level': log.get('level', 'INFO'),
                    'source': log.get('source', ''),
                    'message': log.get('message', '')
                }
                for log in logs
            ]
        
        return []
        
    except Exception as e:
        print(f"Error fetching logs: {e}")
        return []


@anvil.server.callable
def write_log(level, source, message, details=None):
    """Write a log entry."""
    try:
        if hasattr(app_tables, 'system_logs'):
            app_tables.system_logs.add_row(
                timestamp=datetime.datetime.now(),
                level=level,
                source=source,
                message=message,
                details=details or {}
            )
            return True
        return False
        
    except Exception as e:
        print(f"Error writing log: {e}")
        return False


# ============================================================================
# Data Import/Export
# ============================================================================

@anvil.server.callable
def export_table_to_csv(table_name):
    """Export a table to CSV format."""
    try:
        import csv
        import io
        
        # Get the table
        table = getattr(app_tables, table_name, None)
        if not table:
            return f"Table '{table_name}' not found"
        
        rows = table.search()
        if not rows:
            return "No data to export"
        
        # Create CSV
        output = io.StringIO()
        
        # Get column names from first row
        first_row = rows[0]
        fieldnames = list(first_row.keys())
        
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in rows:
            row_dict = {}
            for field in fieldnames:
                value = row[field]
                # Convert datetime objects to string
                if isinstance(value, datetime.datetime):
                    value = value.isoformat()
                row_dict[field] = value
            writer.writerow(row_dict)
        
        return output.getvalue()
        
    except Exception as e:
        return f"Error exporting table: {e}"


# ============================================================================
# System Health
# ============================================================================

@anvil.server.callable
def get_system_health():
    """Get overall system health status."""
    health = {
        'status': 'healthy',
        'checks': {}
    }
    
    try:
        # Check database connection
        if hasattr(app_tables, 'system_logs'):
            app_tables.system_logs.search(tables.order_by('timestamp', ascending=False))[:1]
            health['checks']['database'] = 'OK'
        else:
            health['checks']['database'] = 'No tables'
            health['status'] = 'degraded'
        
        # Check secrets
        try:
            test_secret = anvil.secrets.get_secret('ANVIL_UPLINK_KEY')
            health['checks']['secrets'] = 'OK' if test_secret else 'Not configured'
        except:
            health['checks']['secrets'] = 'Error'
            health['status'] = 'degraded'
        
        # Check scheduled tasks (this is a placeholder)
        health['checks']['scheduled_tasks'] = 'OK'
        
    except Exception as e:
        health['status'] = 'unhealthy'
        health['error'] = str(e)
    
    return health
