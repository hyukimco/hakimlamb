# The HakimLamb Project

An interactive map to search publications in plant-based technology accross all sciences.

The HakimLamb Project is a non-profit project initially designed for the Wix platform using Velo language, JavaScript and Leaflet maps. It lists scientific publications on plant-based technologies and related fields, such as veganism, vegetarianism, cruelty-free, fungi-based, algi-based and bacteria-based technologies, serving as a tool to advance sustainable development.

It includes buttons to generate AI summaries of data, including a comparison of pros and cons, health policies and environmental policies based on filtered publications.

The tools provided by HakimLamb only provide and process data that is of open access, such as title, abstract, author name, affiliation and supplementary data. The tools provided by HakimLamb do not avail restricted content.



---
# Comments about the code

HakimLamb Website Code (Wix / Velo Implementation)

This folder contains the custom development assets used in the HakimLamb Wix website implementation.

PROJECT STRUCTURE
---

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


IMPORTANT NOTES
---

- Wix does not support full export of website design, layout, or editor structure.
- This package includes only custom code and embedded implementations.
- UI/UX design, styling, and Wix page structure are not included.

TECHNICAL OVERVIEW
---

Frontend (Velo):
- Handles UI interactions, filtering logic, repeater updates, and communication with iframe map.

Backend (Velo Web Modules):
- Handles AI-based processing via OpenRouter API.
- Secure API key management using Wix Secrets Manager.

Map (Leaflet Iframe):
- Renders interactive geospatial visualization.
- Communicates with Wix frontend via postMessage API.
