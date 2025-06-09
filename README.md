# PostReach AI - Client Applications

This directory contains client applications and user interfaces for interacting with various PostReach AI services. Each client is designed to provide an intuitive, web-based interface for testing and using specific AI services.

## 📁 Directory Structure

```
clients/
├── common/                    # Shared utilities and components
│   ├── __init__.py
│   └── auth.py               # Authentication system for all clients
├── website_analyzer/         # Website Analyzer Streamlit client
│   ├── app.py               # Main application
│   ├── api_client.py        # API client
│   ├── ui_components.py     # UI components
│   ├── requirements.txt     # Dependencies
│   ├── README.md           # Client-specific documentation
│   └── ...
└── README.md               # This file
```

## 🚀 Available Clients

### 🔍 Website Analyzer Client
**Location:** `clients/website_analyzer/`  
**Framework:** Streamlit  
**Purpose:** Comprehensive website analysis and brand intelligence extraction

**Features:**
- 🎨 Logo extraction and color palette analysis
- 🗣️ Brand voice and communication style analysis
- 📊 Custom information extraction (contact info, pricing, etc.)
- 📚 Analysis history and result management
- 🔐 Secure authentication system

**Quick Start:**
```bash
cd clients/website_analyzer
pip install -r requirements.txt
python run.py
```

[📖 Full Documentation](./website_analyzer/README.md)

## 🔧 Common Components

### 🔐 Authentication System
**Location:** `clients/common/auth.py`

Shared authentication system used across all client applications:
- **Multi-environment support**: Works with both environment variables and Streamlit Cloud secrets
- **Secure password hashing**: HMAC-SHA256 password hashing
- **Session management**: Proper user session handling
- **Demo mode**: Pre-configured demo credentials for testing

**Usage:**
```python
from common.auth import StreamlitAuth

auth = StreamlitAuth()
if auth.require_auth():
    # User is authenticated, show the app
    pass
```

### 🎨 UI Patterns
Common UI patterns and design elements:
- Gradient headers and modern styling
- Consistent color schemes and layouts
- Responsive design for mobile and desktop
- Loading states and error handling
- History management and result caching

## 🌐 Deployment Options

### Local Development
Each client can be run locally for development and testing:

1. **Install Dependencies**
   ```bash
   cd clients/[client_name]
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp env_template.txt .env
   # Edit .env with your configuration
   ```

3. **Run Application**
   ```bash
   python run.py
   # or
   streamlit run app.py
   ```

### Streamlit Cloud Deployment
All Streamlit-based clients can be deployed to Streamlit Cloud:

1. **Connect Repository** to Streamlit Cloud
2. **Set App Path** to `clients/[client_name]/app.py`
3. **Configure Secrets** with required environment variables
4. **Deploy** and test the application

### Docker Deployment
For containerized deployments:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY clients/[client_name]/ .
COPY clients/common/ ../common/
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## 🔧 Development Guidelines

### Adding New Clients

1. **Create Client Directory**
   ```bash
   mkdir clients/new_client
   cd clients/new_client
   ```

2. **Essential Files**
   - `app.py` - Main application entry point
   - `requirements.txt` - Python dependencies
   - `README.md` - Client-specific documentation
   - `env_template.txt` - Environment configuration template

3. **Use Common Components**
   ```python
   # Import shared authentication
   from common.auth import StreamlitAuth
   
   # Follow consistent UI patterns
   # Use standardized error handling
   # Implement proper logging
   ```

4. **Configuration Management**
   - Support both environment variables and secrets
   - Provide clear configuration examples
   - Include validation and error messages

### Code Standards

- **Python Style**: Follow PEP 8 guidelines
- **Documentation**: Include comprehensive docstrings
- **Error Handling**: Implement graceful error handling with user-friendly messages
- **Security**: Never commit secrets or sensitive information
- **Testing**: Include unit tests for core functionality

### UI/UX Guidelines

- **Consistent Branding**: Use PostReach AI color scheme and styling
- **Responsive Design**: Ensure compatibility across devices
- **Accessibility**: Follow web accessibility best practices
- **User Feedback**: Provide clear status messages and loading indicators
- **Error States**: Show helpful error messages with troubleshooting tips

## 📝 Configuration

### Environment Variables
Common environment variables used across clients:

| Variable | Description | Example |
|----------|-------------|---------|
| `AUTH_SECRET_KEY` | Secret key for password hashing | `your-secret-key` |
| `VALID_USERS` | Comma-separated user credentials | `user:hash,admin:hash` |
| `API_BASE_URL` | Base URL for API services | `https://api.example.com` |
| `API_KEY` | API authentication key | `your-api-key` |

### Streamlit Cloud Secrets
For production deployment on Streamlit Cloud:

```toml
[secrets]
AUTH_SECRET_KEY = "your-secret-key"
API_BASE_URL = "https://your-api.amazonaws.com"
API_KEY = "your-api-key"

[secrets.VALID_USERS]
admin = "hashed_password"
user1 = "hashed_password"
```

## 🔒 Security Considerations

### Authentication
- All clients use the shared authentication system
- Passwords are hashed using HMAC-SHA256
- Sessions are managed securely
- Demo credentials are provided for testing

### API Security
- API keys are stored securely in environment variables or secrets
- All API requests include proper authentication headers
- Timeout and retry logic implemented for API calls

### Data Protection
- No sensitive data is logged or stored persistently
- User sessions are cleared on logout
- Analysis results are stored only in session state

## 🛠️ Troubleshooting

### Common Issues

1. **Authentication Problems**
   - Check `AUTH_SECRET_KEY` configuration
   - Verify password hashing
   - Ensure user credentials are correct

2. **API Connection Issues**
   - Verify API URL and credentials
   - Check network connectivity
   - Review API service status

3. **Deployment Issues**
   - Check Streamlit Cloud secrets configuration
   - Verify repository access and file paths
   - Review deployment logs for errors

### Debug Mode
Most clients include debug information:
- API connection status
- Configuration details
- Error logs and troubleshooting tips

## 📞 Support

For issues and questions:
1. Check client-specific README files
2. Review configuration and troubleshooting sections
3. Contact the development team

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch for your client
3. **Follow** development guidelines and code standards
4. **Test** thoroughly with different configurations
5. **Document** your client with comprehensive README
6. **Submit** a pull request

## 📄 License

This project is part of the PostReach AI platform. Please refer to the main project license for usage terms.

---

**Build beautiful, secure, and functional client applications! 🚀✨**
