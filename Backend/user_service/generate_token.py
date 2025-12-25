#!/usr/bin/env python3
"""
Script to generate Google Drive OAuth token.json
Works with both web and installed app OAuth credentials
"""
import os
import sys
import json
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_PATH = 'client_secret.json'
TOKEN_PATH = 'token.json'

if __name__ == '__main__':
    if not os.path.exists(CREDENTIALS_PATH):
        print(f"Error: {CREDENTIALS_PATH} not found!")
        sys.exit(1)
    
    print("=" * 70)
    print("Google OAuth Setup Check")
    print("=" * 70)
    print("\nBefore proceeding, make sure:")
    print("1. Your email is added as a test user in Google Cloud Console")
    print("2. The OAuth consent screen is configured")
    print("\nIf you see 'access_denied' error, add your email here:")
    print("https://console.cloud.google.com/apis/credentials/consent?project=kharjam-482318")
    print("\nGo to 'Test users' section and click 'ADD USERS'")
    input("\nPress Enter to continue...")
    
    # Read credentials to determine type
    with open(CREDENTIALS_PATH, 'r') as f:
        creds_data = json.load(f)
    
    # Check if it's web or installed app
    is_web_app = 'web' in creds_data
    is_installed_app = 'installed' in creds_data
    
    # Initialize redirect_uri variable
    redirect_uri = None
    
    if is_web_app:
        # For web apps, we need to configure redirect URI
        # IMPORTANT: This is ONLY for token generation, NOT your API base URL!
        print("=" * 70)
        print("⚠️  OAuth Redirect URI Configuration")
        print("=" * 70)
        print("\nIMPORTANT: The redirect URI is NOT your API base URL!")
        print("It's ONLY used during token generation (one-time process).")
        print("After token.json is created, you won't need it anymore.\n")
        print("Your API base URL (http://95.216.121.248:800/) is separate")
        print("and has nothing to do with OAuth redirect URIs.\n")
        print("Choose redirect URI option:")
        print("1. localhost:8080 (recommended - simple, temporary local server)")
        print("2. Your server URL (if you want, but not necessary)")
        print("3. Switch to Desktop app (best - no redirect URI needed)")
        
        choice = input("\nEnter choice (1/2/3, default: 1): ").strip() or "1"
        
        if choice == "2":
            server_url = input("Enter your server URL (e.g., http://95.216.121.248:800): ").strip().rstrip('/')
            redirect_uri = f"{server_url}/oauth/callback"
            print(f"\nUsing: {redirect_uri}")
            print("⚠️  Note: This URL must be accessible and handle OAuth callback")
        elif choice == "3":
            print("\n" + "=" * 70)
            print("RECOMMENDED: Switch to Desktop App Type")
            print("=" * 70)
            print("This is the BEST option for Docker/server environments:")
            print("1. Go to: https://console.cloud.google.com/apis/credentials?project=kharjam-482318")
            print("2. Click 'CREATE CREDENTIALS' > 'OAuth client ID'")
            print("3. Application type: Desktop app")
            print("4. Name: 'Kharjam User Service Desktop'")
            print("5. Click 'CREATE'")
            print("6. Download the JSON file")
            print("7. Replace client_secret.json with the new file")
            print("8. Run this script again")
            print("\nDesktop apps don't need redirect URIs at all!")
            print("=" * 70)
            sys.exit(0)
        else:
            # Default to localhost (recommended)
            redirect_uri = 'http://localhost:8080/'
            print(f"\nUsing: {redirect_uri} (temporary local server for token generation)")
        
        # Create flow with web app credentials
        flow = Flow.from_client_config(
            creds_data,
            scopes=SCOPES,
            redirect_uri=redirect_uri
        )
        
        print("\n" + "=" * 70)
        print("Add Redirect URI to Google Cloud Console")
        print("=" * 70)
        print(f"\nAdd this redirect URI in Google Cloud Console:")
        print(f"\n  {redirect_uri}\n")
        print("Steps:")
        print("1. Go to: https://console.cloud.google.com/apis/credentials?project=kharjam-482318")
        print("2. Click on your OAuth 2.0 Client ID")
        print("3. Scroll to 'Authorized redirect URIs' section")
        print("4. Click 'ADD URI'")
        print(f"5. Add: {redirect_uri}")
        print("6. Click 'SAVE'")
        print("\nPress Enter after adding the redirect URI to continue...")
        input()
        
    elif is_installed_app:
        # For installed apps, use InstalledAppFlow
        from google_auth_oauthlib.flow import InstalledAppFlow
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
    else:
        print("Error: Unknown OAuth client type in client_secret.json")
        print("Expected 'web' or 'installed' application type.")
        sys.exit(1)
    
    try:
        # Try to use local server (works in local dev)
        if is_installed_app:
            creds = flow.run_local_server(port=0, open_browser=True)
        else:
            # For web apps, use local server with the configured redirect URI
            # IMPORTANT: Use the exact redirect_uri we set above
            print(f"\nStarting local server on {redirect_uri}...")
            # Extract port from redirect URI
            if redirect_uri.startswith('http://localhost:'):
                port = int(redirect_uri.split(':')[2].rstrip('/'))
            else:
                port = 8080
            creds = flow.run_local_server(port=port, open_browser=True)
    except Exception as e:
        # If browser can't be opened (Docker), use manual flow
        print(f"\nBrowser not available (likely Docker environment): {e}")
        print("=" * 70)
        print("Manual OAuth Flow:")
        print("=" * 70)
        
        if is_web_app:
            # For web apps, use the redirect URI we already configured
            # Make sure it matches exactly what's in Google Cloud Console
            print(f"\n⚠️  CRITICAL: Redirect URI must match EXACTLY")
            print(f"Using redirect URI: '{redirect_uri}'")
            print("\nIn Google Cloud Console, make sure you have EXACTLY:")
            print(f"  {redirect_uri}")
            print("\nCheck:")
            print("  ✓ Trailing slash: http://localhost:8080/ (with /)")
            print("  ✓ http:// not https://")
            print("  ✓ No extra spaces")
            print("  ✓ Port is 8080\n")
            
            # Verify the redirect URI matches
            verify = input(f"Is '{redirect_uri}' EXACTLY (character-by-character) in Google Cloud Console? (y/n): ").strip().lower()
            if verify != 'y':
                print("\n❌ Please add the EXACT redirect URI to Google Cloud Console:")
                print(f"   {redirect_uri}")
                print("\nThen run this script again.")
                sys.exit(1)
            
            # Ensure redirect URI is set correctly (re-set it to be sure)
            flow.redirect_uri = redirect_uri
            print(f"\n✓ Redirect URI set to: {flow.redirect_uri}")
        else:
            # For installed apps, use out-of-band
            flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
        
        # Get authorization URL
        auth_url, state = flow.authorization_url(prompt='consent')
        
        # Extract redirect_uri from the authorization URL to verify
        import urllib.parse
        parsed = urllib.parse.urlparse(auth_url)
        params = urllib.parse.parse_qs(parsed.query)
        redirect_uri_in_url = params.get('redirect_uri', [None])[0]
        
        print(f"\n1. Open this URL in your browser (on your local machine):")
        print(f"\n   {auth_url}\n")
        
        if redirect_uri_in_url:
            print(f"⚠️  VERIFY: The redirect_uri in the URL is:")
            print(f"   {urllib.parse.unquote(redirect_uri_in_url)}")
            print(f"\n   This MUST match EXACTLY what's in Google Cloud Console!")
            print(f"   Expected: {redirect_uri}\n")
            
            if urllib.parse.unquote(redirect_uri_in_url) != redirect_uri:
                print("❌ MISMATCH DETECTED!")
                print(f"   URL has: {urllib.parse.unquote(redirect_uri_in_url)}")
                print(f"   Expected: {redirect_uri}")
                print("\nThis will cause redirect_uri_mismatch error!")
                print("Please check your Google Cloud Console configuration.")
                sys.exit(1)
            else:
                print("✓ Redirect URI matches!")
        
        if flow.redirect_uri == 'urn:ietf:wg:oauth:2.0:oob':
            print("2. Sign in with your Google account and authorize the app")
            print("3. Google will show you a code on the page")
            print("4. Copy that code and paste it below\n")
        else:
            print("2. Sign in with your Google account and authorize the app")
            print("3. After authorization, you'll be redirected")
            print("4. Copy the 'code' parameter from the redirect URL\n")
        
        print("   (The code will look like: 4/0A...VERY_LONG_STRING...)\n")
        
        # Get authorization code from user
        code = input("Enter the authorization code: ").strip()
        
        if not code:
            print("Error: Authorization code is required!")
            sys.exit(1)
        
        # Exchange code for token
        try:
            flow.fetch_token(code=code)
            creds = flow.credentials
        except Exception as token_error:
            print(f"\nError exchanging code for token: {token_error}")
            print("\nPossible issues:")
            print("1. Redirect URI not registered in Google Cloud Console")
            print("2. Code expired (codes expire quickly)")
            print("3. Code copied incorrectly")
            sys.exit(1)
    
    # Save the credentials for the next run
    with open(TOKEN_PATH, 'w') as token:
        token.write(creds.to_json())
    
    print(f"\n✓ Success! Token saved to {TOKEN_PATH}")
    print("You can now use this file in your Docker container.")

