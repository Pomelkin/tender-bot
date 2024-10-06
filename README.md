# Automation of Supplementary Agreements Drafting
A solution for **automating the process of drafting supplementary agreements** with NLP, developed as part of the **TenderHack hackathon** in Perm, Russia. 

This system enables users to consult on legal matters, automatically generate documents, and edit them while ensuring compliance with Russian legal standards.

## Key Features
- **Legal Consultation**: The system analyzes contracts and legislation to provide recommendations on the possibility of drafting a supplementary agreement.
- **Request Validation**: Before document generation, the system checks whether the request complies with legal norms, ensuring legal accuracy.
- **Automated Agreement Generation**: The system generates the text of the supplementary agreement based on the user’s request.
- **Editing and Version Tracking**: Users can manually edit the generated document, tracking changes in a manner similar to Google Docs.
- **Text Rephrasing**: The built-in AI model helps adapt document text based on user requests while maintaining legal accuracy.

## Technologies
### Web Interface
- **React + TypeScript**: Provides flexibility and scalability for building complex interfaces. Strong typing simplifies code maintenance.
- **Modular FSD Structure**: Ensures scalability, isolates business logic from the interface, and reduces dependencies between modules.
- **Telegram Bot on Aiogram**: Acts as a frontend, enabling interaction with the system via chat.  

React Web application's code is available [here](https://github.com/Sh6abrA/TenderHackWeb).
### Backend
- **FastAPI**: Built on Domain-Driven Design (DDD) and the C4 model, ensuring scalability and separation of business logic from technical details.
- **RAG (Retrieval-Augmented Generation)**: Used for consultation services, integrating large language models (LLMs) and document search and ranking mechanisms.

### AI Models
- **Gemma2 27B**: Generates responses based on context and performs text rephrasing.
- **USER-BGE**: Indexes and searches through contract and legal data, enhancing the accuracy of responses.
- **Qwen2 7B**: Works with long contexts to extract the essence of user requests.

### Infrastructure
- **Distributed Architecture**: The system operates on three servers with optimized language models through vLLM, minimizing latency and ensuring smooth operation.
- **Data Storage**: Utilizes S3 storage and MongoDB for document storage and data tracking.
- **Docker**: Each component of the system is isolated to facilitate updates and ensure stable operation.
