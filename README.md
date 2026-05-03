# DecoraAI — Collaborative Interior Design Platform

## 📄 Project Overview

The Floor Plan Generator is a cloud-native, AI-powered web application that enables interior designers and clients to collaboratively design, visualize, and optimize room layouts. Users can create floor plans via an interactive drag-and-drop canvas, communicate in real-time via chat, and leverage AI assistance to generate improved designs based on the created layouts.

---

## 🎯 Key Features

*  **Drag-and-Drop Canvas:** Interactive design interface to create custom floor plans with pre-built catalog items.
*  **Real-Time Chat:** WebSocket-powered chat service for instant communication between designer and client.
*  **AI Design Assistant:** Machine learning-based recommendations to optimize floor plans.
*  **Secure Authentication:** OAuth2-based user authentication and role-based access control (RBAC).
*  **Microservices Architecture:** Fully containerized backend with independent scalable services.

---

## 🛠️ Technology Stack

### Frontend

* Next.js (React)
* TypeScript

### Backend (Microservices)

* Python FastAPI
* REST APIs (All microservices)

### Machine Learning

* TensorFlow / PyTorch
* Image-to-layout analysis for design suggestions

---

## 🧱 Project Structure

```
project-root/
│
├── client/            # Next.js frontend app
└── server/
    ├── auth-service/    # User management & OAuth2
    ├── chat-service/    # WebSocket chat server
    ├── canvas-service/  # Canvas image export & storage
    ├── ai-assistant/    # ML model inference API
    └── shared/          # Shared modules
```

---

## 🚩 Security

* OAuth2 authentication (Auth0/AWS Cognito)
* HTTPS with SSL certificates (AWS ACM)
* Database & storage encryption (at rest & in-transit)

---

## 📅 Roadmap (MVP Milestones)

✅ Set up GitHub repo  
✅ Complete basic drag-and-drop canvas interface  
✅ Implement secure OAuth2 authentication  
✅ Integrate ML model for AI Design Assistant

---

## 👥 Team Roles

| Member   | Responsibility                        |
| -------- |---------------------------------------|
| Frontend | Canvas interface, Next.js, Chat UI    |
| Backend  | Microservices, APIs                   |

| ML       | AI assistant model development        |

---

## 📄 License

This project is proprietary and intended for academic/professional use only.

---

## 📞 Contact

For any questions, discussions, or contributions, please contact the project maintainers directly.

---
