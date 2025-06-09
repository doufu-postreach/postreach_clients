"""
Main Streamlit application for Website Analyzer.
Provides a comprehensive UI for testing the website analyzer service.
"""

import streamlit as st
import sys
import os
from typing import Dict, Any

# Add the clients directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.auth import StreamlitAuth
from website_analyzer.api_client import WebsiteAnalyzerAPIClient, WebsiteAnalysisRequest
from website_analyzer.ui_components import (
    display_header, display_url_input, display_analysis_status,
    display_company_info, display_logo_section, display_brand_voice,
    display_additional_info, display_raw_content, display_analysis_metadata,
    save_to_history, display_history_sidebar, display_error_message,
    display_loading_placeholder
)


class WebsiteAnalyzerApp:
    """Main application class for the Website Analyzer Streamlit app."""
    
    def __init__(self):
        """Initialize the application."""
        self.auth = StreamlitAuth()
        self.api_client = None
        self.setup_page_config()
    
    def setup_page_config(self):
        """Setup Streamlit page configuration."""
        try:
            display_header()
        except Exception:
            # Fallback if page config was already set
            st.title("🔍 Website Analyzer")
    
    def initialize_api_client(self) -> bool:
        """
        Initialize the API client and check service availability.
        
        Returns:
            True if API client is ready, False otherwise
        """
        try:
            self.api_client = WebsiteAnalyzerAPIClient()
            return True
        except Exception as e:
            st.error(f"Failed to initialize API client: {str(e)}")
            return False
    
    def display_connection_status(self):
        """Display API connection status in the sidebar."""
        with st.sidebar:
            st.markdown("## 🔗 API Connection")
            
            if not self.api_client:
                st.error("❌ API client not initialized")
                return
            
            connection_info = self.api_client.get_connection_info()
            
            # Connection status
            if connection_info['service_available']:
                st.success("✅ Service Available")
            else:
                st.error("❌ Service Unavailable")
            
            # API details
            with st.expander("🔧 Connection Details", expanded=False):
                st.markdown(f"**Base URL:** `{connection_info['base_url']}`")
                st.markdown(f"**Has API Key:** {'✅' if connection_info['has_api_key'] else '❌'}")
                
                if not connection_info['service_available']:
                    st.markdown("""
                    **Troubleshooting:**
                    - Check if the API URL is correct
                    - Verify the service is running
                    - Ensure network connectivity
                    """)
    
    def display_configuration_help(self):
        """Display configuration help in the sidebar."""
        with st.sidebar:
            st.markdown("---")
            with st.expander("⚙️ Configuration", expanded=False):
                st.markdown("""
                **For Local Development:**
                Create a `.env` file with:
                ```
                WEBSITE_ANALYZER_API_URL=https://your-api-endpoint.amazonaws.com
                WEBSITE_ANALYZER_API_KEY=your-api-key
                AUTH_SECRET_KEY=your-secret-key
                VALID_USERS=demo:8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918
                ```
                
                **For Streamlit Cloud:**
                Add to your app's secrets:
                ```toml
                [secrets]
                WEBSITE_ANALYZER_API_URL = "https://your-api-endpoint.amazonaws.com"
                WEBSITE_ANALYZER_API_KEY = "your-api-key"
                AUTH_SECRET_KEY = "your-secret-key"
                
                [secrets.VALID_USERS]
                username = "hashed_password"
                ```
                """)
    
    def analyze_website(self, url: str, include_logo: bool, include_colors: bool, 
                       include_brand: bool, additional_fields: list) -> Dict[str, Any]:
        """
        Perform website analysis.
        
        Args:
            url: Website URL to analyze
            include_logo: Whether to extract logo
            include_colors: Whether to extract colors
            include_brand: Whether to extract brand info
            additional_fields: Additional fields to extract
            
        Returns:
            Analysis result dictionary
        """
        if not self.api_client:
            return {
                "status": "failed",
                "error": "API client not initialized"
            }
        
        # Create request
        request = WebsiteAnalysisRequest(
            url=url,
            include_logo=include_logo,
            include_colors=include_colors,
            include_brand=include_brand,
            additional_fields=additional_fields,
            session_id=f"streamlit-session-{self.auth.get_current_user()}"
        )
        
        # Make API call
        try:
            with st.spinner("🔍 Analyzing website... This may take a few minutes."):
                response = self.api_client.analyze_website(request)
                
                # Convert response to dictionary for easier handling
                result = {
                    "analysis_id": response.analysis_id,
                    "url": response.url,
                    "logo_url": response.logo_url,
                    "company_name": response.company_name,
                    "company_info": response.company_info,
                    "brand_identity": response.brand_identity,
                    "brand_voice": response.brand_voice,
                    "color_palette": response.color_palette,
                    "website_content": response.website_content,
                    "additional_info": response.additional_info,
                    "processing_time": response.processing_time,
                    "created_at": response.created_at,
                    "status": response.status,
                    "error": response.error
                }
                
                return result
                
        except Exception as e:
            return {
                "status": "failed",
                "error": f"Analysis failed: {str(e)}"
            }
    
    def display_analysis_results(self, result: Dict[str, Any]):
        """
        Display comprehensive analysis results.
        
        Args:
            result: Analysis result dictionary
        """
        # Display status
        display_analysis_status(result.get('status', 'unknown'), result.get('processing_time'))
        
        # If failed, show error and return
        if result.get('status') == 'failed':
            display_error_message(result.get('error', 'Unknown error'))
            return
        
        # Display results in organized sections
        st.markdown("---")
        
        # Company information
        display_company_info(
            result.get('company_name'),
            result.get('company_info'),
            result.get('brand_identity')
        )
        
        # Visual assets (logo and colors)
        display_logo_section(
            result.get('logo_url'),
            result.get('color_palette')
        )
        
        # Brand voice analysis
        display_brand_voice(result.get('brand_voice'))
        
        # Additional information
        display_additional_info(result.get('additional_info'))
        
        # Raw content and metadata
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            display_raw_content(result.get('website_content'))
        
        with col2:
            display_analysis_metadata(
                result.get('analysis_id'),
                result.get('url'),
                result.get('created_at'),
                result.get('processing_time')
            )
    
    def handle_history_selection(self):
        """Handle selection from analysis history."""
        if 'selected_history' in st.session_state:
            result = st.session_state.selected_history
            st.info("📚 Displaying results from history")
            self.display_analysis_results(result)
            
            # Clear selection after displaying
            if st.button("🔄 Start New Analysis", type="primary"):
                del st.session_state.selected_history
                st.rerun()
            
            return True
        return False
    
    def run(self):
        """Run the main application."""
        # Check authentication
        if not self.auth.require_auth():
            return
        
        # Show user info in sidebar
        self.auth.show_user_info()
        
        # Initialize API client
        if not self.initialize_api_client():
            st.error("Failed to initialize API client. Please check your configuration.")
            return
        
        # Display connection status and configuration help
        self.display_connection_status()
        self.display_configuration_help()
        
        # Display history sidebar
        display_history_sidebar()
        
        # Handle history selection
        if self.handle_history_selection():
            return
        
        # Main application interface
        st.markdown("---")
        
        # URL input and analysis configuration
        url_input_result = display_url_input()
        
        if url_input_result[0] is not None:  # If form was submitted
            url, include_logo, include_colors, include_brand, additional_fields = url_input_result
            
            # Display loading placeholder
            loading_container = st.container()
            with loading_container:
                display_loading_placeholder()
            
            # Perform analysis
            result = self.analyze_website(
                url, include_logo, include_colors, include_brand, additional_fields
            )
            
            # Clear loading placeholder
            loading_container.empty()
            
            # Save to history if successful
            if result.get('status') == 'success':
                save_to_history(result)
            
            # Display results
            self.display_analysis_results(result)
        
        else:
            # Show example/demo section when no analysis is running
            self.display_demo_section()
    
    def display_demo_section(self):
        """Display demo section with example results and usage information."""
        st.markdown("---")
        st.subheader("📖 How to Use")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **Step 1: Enter URL**
            - Enter any public website URL
            - Configure analysis options
            - Select additional fields if needed
            """)
        
        with col2:
            st.markdown("""
            **Step 2: Analysis**
            - Logo extraction & processing
            - Brand voice analysis
            - Color palette extraction
            - Custom information gathering
            """)
        
        with col3:
            st.markdown("""
            **Step 3: Results**
            - Comprehensive brand insights
            - Visual assets & colors
            - Organized information display
            - History for easy access
            """)
        
        # Example URLs section
        st.markdown("---")
        st.subheader("🌟 Try These Examples")
        
        example_urls = [
            "https://stripe.com",
            "https://openai.com",
            "https://microsoft.com",
            "https://apple.com",
            "https://google.com"
        ]
        
        cols = st.columns(len(example_urls))
        for i, url in enumerate(example_urls):
            with cols[i]:
                domain = url.replace("https://", "").replace("www.", "")
                if st.button(f"🔗 {domain}", key=f"example_{i}", use_container_width=True):
                    # Auto-fill the form with the example URL
                    st.session_state.example_url = url
                    st.rerun()
        
        # Features showcase
        st.markdown("---")
        st.subheader("✨ Features")
        
        feature_cols = st.columns(2)
        
        with feature_cols[0]:
            st.markdown("""
            **🎨 Visual Analysis**
            - Logo extraction and processing
            - Color palette generation
            - Brand asset identification
            
            **🗣️ Brand Intelligence**
            - Voice and tone analysis
            - Target audience identification
            - Communication style assessment
            """)
        
        with feature_cols[1]:
            st.markdown("""
            **📊 Comprehensive Insights**
            - Company information extraction
            - Custom field analysis
            - Structured data output
            
            **📚 History & Management**
            - Analysis history tracking
            - Easy result retrieval
            - Export capabilities
            """)


def main():
    """Main entry point for the application."""
    app = WebsiteAnalyzerApp()
    app.run()


if __name__ == "__main__":
    main() 