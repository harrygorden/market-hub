# Market Hub - Project Overview

## Project Vision
Market Hub is a comprehensive trading information platform built on Anvil.works that serves as a centralized dashboard for all market-related information needed for day-to-day trading decisions. The application aggregates, analyzes, and presents market data, news, events, and technical indicators with AI-powered insights to support informed trading strategies.

## Core Architecture

### Platform & Infrastructure
- **Hosting Platform**: Anvil.works cloud environment
- **Security**: Anvil Secrets for API keys and sensitive data management
- **Automation**: Anvil Scheduled Tasks for background processing and data updates
- **Connectivity**: Anvil Uplink for local development and testing
- **AI Integration**: LangChain framework for sophisticated AI communication patterns
- **Notifications**: Discord webhook integration for real-time alerts
- **Documentation**: Context7 MCP for code lookup and API documentation

## Key Features & Pages

### 1. Home Page
**Purpose**: Provide a comprehensive market overview and top-level analysis
- **Components**:
  - Market indices summary (S&P 500, NASDAQ, DOW, etc.)
  - Key metrics dashboard
  - Market sentiment indicators
  - Quick insights panel with AI-generated market summary
  - Recent alerts and notifications

### 2. Events Page
**Purpose**: Track and analyze market-moving economic events
- **Data Source**: https://nfs.faireconomy.media/ff_calendar_thisweek.json
- **Update Frequency**: Hourly data retrieval
- **AI Analysis**:
  - Morning-of analysis for each event
  - Impact assessment (High/Medium/Low)
  - Historical context and expected market reaction
  - Real-time updates posted to the page
- **Features**:
  - Event filtering by impact level
  - Country/currency filtering
  - Calendar view with upcoming events
  - Historical event performance tracking

### 3. News Page
**Purpose**: Aggregate and analyze market-relevant news with AI-powered insights
- **Data Source**: Polygon.io News API
- **Processing Pipeline**:
  1. Retrieve articles via API
  2. AI classification for market relevance
  3. Market-relevant articles sent for deeper analysis
  4. Generate AI insights including:
     - Article summarization
     - Sentiment scoring (bullish/bearish/neutral)
     - Confidence rating
     - Market impact explanation
     - Author's intended market message
- **Features**:
  - Real-time news feed
  - Filtered views by relevance and sentiment
  - Historical news archive
  - Trending topics identification

### 4. Technicals Page
**Purpose**: Provide technical analysis and charting capabilities
- **Phase 1 Implementation**:
  - Integration with existing Google Sheets data
  - Webhook-based data updates
  - AI analysis of technical indicators
  - Pattern recognition and alerts
- **Phase 2 Implementation**:
  - Polygon.io WebSocket integration
  - Real-time streaming quotes
  - Live technical indicator calculations
  - Advanced charting capabilities
- **Features**:
  - Multiple timeframe analysis
  - Custom indicator configurations
  - AI-powered pattern detection
  - Technical alert system

## Integration Points

### External APIs
1. **Polygon.io**
   - News API for market news
   - WebSocket for real-time quotes (future)
   - Historical data endpoints

2. **Economic Calendar API**
   - Endpoint: https://nfs.faireconomy.media/ff_calendar_thisweek.json
   - Provides economic event data

3. **OpenAI API**
   - Text analysis and summarization
   - Sentiment analysis
   - Market impact assessment

### Internal Systems
1. **Google Sheets Integration**
   - Webhook receivers for data updates
   - Technical indicator calculations
   - Data storage and history

2. **Discord Integration**
   - Webhook notifications for:
     - High-impact events
     - Significant news
     - Technical alerts
     - System status updates

## AI Strategy

### LangChain Implementation
- **Custom Chains**: Tailored processing pipelines for different data types
- **Memory Management**: Context retention for related analyses
- **Prompt Engineering**: Optimized prompts for financial analysis
- **Model Selection**: Strategic use of different models based on task complexity

### AI Use Cases
1. **Event Analysis**: Contextual understanding of economic events
2. **News Processing**: Relevance filtering and summarization
3. **Technical Analysis**: Pattern recognition and signal generation
4. **Market Synthesis**: Combining multiple data sources for insights

## Development Tools

### Anvil Uplink Utility
A continuously evolving tool that provides:
- Connection testing to Anvil instance
- Statistics reporting
- Database operations
- Scheduled task management
- API endpoint testing
- Performance monitoring
- Debug utilities

## Security & Compliance
- All API keys stored in Anvil Secrets
- Secure webhook endpoints
- Rate limiting implementation
- Error handling and logging
- Data retention policies

## Scalability Considerations
- Modular architecture for feature additions
- Efficient data caching strategies
- Background task optimization
- WebSocket connection management (future)
- Database query optimization

## Success Metrics
- Data retrieval reliability (>99% uptime)
- AI analysis accuracy
- Notification delivery speed (<1 second)
- User interface responsiveness
- System resource utilization

## Future Enhancements
- Portfolio tracking integration
- Custom watchlists
- Backtesting capabilities
- Social sentiment analysis
- Options flow analysis
- Multi-asset class support
- Mobile application
- Advanced charting library
- Machine learning model training on historical data

## Development Philosophy
- **Iterative Development**: Start with core features, continuously enhance
- **Data-Driven Decisions**: Use metrics to guide feature development
- **User-Centric Design**: Focus on actionable insights
- **Reliability First**: Ensure core functions work flawlessly before adding complexity
- **AI-Augmented**: Use AI to enhance, not replace, human decision-making
