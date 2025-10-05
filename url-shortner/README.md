# URL Shortener - NeetCodeIO Style

A modern, scalable URL shortener service built with FastAPI, following NeetCodeIO's system design principles.

## Features

- 🚀 **Fast URL Shortening**: Generate short URLs instantly
- 🎯 **Custom Aliases**: Create memorable custom short codes
- 📊 **Analytics**: Track click counts and usage statistics
- 🔒 **Secure**: Built with security best practices
- 🎨 **Modern UI**: Beautiful, responsive web interface
- 📱 **Mobile Friendly**: Works perfectly on all devices

## System Design

This URL shortener follows NeetCodeIO's recommended architecture:

### Core Components

1. **Web Interface**: Modern, responsive frontend
2. **REST API**: FastAPI backend with automatic documentation
3. **Database**: SQLite for development (easily scalable to PostgreSQL/MySQL)
4. **URL Generation**: Secure random code generation with collision detection

### Key Features

- **URL Validation**: Ensures only valid URLs are shortened
- **Collision Handling**: Automatic retry for duplicate short codes
- **Click Tracking**: Analytics for monitoring link performance
- **Custom Aliases**: User-defined short codes
- **Health Monitoring**: Built-in health check endpoint

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd url-shortner
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

4. **Open your browser**:
   Navigate to `http://localhost:8000`

## API Endpoints

### Core Endpoints

- `GET /` - Main web interface
- `POST /api/shorten` - Create a short URL
- `GET /{short_code}` - Redirect to original URL
- `GET /api/stats/{short_code}` - Get URL statistics
- `GET /api/health` - Health check

### API Usage Examples

#### Shorten a URL
```bash
curl -X POST "http://localhost:8000/api/shorten" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com/very-long-url"}'
```

#### Shorten with Custom Alias
```bash
curl -X POST "http://localhost:8000/api/shorten" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com/very-long-url", "custom_alias": "my-link"}'
```

#### Get Statistics
```bash
curl "http://localhost:8000/api/stats/abc123"
```

## Database Schema

```sql
CREATE TABLE urls (
    id INTEGER PRIMARY KEY,
    short_code VARCHAR UNIQUE NOT NULL,
    original_url VARCHAR NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    click_count INTEGER DEFAULT 0
);
```

## Architecture Decisions

### Following NeetCodeIO Guidelines

1. **User Stories First**: Designed around core user needs
2. **Scalability**: Database design supports horizontal scaling
3. **Security**: Input validation and secure random generation
4. **Performance**: Optimized for fast response times
5. **Monitoring**: Built-in health checks and analytics

### Scalability Considerations

- **Database**: Easy migration to PostgreSQL/MySQL for production
- **Caching**: Redis can be added for frequently accessed URLs
- **Load Balancing**: Stateless design supports multiple instances
- **CDN**: Static assets can be served via CDN

## Development

### Project Structure

```
url-shortner/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── templates/           # HTML templates
│   └── index.html      # Main web interface
├── static/             # Static assets (CSS, JS)
└── README.md           # This file
```

### Adding Features

1. **Custom Domains**: Add domain validation and routing
2. **User Accounts**: Implement authentication and user management
3. **Bulk Operations**: Support for shortening multiple URLs
4. **QR Codes**: Generate QR codes for short URLs
5. **Expiration**: Add URL expiration dates

## Deployment

### Production Considerations

1. **Database**: Use PostgreSQL or MySQL
2. **Environment Variables**: Configure via `.env` file
3. **HTTPS**: Enable SSL/TLS certificates
4. **Monitoring**: Add logging and metrics
5. **Backup**: Implement database backup strategy

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Inspired by NeetCodeIO's system design tutorials
- Built with FastAPI and modern web technologies
- Follows industry best practices for URL shorteners
