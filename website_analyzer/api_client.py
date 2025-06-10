"""
API client for Website Analyzer service.
Handles communication with the deployed AWS service.
"""

import os
import requests
import streamlit as st
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class WebsiteAnalysisRequest:
    """Request model for website analysis."""
    url: str
    session_id: Optional[str] = None
    track_id: Optional[str] = None
    include_logo: bool = True
    include_colors: bool = True
    include_brand: bool = True
    additional_fields: Optional[List[str]] = None


@dataclass
class WebsiteAnalysisResponse:
    """Response model for website analysis."""
    analysis_id: Optional[str] = None
    url: Optional[str] = None
    logo_url: Optional[str] = None
    company_name: Optional[str] = None
    company_info: Optional[str] = None
    brand_identity: Optional[str] = None
    brand_voice: Optional[Dict[str, Any]] = None
    color_palette: Optional[List[Dict[str, Any]]] = None
    website_content: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None
    processing_time: Optional[float] = None
    created_at: Optional[str] = None
    status: str = "processing"
    error: Optional[str] = None


class WebsiteAnalyzerAPIClient:
    """
    API client for the Website Analyzer service.
    
    Handles authentication, request formatting, and response parsing
    for the deployed AWS service.
    """
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL of the API service
            api_key: API key for authentication (if required)
        """
        self.base_url = self._get_base_url(base_url)
        self.api_key = self._get_api_key(api_key)
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "WebsiteAnalyzer-StreamlitClient/1.0"
        })
        
        # Add API key if available
        if self.api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}"
            })
    
    def _get_base_url(self, base_url: Optional[str]) -> str:
        """
        Get the base URL from parameter, Streamlit secrets, or environment.
        
        Args:
            base_url: Explicitly provided base URL
            
        Returns:
            Base URL for the API service
        """
        if base_url:
            return base_url.rstrip('/')
        
        # Try Streamlit secrets first
        try:
            return st.secrets["WEBSITE_ANALYZER_API_URL"].rstrip('/')
        except (KeyError, FileNotFoundError):
            pass
        
        # Fallback to environment variable
        env_url = os.getenv("WEBSITE_ANALYZER_API_URL", "")
        if env_url:
            return env_url.rstrip('/')
        
        # Default placeholder (will show error in UI)
        return "https://your-api-endpoint.amazonaws.com"
    
    def _get_api_key(self, api_key: Optional[str]) -> Optional[str]:
        """
        Get the API key from parameter, Streamlit secrets, or environment.
        
        Args:
            api_key: Explicitly provided API key
            
        Returns:
            API key for authentication
        """
        if api_key:
            return api_key
        
        # Try Streamlit secrets first
        try:
            return st.secrets["WEBSITE_ANALYZER_API_KEY"]
        except (KeyError, FileNotFoundError):
            pass
        
        # Fallback to environment variable
        return os.getenv("WEBSITE_ANALYZER_API_KEY")
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters
            
        Returns:
            Response data as dictionary
            
        Raises:
            requests.RequestException: If the request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=300  # 5 minutes timeout for long-running analysis
            )
            
            # Check if the response is successful
            if response.status_code == 200:
                return response.json()
            else:
                error_msg = f"API request failed with status {response.status_code}"
                try:
                    error_detail = response.json().get("detail", response.text)
                    error_msg += f": {error_detail}"
                except:
                    error_msg += f": {response.text}"
                
                return {
                    "status": "failed",
                    "error": error_msg
                }
        
        except requests.exceptions.Timeout:
            return {
                "status": "failed",
                "error": "Request timed out. The analysis might still be processing."
            }
        except requests.exceptions.ConnectionError:
            return {
                "status": "failed",
                "error": f"Failed to connect to API at {self.base_url}. Please check the URL."
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "failed",
                "error": f"Request failed: {str(e)}"
            }
        except Exception as e:
            return {
                "status": "failed",
                "error": f"Unexpected error: {str(e)}"
            }
    
    def analyze_website(self, request: WebsiteAnalysisRequest) -> WebsiteAnalysisResponse:
        """
        Analyze a website.
        
        Args:
            request: Website analysis request
            
        Returns:
            Website analysis response
        """
        # Convert request to dictionary
        request_data = {
            "url": request.url,
            "include_logo": request.include_logo,
            "include_colors": request.include_colors,
            "include_brand": request.include_brand,
        }
        
        # Add optional fields
        if request.session_id:
            request_data["session_id"] = request.session_id
        if request.track_id:
            request_data["track_id"] = request.track_id
        if request.additional_fields:
            request_data["additional_fields"] = request.additional_fields
        
        # Make the API request
        response_data = self._make_request(
            method="POST",
            endpoint="/api/v1/website-analyser/analyze",
            data=request_data
        )
        
        # Convert response to WebsiteAnalysisResponse
        return WebsiteAnalysisResponse(
            analysis_id=response_data.get("analysis_id"),
            url=response_data.get("url"),
            logo_url=response_data.get("logo_url"),
            company_name=response_data.get("company_name"),
            company_info=response_data.get("company_info"),
            brand_identity=response_data.get("brand_identity"),
            brand_voice=response_data.get("brand_voice"),
            color_palette=response_data.get("color_palette"),
            website_content=response_data.get("website_content"),
            additional_info=response_data.get("additional_info"),
            processing_time=response_data.get("processing_time"),
            created_at=response_data.get("created_at"),
            status=response_data.get("status", "failed"),
            error=response_data.get("error")
        )
    
    def get_website_analysis(self, analysis_id: str) -> WebsiteAnalysisResponse:
        """
        Get a specific website analysis by ID.
        
        Args:
            analysis_id: Analysis ID
            
        Returns:
            Website analysis response
        """
        response_data = self._make_request(
            method="GET",
            endpoint="/api/v1/website-analyser/get",
            params={"analysis_id": analysis_id}
        )
        
        return WebsiteAnalysisResponse(
            analysis_id=response_data.get("analysis_id"),
            url=response_data.get("url"),
            logo_url=response_data.get("logo_url"),
            company_name=response_data.get("company_name"),
            company_info=response_data.get("company_info"),
            brand_identity=response_data.get("brand_identity"),
            brand_voice=response_data.get("brand_voice"),
            color_palette=response_data.get("color_palette"),
            website_content=response_data.get("website_content"),
            additional_info=response_data.get("additional_info"),
            processing_time=response_data.get("processing_time"),
            created_at=response_data.get("created_at"),
            status=response_data.get("status", "failed"),
            error=response_data.get("error")
        )
    
    def list_website_analyses(self, page: int = 0, limit: int = 100, 
                            url_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        List website analyses.
        
        Args:
            page: Page number
            limit: Results per page
            url_filter: URL filter pattern
            
        Returns:
            List response with analyses and metadata
        """
        params = {
            "page": page,
            "limit": limit
        }
        
        if url_filter:
            params["url_filter"] = url_filter
        
        return self._make_request(
            method="GET",
            endpoint="/api/v1/website-analyser/list",
            params=params
        )
    
    def is_service_available(self) -> bool:
        """
        Check if the API service is available.
        
        Returns:
            True if service is available, False otherwise
        """
        try:
            # Try to make a simple request to check availability
            response = self.session.get(f"{self.base_url}/api/v1/ping", timeout=10)
            return response.status_code == 200
        except:
            # If health endpoint doesn't exist, try the list endpoint with minimal params
            try:
                response_data = self._make_request(
                    method="GET",
                    endpoint="/api/v1/website-analyser/list",
                    params={"page": 0, "limit": 1}
                )
                return "error" not in response_data or "connection" not in response_data.get("error", "").lower()
            except:
                return False
    
    def get_connection_info(self) -> Dict[str, Any]:
        """
        Get connection information for debugging.
        
        Returns:
            Dictionary with connection details
        """
        return {
            "base_url": self.base_url,
            "has_api_key": bool(self.api_key),
            "service_available": self.is_service_available()
        } 