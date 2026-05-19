HakimLamb Website Code (Wix / Velo Implementation)

This folder contains the custom development assets used in the HakimLamb Wix website implementation.

────────────────────────────────────────
PROJECT STRUCTURE
────────────────────────────────────────

/frontend
- wix-frontend-logic.js
  Contains all frontend Velo logic including UI interactions, filtering, map communication, and user event handling.

/backend
- aiFunctions.web.js
  Contains backend Velo web modules including OpenRouter AI integration, API handling, and server-side logic.

/map
- leaflet-map-iframe.html
  Custom Leaflet-based interactive map used as an iframe inside the Wix site for rendering geolocation markers and visual data.

/README.txt
- Documentation for the project structure and usage notes.

────────────────────────────────────────
IMPORTANT NOTES
────────────────────────────────────────

- Wix does not support full export of website design, layout, or editor structure.
- This package includes only custom code and embedded implementations.
- UI/UX design, styling, and Wix page structure are not included.

────────────────────────────────────────
TECHNICAL OVERVIEW
────────────────────────────────────────

Frontend (Velo):
- Handles UI interactions, filtering logic, repeater updates, and communication with iframe map.

Backend (Velo Web Modules):
- Handles AI-based processing via OpenRouter API.
- Secure API key management using Wix Secrets Manager.

Map (Leaflet Iframe):
- Renders interactive geospatial visualization.
- Communicates with Wix frontend via postMessage API.

