# Crop Disease Identifier

An AI-powered, offline tool for early detection and severity estimation of crop diseases to empower farmers in rural areas.

## 1. Problem Statement

### Problem Title
Agricultural Productivity Loss due to Delayed Disease Detection

### Problem Description
Crop diseases significantly reduce agricultural productivity and income for farmers. Early detection is critical to prevent large-scale crop damage. However, many farmers rely on manual inspection or delayed expert consultation, which may not be readily accessible in rural areas.

### Target Users
- Small-scale farmers in rural regions.
- Agricultural extension workers.
- Cultivators with limited or no internet connectivity.

### Existing Gaps
- Manual inspection is prone to error and slow.
- Expert consultation is often delayed or geographically inaccessible.
- Most existing AI diagnostic tools require a stable internet connection for cloud-based inference.

## 2. Problem Understanding & Approach

### Root Cause Analysis
Delayed diagnosis leads to the rapid spread of diseases, causing decreased yields and increased input costs due to late-stage treatments. Economic vulnerability rises as farmers rely on guesswork or wait for professional help that arrives too late.

### Solution Strategy
The strategy involves using on-device TensorFlow.js models to enable real-time, offline classification. By performing inference directly on the user's device, we eliminate the need for internet connectivity at the point of need.

## 3. Proposed Solution

### Solution Overview
A mobile-first web application designed for offline crop disease diagnosis and severity estimation.

### Core Idea
Bringing intelligent disease detection directly to the farmer's smartphone. By utilizing on-device machine learning, the system provides immediate feedback without sending data to a remote server.

### Key Features
- **Offline Inference**: Operates fully without internet connectivity once the model is cached.
- **Disease Classification**: Identifies specific crop diseases from leaf photographs.
- **Severity Estimation**: Estimates the extent of the disease to guide treatment urgency.
- **Treatment Recommendations**: Provides actionable agricultural advice based on the diagnosis.
- **Local Knowledge Base**: Stores a structured database of diseases and treatments locally.

## 4. System Architecture

### High-Level Flow
User → Frontend → Model → Response

### Architecture Description
The system follows a client-side architecture. The TensorFlow.js model and the agricultural knowledge base are served once and stored in the browser's cache (using Service Workers). All subsequent operations—image processing, model inference, and recommendation retrieval—happen locally on the device.

### Architecture Diagram
(Add system architecture diagram image here)

## 5. Database Design

### ER Diagram
(Add ER diagram image here)

### ER Diagram Description
The local database (IndexedDB) stores:
- **Diseases**: Name, symptoms, and causal agents.
- **Treatments**: Biological and chemical control measures.
- **Crops**: List of supported crop species.
- **Mapping**: Linking model output classes to specific disease and treatment records.

## 6. Dataset Selected

### Dataset Name
PlantVillage Dataset

### Source
Publicly available via Kaggle and research repositories.

### Data Type
RGB leaf images across various crop species and health conditions.

### Selection Reason
It is the gold standard for crop disease classification, containing over 54,000 labeled images across 14 species and 38 classes.

### Preprocessing Steps
- Image resizing to 224x224 pixels.
- Pixel normalization.
- Data augmentation (rotation, flipping, and brightness adjustments) to improve model robustness.

## 7. Model Selected

### Model Name
MobileNetV2 (TensorFlow.js)

### Selection Reasoning
Optimized for mobile and edge devices, providing a balance between low latency and high classification accuracy.

### Alternatives Considered
- **ResNet50**: Higher accuracy but too large for browser-based offline use.
- **SqueezeNet**: Smaller but with lower accuracy compared to MobileNetV2.

### Evaluation Metrics
- Classification Accuracy
- F1-Score
- On-device Inference Latency

## 8. Technology Stack

### Frontend
- React.js
- Vite
- Tailwind CSS

### Backend
- N/A (Fully Offline PWA)

### ML/AI
- TensorFlow.js
- MobileNetV2

### Database
- IndexedDB (via Dexie.js)
- LocalStorage

### Deployment
- GitHub Pages / Vercel

## 9. API Documentation & Testing

### API Endpoints List
The system operates locally; however, the internal classification service exposes the following:

- **Endpoint 1**: `classifyImage(imageData)` - Takes image data and returns predicted class and confidence.
- **Endpoint 2**: `getTreatment(diseaseId)` - Retrieves treatment protocol from local storage.
- **Endpoint 3**: `estimateSeverity(imageData)` - Calculates disease severity index.

### API Testing Screenshots
(Add Postman / Thunder Client screenshots here)

## 10. Module-wise Development & Deliverables

### Checkpoint 1: Research & Planning
- **Deliverables**: Problem definition, dataset selection, and technology stack finalization.

### Checkpoint 2: Backend Development
- **Deliverables**: Local database schema design and knowledge base population.

### Checkpoint 3: Frontend Development
- **Deliverables**: Responsive UI for image upload/capture and result display.

### Checkpoint 4: Model Training
- **Deliverables**: Trained MobileNetV2 model converted to TensorFlow.js format.

### Checkpoint 5: Model Integration
- **Deliverables**: Offline inference engine and PWA service worker implementation.

### Checkpoint 6: Deployment
- **Deliverables**: Live web application and GitHub repository.

## 11. End-to-End Workflow
1. User captures or uploads a leaf image.
2. The image is preprocessed in the browser.
3. The TensorFlow.js model performs local inference.
4. Results (Disease name, Severity) are displayed.
5. Actionable treatment recommendations are retrieved from the local database.

## 12. Demo & Video
- **Live Demo Link**: [Pending]
- **Demo Video Link**: [Pending]
- **GitHub Repository**: https://github.com/Advikkhandelwal/crop_disease_identifier.git

## 13. Hackathon Deliverables Summary
- Functional Offline PWA.
- Trained ML Model (TF.js).
- Agricultural Knowledge Base.
- Technical Documentation.

## 14. Team Roles & Responsibilities
| Member Name | Role | Responsibilities |
| :--- | :--- | :--- |
| Advik Khandelwal | Lead Developer | ML Model Training & Integration |
| [Member Name] | Frontend Developer | UI/UX Design & Frontend Logic |
| [Member Name] | Research Analyst | Dataset & Agricultural Knowledge Base |

## 15. Future Scope & Scalability

### Short-Term
- Support for more crop species.
- Multi-language support for regional farmers.

### Long-Term
- IoT integration for soil health monitoring.
- Community-based reporting for disease outbreaks.

## 16. Known Limitations
- Accuracy may vary under poor lighting conditions.
- Limited by the hardware capabilities of the user's smartphone.

## 17. Impact
- **Increased Productivity**: Early detection prevents yield loss.
- **Economic Stability**: Reduced costs for unnecessary chemical treatments.
- **Accessibility**: Democratizing AI for farmers without internet access.
