curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Give me tips to manage stress."
          }
        ]
      }
    ]
  }' \
  "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=AIzaSyD6kC8AsgMAq1kk9-tyBSLt53J0_ai1Rzg"
