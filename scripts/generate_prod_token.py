import argparse
import sys
import datetime as dt
import os
from pathlib import Path

# Add parent directory to sys.path so we can import from the app
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from identity import build_dev_claims, create_verification_token

def main():
    parser = argparse.ArgumentParser(description="Generate a production identity verification token.")
    parser.add_argument("--secret", required=True, help="The PLATFORM_IDENTITY_BRIDGE_SECRET set on Render")
    parser.add_argument("--provider", default="government_id", help="Identity provider (e.g., bankid, government_id)")
    parser.add_argument("--subject_id", required=True, help="A unique ID for the person (e.g., social security number)")
    parser.add_argument("--name", required=True, help="Legal name of the person")
    parser.add_argument("--country", default="SE", help="Country code (default: SE)")
    
    args = parser.parse_args()
    
    print("\n--- Generating Production Token ---")
    
    # 1. Build the claims (using the same logic as dev claims, but we will sign it with the PROD secret)
    claims = build_dev_claims(
        provider=args.provider,
        subject_id=args.subject_id,
        legal_name=args.name,
        country_code=args.country,
    )
    
    # 2. Sign the token using the PROD secret
    try:
        token = create_verification_token(claims, secret_key=args.secret)
        print("\n✅ Verification Token Generated Successfully!")
        print("-" * 50)
        print(token)
        print("-" * 50)
        print("\nTo test the UX on your physical Render deployment:")
        print("1. Open your live website (e.g., https://tp-platform-pilot.onrender.com)")
        print("2. Open Browser DevTools (F12) -> Network Tab to grab the exact API request body... OR just let it fail once, copy the payload, add this token to it.")
        print('Actually, to test the frontend easily without rewriting it: ')
        print('Open the browser console on your live site and run:')
        print(f"localStorage.setItem('temp_token', '{token}');")
        print("\nIf the UI doesn't have an input box for the token yet, it will fail. Let's fix that UX!")
    except Exception as e:
        print(f"Error generating token: {e}")

if __name__ == "__main__":
    main()
