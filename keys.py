# account_sid = "ACec4816fe66931cbc4d9e2e6048c952e6"
# auth_token = "cd895145bb23514c06c66dc697a12a18"
# twilio_number = "+18314259788"

import os

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_NUMBER")