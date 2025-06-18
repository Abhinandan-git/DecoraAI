# DecoraAI — Collaborative Interior Design Platform

## 📄 Project Overview

The Floor Plan Generator is a cloud-native, AI-powered web application that enables interior designers and clients to collaboratively design, visualize, and optimize room layouts. Users can create floor plans via an interactive drag-and-drop canvas, communicate in real-time via chat, and leverage AI assistance to generate improved designs based on the created layouts.

---

## 🎯 Key Features

* 🎨 **Drag-and-Drop Canvas:** Interactive design interface to create custom floor plans with pre-built catalog items.
* 💬 **Real-Time Chat:** WebSocket-powered chat service for instant communication between designer and client.
* 🖼 **Canvas Export:** Save the canvas design as an image for sharing or AI analysis.
* 🤖 **AI Design Assistant:** Machine learning-based recommendations to optimize floor plans.
* 🔒 **Secure Authentication:** OAuth2-based user authentication and role-based access control (RBAC).
* 🔄 **Microservices Architecture:** Fully containerized backend with independent scalable services.
* 🚀 **CI/CD Ready:** Fully automated build, test, and deployment pipelines using GitHub Actions and Jenkins.

---

## 🛠️ Technology Stack

### Frontend

* Next.js (React)
* Tailwind CSS (Styling)
* Konva.js (Canvas rendering)
* TypeScript

### Backend (Microservices)

* Python FastAPI
* WebSockets (Chat service)
* REST APIs (All microservices)
* PostgreSQL (AWS RDS)
* AWS S3 (Canvas image storage)
* OAuth2 (Auth0 / AWS Cognito)

### Machine Learning

* TensorFlow / PyTorch
* Image-to-layout analysis for design suggestions

### DevOps & Infrastructure

* Docker (Containerization)
* Kubernetes (AWS EKS - Orchestration)
* GitHub Actions & Jenkins (CI/CD Pipelines)
* Terraform (Infrastructure as Code)
* AWS CloudWatch / Prometheus (Monitoring)
* AWS Secrets Manager (Secrets Management)

---

## 🧱 Project Structure

```
project-root/
│
├── frontend/            # Next.js frontend app
├── backend/
│   ├── auth-service/    # User management & OAuth2
│   ├── chat-service/    # WebSocket chat server
│   ├── canvas-service/  # Canvas image export & storage
│   ├── ai-assistant/    # ML model inference API
│   └── shared/          # Shared modules
├── docker/              # Dockerfiles
├── k8s/                 # Kubernetes manifests
├── terraform/           # Infrastructure as Code configs
├── .github/             # GitHub Actions workflows
└── docs/                # Documentation & architecture diagrams
```

---

## ⚙️ Deployment Pipeline

1. **Code Commit (GitHub)**
2. **GitHub Actions:**
   * Code linting (ESLint, Pylint)
   * Unit Testing (Jest, Pytest)
   * Docker Image Build & Push (AWS ECR)
3. **Kubernetes (AWS EKS):**
   * Deployment to Staging → Production

---

## 🚩 Security

* OAuth2 authentication (Auth0/AWS Cognito)
* HTTPS with SSL certificates (AWS ACM)
* Role-based access control (RBAC)
* Secure WebSockets (Chat service)
* Database & storage encryption (at rest & in-transit)

---

## 📊 Monitoring & Observability

* AWS CloudWatch (logs & metrics)
* Prometheus + Grafana (metrics & dashboards - optional)
* ELK Stack / Loki (optional centralized logging)

---

## 📅 Roadmap (MVP Milestones)

⬜ Set up GitHub repo and CI/CD pipelines  
⬜ Complete basic drag-and-drop canvas interface  
⬜ Implement secure OAuth2 authentication  
⬜ Build WebSocket-based real-time chat service  
⬜ Develop Canvas Export and S3 integration  
⬜ Integrate ML model for AI Design Assistant  
⬜ Full deployment on AWS EKS

---

## 👥 Team Roles

| Member   | Responsibility                          |
| -------- | --------------------------------------- |
| Frontend | Canvas interface, Next.js, Chat UI      |
| Backend  | Microservices, APIs, WebSockets         |
| ML       | AI assistant model development          |
| DevOps   | Kubernetes, CI/CD, Security, Monitoring |

---

## 📄 License

This project is proprietary and intended for academic/professional use only.

---

## 📞 Contact

For any questions, discussions, or contributions, please contact the project maintainers directly.

---
