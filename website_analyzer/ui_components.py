"""
UI components for Website Analyzer Streamlit app.
Contains reusable components for displaying analysis results.
"""

import streamlit as st
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import re


def display_header():
    """Display the main application header."""
    st.set_page_config(
        page_title="Website Analyzer",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🔍 Website Analyzer")
    st.markdown("""
    <div style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h3 style='color: white; text-align: center; margin: 0;'>
            Comprehensive Website Analysis & Brand Intelligence
        </h3>
        <p style='color: white; text-align: center; margin: 0.5rem 0 0 0; opacity: 0.9;'>
            Extract logos, analyze brand voice, and gather comprehensive insights from any website
        </p>
    </div>
    """, unsafe_allow_html=True)


def display_url_input() -> tuple:
    """
    Display URL input form with advanced options.
    
    Returns:
        Tuple of (url, include_logo, include_colors, include_brand, additional_fields)
    """
    st.subheader("🌐 Website Analysis Configuration")
    
    with st.form("analysis_form", clear_on_submit=False):
        # URL input
        url = st.text_input(
            "Website URL",
            placeholder="https://example.com",
            help="Enter the complete URL including https:// or http://"
        )
        
        # Analysis options
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Analysis Options**")
            include_logo = st.checkbox("Extract Logo", value=True, help="Extract and process the website logo")
            include_colors = st.checkbox("Extract Colors", value=True, help="Extract color palette from logo")
            include_brand = st.checkbox("Extract Brand Info", value=True, help="Analyze brand voice and identity")
        
        with col2:
            st.markdown("**🎯 Additional Information**")
            additional_fields = st.multiselect(
                "Custom Extraction Fields",
                options=[
                    "contact information including email and phone",
                    "pricing information and subscription plans",
                    "key features and services offered",
                    "company leadership and team information",
                    "social media links and profiles",
                    "business hours and location information",
                    "recent news and announcements",
                    "product catalog and offerings",
                    "customer testimonials and reviews",
                    "technical specifications and documentation"
                ],
                help="Select additional information to extract from the website"
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            analyze_button = st.form_submit_button(
                "🚀 Analyze Website",
                use_container_width=True,
                type="primary"
            )
        
        if analyze_button:
            if not url:
                st.error("Please enter a website URL")
                return None, None, None, None, None
            
            # Basic URL validation
            if not re.match(r'^https?://', url):
                if not url.startswith('www.'):
                    url = f"https://{url}"
                else:
                    url = f"https://{url}"
            
            return url, include_logo, include_colors, include_brand, additional_fields
        
        return None, None, None, None, None


def display_analysis_status(status: str, processing_time: Optional[float] = None):
    """
    Display analysis status with appropriate styling.
    
    Args:
        status: Analysis status
        processing_time: Processing time in seconds
    """
    status_colors = {
        "processing": "🔄",
        "partial": "⏳",
        "success": "✅",
        "failed": "❌"
    }
    
    status_messages = {
        "processing": "Analysis in progress...",
        "partial": "Partial analysis completed",
        "success": "Analysis completed successfully",
        "failed": "Analysis failed"
    }
    
    icon = status_colors.get(status, "❓")
    message = status_messages.get(status, "Unknown status")
    
    if status == "success":
        st.success(f"{icon} {message}")
        if processing_time:
            st.info(f"⏱️ Processing time: {processing_time:.2f} seconds")
    elif status == "failed":
        st.error(f"{icon} {message}")
    elif status in ["processing", "partial"]:
        st.warning(f"{icon} {message}")
    else:
        st.info(f"{icon} {message}")


def display_company_info(company_name: Optional[str], company_info: Optional[str], 
                        brand_identity: Optional[str]):
    """
    Display company information section.
    
    Args:
        company_name: Company name
        company_info: Company description
        brand_identity: Brand identity description
    """
    if not any([company_name, company_info, brand_identity]):
        return
    
    st.subheader("🏢 Company Information")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if company_name:
            st.markdown(f"**Company Name:**")
            st.markdown(f'<div style="font-size: 1.2em; font-weight: bold; color: #1f77b4; padding: 0.5rem; background-color: #f0f2f6; border-radius: 5px;">{company_name}</div>', unsafe_allow_html=True)
    
    with col2:
        if company_info:
            st.markdown("**Company Description:**")
            st.markdown(f'<div style="padding: 0.5rem; background-color: #f9f9f9; border-left: 4px solid #1f77b4; border-radius: 0 5px 5px 0;">{company_info}</div>', unsafe_allow_html=True)
    
    if brand_identity:
        st.markdown("**Brand Identity:**")
        st.markdown(f'<div style="padding: 1rem; background-color: #f0f8ff; border: 1px solid #e1e8ed; border-radius: 8px; margin-top: 0.5rem;">{brand_identity}</div>', unsafe_allow_html=True)


def display_logo_section(logo_url: Optional[str], color_palette: Optional[List[Dict[str, Any]]]):
    """
    Display logo and color palette section.
    
    Args:
        logo_url: URL of the extracted logo
        color_palette: List of color information dictionaries
    """
    if not logo_url and not color_palette:
        return
    
    st.subheader("🎨 Visual Brand Assets")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if logo_url:
            st.markdown("**Company Logo:**")
            try:
                st.image(logo_url, width=200, caption="Extracted Logo")
            except Exception as e:
                st.error(f"Failed to load logo: {str(e)}")
                st.markdown(f"Logo URL: {logo_url}")
    
    with col2:
        if color_palette and len(color_palette) > 0:
            st.markdown("**Brand Color Palette:**")
            
            # Check if color_palette contains HTML strings instead of proper data
            if isinstance(color_palette, str):
                st.warning("⚠️ Color palette data appears to be in HTML format. Displaying raw data:")
                with st.expander("Raw Color Data", expanded=False):
                    st.code(color_palette, language="html")
                return
            
            # Validate that color_palette is a list of dictionaries with proper structure
            try:
                valid_colors = []
                for color in color_palette:
                    if isinstance(color, dict) and 'hex_code' in color:
                        valid_colors.append(color)
                    elif isinstance(color, str):
                        # Skip HTML strings that might be mixed in
                        continue
                
                if not valid_colors:
                    st.warning("⚠️ No valid color data found in the color palette.")
                    return
                
                # Create color swatches using Streamlit columns for better layout
                num_colors = len(valid_colors)
                cols = st.columns(min(num_colors, 6))  # Max 6 colors per row
                
                for i, color in enumerate(valid_colors):
                    hex_code = color.get('hex_code', '#000000')
                    rgb = color.get('rgb', [0, 0, 0])
                    
                    # Ensure RGB is properly formatted
                    if isinstance(rgb, (list, tuple)) and len(rgb) >= 3:
                        rgb_values = f"RGB({rgb[0]}, {rgb[1]}, {rgb[2]})"
                    else:
                        rgb_values = "RGB(?, ?, ?)"
                    
                    with cols[i % len(cols)]:
                        # Create individual color swatch with proper HTML
                        color_swatch_html = f"""
                        <div style='text-align: center; margin-bottom: 1rem;'>
                            <div style='width: 80px; height: 80px; background-color: {hex_code}; border: 2px solid #ddd; border-radius: 8px; margin: 0 auto 0.5rem auto;'></div>
                            <div style='font-size: 0.8em; font-weight: bold;'>{hex_code}</div>
                            <div style='font-size: 0.7em; color: #666;'>{rgb_values}</div>
                        </div>
                        """
                        st.markdown(color_swatch_html, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Failed to render color palette: {str(e)}")
                st.warning("⚠️ There was an issue with the color palette data format.")
                with st.expander("Debug Information", expanded=False):
                    st.write("Color palette data type:", type(color_palette))
                    st.write("Color palette content:", color_palette)


def display_brand_voice(brand_voice: Optional[Dict[str, Any]]):
    """
    Display brand voice analysis.
    
    Args:
        brand_voice: Brand voice information dictionary
    """
    if not brand_voice:
        return
    
    st.subheader("🗣️ Brand Voice Analysis")
    
    # Create tabs for different aspects
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Audience & Topics", "🎭 Tone & Style", "🌐 Language", "📊 Summary"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            target_audience = brand_voice.get('target_audience')
            if target_audience:
                st.markdown("**🎯 Target Audience:**")
                st.markdown(f'<div style="padding: 0.75rem; background-color: #e8f4fd; border-left: 4px solid #1f77b4; border-radius: 0 5px 5px 0;">{target_audience}</div>', unsafe_allow_html=True)
        
        with col2:
            topics = brand_voice.get('topics', [])
            if topics:
                st.markdown("**📝 Main Topics:**")
                for topic in topics:
                    st.markdown(f"• {topic}")
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            tones = brand_voice.get('tones', [])
            if tones:
                st.markdown("**🎭 Communication Tones:**")
                for tone in tones:
                    st.markdown(f'<span style="background-color: #f0f8ff; padding: 0.25rem 0.5rem; margin: 0.2rem; border-radius: 15px; display: inline-block; border: 1px solid #d1e7dd;">🎵 {tone}</span>', unsafe_allow_html=True)
        
        with col2:
            language_types = brand_voice.get('language_types', [])
            if language_types:
                st.markdown("**✍️ Language Style:**")
                for lang_type in language_types:
                    st.markdown(f'<span style="background-color: #fff3cd; padding: 0.25rem 0.5rem; margin: 0.2rem; border-radius: 15px; display: inline-block; border: 1px solid #ffeaa7;">📝 {lang_type}</span>', unsafe_allow_html=True)
    
    with tab3:
        language = brand_voice.get('language', 'Not specified')
        st.markdown(f"**🌐 Primary Language:** {language}")
        
        # Additional language analysis could go here
        st.markdown("**📊 Language Analysis:**")
        st.info("The brand voice analysis provides insights into how the company communicates with its audience, helping you understand their communication strategy and brand personality.")
    
    with tab4:
        # Create a summary card
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 10px; color: white; margin: 1rem 0;'>
            <h4 style='margin: 0 0 1rem 0; color: white;'>🎯 Brand Voice Summary</h4>
        """, unsafe_allow_html=True)
        
        if target_audience:
            st.markdown(f"**Target Audience:** {target_audience}")
        
        if tones:
            st.markdown(f"**Key Tones:** {', '.join(tones)}")
        
        if language_types:
            st.markdown(f"**Communication Style:** {', '.join(language_types)}")
        
        if topics:
            st.markdown(f"**Main Focus Areas:** {', '.join(topics[:3])}")
        
        st.markdown("</div>", unsafe_allow_html=True)


def display_additional_info(additional_info: Optional[Dict[str, Any]]):
    """
    Display additional extracted information.
    
    Args:
        additional_info: Dictionary of additional information
    """
    if not additional_info:
        return
    
    st.subheader("📋 Additional Information")
    
    # Create expandable sections for different types of information
    for key, value in additional_info.items():
        if value:  # Only show non-empty values
            with st.expander(f"📂 {key.replace('_', ' ').title()}", expanded=False):
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        if sub_value:
                            st.markdown(f"**{sub_key.replace('_', ' ').title()}:** {sub_value}")
                elif isinstance(value, list):
                    for item in value:
                        st.markdown(f"• {item}")
                else:
                    st.markdown(str(value))


def display_raw_content(website_content: Optional[str]):
    """
    Display raw website content in an expandable section.
    
    Args:
        website_content: Raw website content
    """
    if not website_content:
        return
    
    with st.expander("📄 Raw Website Content", expanded=False):
        st.markdown("**Extracted Content Preview:**")
        # Show first 1000 characters
        preview = website_content[:1000]
        if len(website_content) > 1000:
            preview += "\n\n... (truncated)"
        
        st.text_area(
            "Content",
            value=preview,
            height=200,
            disabled=True,
            help=f"Full content length: {len(website_content)} characters"
        )


def display_analysis_metadata(analysis_id: Optional[str], url: Optional[str], 
                            created_at: Optional[str], processing_time: Optional[float]):
    """
    Display analysis metadata.
    
    Args:
        analysis_id: Analysis ID
        url: Analyzed URL
        created_at: Creation timestamp
        processing_time: Processing time in seconds
    """
    with st.expander("🔍 Analysis Details", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            if analysis_id:
                st.markdown(f"**Analysis ID:** `{analysis_id}`")
            if url:
                st.markdown(f"**URL:** {url}")
        
        with col2:
            if created_at:
                try:
                    # Parse the datetime string
                    dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
                    st.markdown(f"**Created:** {formatted_time}")
                except:
                    st.markdown(f"**Created:** {created_at}")
            
            if processing_time:
                st.markdown(f"**Processing Time:** {processing_time:.2f} seconds")


def save_to_history(analysis_data: Dict[str, Any]):
    """
    Save analysis result to session history.
    
    Args:
        analysis_data: Analysis result data
    """
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    
    # Create history entry
    history_entry = {
        'timestamp': datetime.now().isoformat(),
        'url': analysis_data.get('url', 'Unknown'),
        'company_name': analysis_data.get('company_name', 'Unknown Company'),
        'status': analysis_data.get('status', 'unknown'),
        'analysis_id': analysis_data.get('analysis_id'),
        'data': analysis_data
    }
    
    # Add to beginning of list (most recent first)
    st.session_state.analysis_history.insert(0, history_entry)
    
    # Keep only last 50 entries
    st.session_state.analysis_history = st.session_state.analysis_history[:50]


def display_history_sidebar():
    """Display analysis history in the sidebar."""
    with st.sidebar:
        st.markdown("## 📚 Analysis History")
        
        if 'analysis_history' not in st.session_state or not st.session_state.analysis_history:
            st.info("No analysis history yet.")
            return
        
        # Clear history button
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.analysis_history = []
            st.rerun()
        
        st.markdown("---")
        
        # Display history entries
        for i, entry in enumerate(st.session_state.analysis_history):
            status_icon = {"success": "✅", "failed": "❌", "processing": "🔄", "partial": "⏳"}.get(entry['status'], "❓")
            
            with st.expander(f"{status_icon} {entry['company_name'][:20]}...", expanded=False):
                st.markdown(f"**URL:** {entry['url']}")
                st.markdown(f"**Status:** {entry['status']}")
                
                try:
                    dt = datetime.fromisoformat(entry['timestamp'])
                    formatted_time = dt.strftime("%m/%d %H:%M")
                    st.markdown(f"**Time:** {formatted_time}")
                except:
                    pass
                
                if st.button(f"📋 Load Results", key=f"load_{i}", use_container_width=True):
                    st.session_state.selected_history = entry['data']
                    st.rerun()


def display_error_message(error: str):
    """
    Display error message with helpful information.
    
    Args:
        error: Error message
    """
    st.error(f"❌ **Analysis Failed:** {error}")
    
    with st.expander("🛠️ Troubleshooting Tips", expanded=False):
        st.markdown("""
        **Common Issues:**
        - **URL Format:** Make sure the URL includes `https://` or `http://`
        - **Website Accessibility:** Ensure the website is publicly accessible
        - **API Connection:** Check if the API service is running and accessible
        - **Network Issues:** Verify your internet connection
        
        **What to try:**
        1. Double-check the URL format
        2. Try a different website
        3. Wait a moment and try again
        4. Contact support if the issue persists
        """)


def display_loading_placeholder():
    """Display a loading placeholder with progress information."""
    with st.container():
        st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🔍</div>
            <h3>Analyzing Website...</h3>
            <p>This may take a few moments while we extract and analyze the website content.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress information
        progress_steps = [
            "🌐 Extracting website content...",
            "🖼️ Finding and processing logo...",
            "🎨 Analyzing color palette...",
            "🗣️ Analyzing brand voice...",
            "📊 Generating comprehensive insights..."
        ]
        
        for step in progress_steps:
            st.markdown(f"• {step}")


def format_json_display(data: Dict[str, Any]) -> str:
    """
    Format dictionary data for JSON display.
    
    Args:
        data: Dictionary to format
        
    Returns:
        Formatted JSON string
    """
    try:
        return json.dumps(data, indent=2, default=str)
    except Exception:
        return str(data) 