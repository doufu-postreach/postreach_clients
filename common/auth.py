"""
Authentication system for Streamlit applications.
Can be used across different service UIs within the clients module.
"""

import os
import streamlit as st
import hashlib
import hmac
from typing import Optional


class StreamlitAuth:
    """
    Authentication system for Streamlit applications.
    
    Supports both environment variables (for local development) and 
    Streamlit Cloud secrets (for production deployment).
    """
    
    def __init__(self, secret_key_name: str = "AUTH_SECRET_KEY"):
        """
        Initialize the authentication system.
        
        Args:
            secret_key_name: Name of the secret key in environment/secrets
        """
        self.secret_key_name = secret_key_name
        self.secret_key = self._get_secret_key()
        
    def _get_secret_key(self) -> Optional[str]:
        """
        Get the secret key from environment variables or Streamlit secrets.
        
        Returns:
            Secret key string or None if not found
        """
        # Try to get from Streamlit secrets first (for cloud deployment)
        try:
            return st.secrets[self.secret_key_name]
        except (KeyError, FileNotFoundError):
            pass
        
        # Fallback to environment variables (for local development)
        return os.getenv(self.secret_key_name)
    
    def _hash_password(self, password: str) -> str:
        """
        Hash a password using HMAC-SHA256.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        if not self.secret_key:
            raise ValueError("Secret key not found. Please set AUTH_SECRET_KEY in environment or Streamlit secrets.")
        
        return hmac.new(
            self.secret_key.encode(),
            password.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password
            hashed_password: Hashed password to verify against
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            return hmac.compare_digest(
                self._hash_password(password),
                hashed_password
            )
        except ValueError:
            return False
    
    def get_valid_users(self) -> dict:
        """
        Get valid users from environment or secrets.
        Expected format: {"username": "hashed_password", ...}
        
        Returns:
            Dictionary of valid users
        """
        # Try to get from Streamlit secrets first
        try:
            users = st.secrets.get("VALID_USERS", {})
            if users:
                return users
        except (KeyError, FileNotFoundError):
            pass
        
        # Fallback to environment variables
        # Expected format: USERNAME1:HASHED_PASSWORD1,USERNAME2:HASHED_PASSWORD2
        users_env = os.getenv("VALID_USERS", "")
        if not users_env:
            # Default demo user (password: "demo123")
            return {
                "demo": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
            }
        
        users = {}
        for user_entry in users_env.split(","):
            if ":" in user_entry:
                username, hashed_password = user_entry.split(":", 1)
                users[username.strip()] = hashed_password.strip()
        
        return users
    
    def is_authenticated(self) -> bool:
        """
        Check if the current user is authenticated.
        
        Returns:
            True if authenticated, False otherwise
        """
        return st.session_state.get("authenticated", False)
    
    def get_current_user(self) -> Optional[str]:
        """
        Get the current authenticated user.
        
        Returns:
            Username if authenticated, None otherwise
        """
        if self.is_authenticated():
            return st.session_state.get("username")
        return None
    
    def login(self, username: str, password: str) -> bool:
        """
        Attempt to log in a user.
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            True if login successful, False otherwise
        """
        valid_users = self.get_valid_users()
        
        if username in valid_users:
            if self._verify_password(password, valid_users[username]):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                return True
        
        return False
    
    def logout(self):
        """Log out the current user."""
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.rerun()
    
    def require_auth(self) -> bool:
        """
        Require authentication for the current page.
        Shows login form if not authenticated.
        
        Returns:
            True if authenticated, False if showing login form
        """
        if self.is_authenticated():
            return True
        
        self.show_login_form()
        return False
    
    def show_login_form(self):
        """Display the login form."""
        st.title("🔐 Authentication Required")
        st.markdown("Please log in to access the Website Analyzer.")
        
        with st.form("login_form"):
            st.subheader("Login")
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                submit_button = st.form_submit_button("Login", use_container_width=True)
            
            if submit_button:
                if not username or not password:
                    st.error("Please enter both username and password.")
                elif self.login(username, password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
        
        # Demo credentials info
        st.markdown("---")
        st.info("**Demo Credentials:** username: `demo`, password: `demo123`")
        st.markdown("""
        <div style='background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;'>
        <h4>🚀 For Production Deployment:</h4>
        <p>Set your authentication credentials in Streamlit Cloud secrets:</p>
        <pre>
[secrets]
AUTH_SECRET_KEY = "your-secret-key-here"

[secrets.VALID_USERS]
username1 = "hashed_password1"
username2 = "hashed_password2"
        </pre>
        <p><strong>Note:</strong> Passwords should be pre-hashed using HMAC-SHA256.</p>
        </div>
        """, unsafe_allow_html=True)
    
    def show_user_info(self):
        """Show current user info in sidebar."""
        if self.is_authenticated():
            with st.sidebar:
                st.markdown("---")
                st.markdown(f"👤 **Logged in as:** {self.get_current_user()}")
                if st.button("Logout", use_container_width=True):
                    self.logout()


def hash_password(password: str, secret_key: str) -> str:
    """
    Utility function to hash a password for storage.
    
    Args:
        password: Plain text password
        secret_key: Secret key for hashing
        
    Returns:
        Hashed password
    """
    return hmac.new(
        secret_key.encode(),
        password.encode(),
        hashlib.sha256
    ).hexdigest()


if __name__ == "__main__":
    # Utility script to generate hashed passwords
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python auth.py <password> <secret_key>")
        sys.exit(1)
    
    password = sys.argv[1]
    secret_key = sys.argv[2]
    
    hashed = hash_password(password, secret_key)
    print(f"Hashed password: {hashed}") 