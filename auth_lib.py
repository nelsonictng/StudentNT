import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
from config import settings

def login():
    # 1. Initialize the OAuth session
    oauth = OAuth2Session(
        settings.AUTH0_CLIENT_ID, 
        settings.AUTH0_CLIENT_SECRET, 
        scope="openid profile email"
    )
    
    # 2. Generate the URL and state
    authorization_url, state = oauth.create_authorization_url(
        f"https://{settings.AUTH0_DOMAIN}/authorize", 
        redirect_uri=settings.AUTH0_CALLBACK_URL
    )
    
    # 3. Store state for security validation later
    st.session_state["oauth_state"] = state
    
    # 4. Use a native Streamlit link button (Previous reliable way)
    st.link_button("🚀 Click here to Login", authorization_url, use_container_width=True)

def handle_callback():
    # Fixed typo: changed st.st to st
    if "user" not in st.session_state and "code" in st.query_params:
        try:
            oauth = OAuth2Session(
                settings.AUTH0_CLIENT_ID, 
                settings.AUTH0_CLIENT_SECRET, 
                state=st.session_state.get("oauth_state")
            )
            token = oauth.fetch_token(
                f"https://{settings.AUTH0_DOMAIN}/oauth/token", 
                code=st.query_params["code"], 
                redirect_uri=settings.AUTH0_CALLBACK_URL
            )
            userinfo = oauth.get(f"https://{settings.AUTH0_DOMAIN}/userinfo").json()
            
            # Save user to session
            st.session_state["user"] = userinfo
            
            # Clear parameters to prevent double-processing on refresh
            st.query_params.clear()
            st.rerun() 
        except Exception as e:
            st.error(f"Login validation failed: {e}")

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    logout_url = (f"https://{settings.AUTH0_DOMAIN}/v2/logout?client_id={settings.AUTH0_CLIENT_ID}&returnTo={settings.AUTH0_CALLBACK_URL}")
    st.markdown(f'<meta http-equiv="refresh" content="0;url={logout_url}">', unsafe_allow_html=True)
    st.stop()