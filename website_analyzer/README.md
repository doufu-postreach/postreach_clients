# Website Analyzer - Streamlit Client

A comprehensive Streamlit application for testing and interacting with the Website Analyzer service. This client provides a beautiful, user-friendly interface for analyzing websites and extracting brand intelligence.

## 🌟 Features

### 🔍 Comprehensive Website Analysis
- **Logo Extraction**: Automatically finds and processes website logos
- **Color Palette Analysis**: Extracts dominant colors from logos and branding
- **Brand Voice Analysis**: Analyzes communication style, tone, and target audience
- **Custom Information Extraction**: Extract specific information like contact details, pricing, features, etc.

### 🎨 Beautiful UI Components
- **Modern Design**: Clean, professional interface with gradient backgrounds
- **Organized Results**: Structured display of analysis results in tabs and sections
- **Color Visualization**: Interactive color swatches showing hex codes and RGB values
- **Responsive Layout**: Works well on different screen sizes

### 🔐 Secure Authentication
- **Multi-Environment Support**: Works with both local environment variables and Streamlit Cloud secrets
- **Password Hashing**: Secure HMAC-SHA256 password hashing
- **Session Management**: Proper user session handling
- **Demo Mode**: Pre-configured demo credentials for testing

### 📚 History Management
- **Analysis History**: Automatically saves analysis results in session
- **Easy Retrieval**: Quick access to previous analyses from sidebar
- **History Persistence**: Results persist throughout the session
- **Clear History**: Option to clear history when needed

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Access to deployed Website Analyzer API service

### Local Development Setup

1. **Clone and Navigate**
   ```bash
   cd clients/website_analyzer
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp env_template.txt .env
   # Edit .env with your actual configuration
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

5. **Access the App**
   - Open your browser to `http://localhost:8501`
   - Login with demo credentials: `demo` / `demo123`

### Streamlit Cloud Deployment

1. **Fork/Upload** your repository to GitHub

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select the `clients/website_analyzer/app.py` file

3. **Configure Secrets**
   Add the following to your Streamlit Cloud app secrets:
   ```toml
   [secrets]
   WEBSITE_ANALYZER_API_URL = "https://your-api-endpoint.amazonaws.com"
   WEBSITE_ANALYZER_API_KEY = "your-api-key"
   AUTH_SECRET_KEY = "your-secret-key"
   
   [secrets.VALID_USERS]
   admin = "hashed_password_here"
   user1 = "another_hashed_password"
   ```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `WEBSITE_ANALYZER_API_URL` | Base URL of the API service | Yes | `https://api.example.com` |
| `WEBSITE_ANALYZER_API_KEY` | API key for authentication | No | `your-api-key` |
| `AUTH_SECRET_KEY` | Secret key for password hashing | Yes | `your-secret-key` |
| `VALID_USERS` | Comma-separated user:hash pairs | No | `user:hash,user2:hash2` |

### Creating User Passwords

To create hashed passwords for users:

1. **Using the CLI utility**:
   ```bash
   python clients/common/auth.py "your-password" "your-secret-key"
   ```

2. **Using Python**:
   ```python
   from clients.common.auth import hash_password
   hashed = hash_password("your-password", "your-secret-key")
   print(hashed)
   ```

## 🖥️ User Interface Guide

### Main Interface

1. **Header Section**
   - Beautiful gradient header with app title and description
   - Clear branding and purpose statement

2. **URL Input Form**
   - Website URL input with validation
   - Analysis options checkboxes (logo, colors, brand info)
   - Custom extraction fields multiselect
   - Submit button to start analysis

3. **Results Display**
   - Status indicators with appropriate colors
   - Company information section
   - Visual brand assets (logo and colors)
   - Brand voice analysis with tabs
   - Additional extracted information
   - Raw content and metadata in expandable sections

### Sidebar Features

1. **User Authentication**
   - Current user display
   - Logout button

2. **API Connection Status**
   - Service availability indicator
   - Connection details and troubleshooting

3. **Analysis History**
   - List of previous analyses
   - Quick load buttons for each result
   - Clear history option

4. **Configuration Help**
   - Environment setup instructions
   - Streamlit Cloud deployment guide

## 🎯 Usage Examples

### Basic Analysis
1. Enter a website URL (e.g., `https://stripe.com`)
2. Keep default options selected
3. Click "🚀 Analyze Website"
4. View comprehensive results

### Custom Analysis
1. Enter website URL
2. Select specific analysis options
3. Choose additional fields like:
   - Contact information
   - Pricing details
   - Company leadership
   - Technical specifications
4. Submit and review detailed results

### Using History
1. Previous analyses appear in sidebar
2. Click "📋 Load Results" to view past analysis
3. Use "🔄 Start New Analysis" to return to input form

## 🛠️ Development

### Project Structure
```
clients/website_analyzer/
├── app.py                 # Main Streamlit application
├── api_client.py          # API client for service communication
├── ui_components.py       # Reusable UI components
├── requirements.txt       # Python dependencies
├── env_template.txt       # Environment configuration template
└── README.md             # This file

clients/common/
├── __init__.py
└── auth.py               # Shared authentication system
```

### Adding New Features

1. **UI Components**: Add new functions to `ui_components.py`
2. **API Methods**: Extend `WebsiteAnalyzerAPIClient` in `api_client.py`
3. **Authentication**: Modify `StreamlitAuth` in `common/auth.py`
4. **Main App**: Update `WebsiteAnalyzerApp` in `app.py`

### Testing

1. **Local Testing**
   ```bash
   streamlit run app.py
   ```

2. **API Testing**
   - Use demo mode with placeholder API
   - Test with real API endpoint
   - Verify error handling

3. **Authentication Testing**
   - Test login/logout functionality
   - Verify password hashing
   - Test multi-user scenarios

## 🔧 Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Check API URL configuration
   - Verify service is running
   - Test network connectivity

2. **Authentication Problems**
   - Verify secret key configuration
   - Check password hashing
   - Ensure user credentials are correct

3. **Streamlit Cloud Issues**
   - Check secrets configuration
   - Verify repository access
   - Review deployment logs

### Debug Mode

Enable debug information by checking connection details in the sidebar:
- API URL and status
- Authentication status
- Service availability

## 📝 API Integration

The client integrates with the Website Analyzer API service with the following endpoints:

- `POST /api/v1/website-analyser/analyze` - Analyze website
- `GET /api/v1/website-analyser/get` - Get analysis by ID
- `GET /api/v1/website-analyser/list` - List analyses

### Request/Response Format

**Analysis Request:**
```json
{
  "url": "https://example.com",
  "include_logo": true,
  "include_colors": true,
  "include_brand": true,
  "additional_fields": ["contact information", "pricing"]
}
```

**Analysis Response:**
```json
{
  "analysis_id": "uuid",
  "url": "https://example.com",
  "logo_url": "https://storage.url/logo.png",
  "company_name": "Example Inc.",
  "company_info": "Description...",
  "brand_voice": {...},
  "color_palette": [...],
  "status": "success"
}
```

## 🚀 Deployment

### Streamlit Cloud Deployment

1. **Prepare Repository**
   - Ensure all files are committed
   - Add secrets configuration
   - Test locally first

2. **Deploy**
   - Connect to Streamlit Cloud
   - Select main branch
   - Set app path to `clients/website_analyzer/app.py`

3. **Configure Secrets**
   - Add all required environment variables
   - Test authentication
   - Verify API connectivity

### Custom Deployment

For custom deployments (Docker, server, etc.):

1. **Dockerfile Example**:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY clients/website_analyzer/ .
   COPY clients/common/ ../common/
   RUN pip install -r requirements.txt
   EXPOSE 8501
   CMD ["streamlit", "run", "app.py"]
   ```

2. **Environment Setup**:
   - Set all required environment variables
   - Ensure proper network access to API
   - Configure authentication

## 📄 License

This project is part of the PostReach AI platform. Please refer to the main project license for usage terms.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review configuration settings
3. Contact the development team

---

**Happy Analyzing! 🔍✨** 