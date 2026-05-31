## Changes to make in code before deployment:

- frontend/App.jsx : \
At line 24, change backend's url to `localhost:8002` or if exposed to the internet, change to your backend's domain name in the form of "www.domain.xyz".

- frontend/vite.config.js : \
Add `localhost:5173` or your domain name in the form of "www.domain.xyz" in allowed hosts section.

- Create `.env` file in backend directory and add your Gemini API key in the form of:
```bash
GEMINI_API_KEY=<your_api_key>
```
- 