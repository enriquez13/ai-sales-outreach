# AI Sales Outreach Platform

[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://ai-sales-outreach-sandy.vercel.app)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow)
![Status](https://img.shields.io/badge/status-active-brightgreen)

> AI-powered sales outreach automation platform that generates personalized email campaigns using natural language processing and machine learning.

🔗 **[Live Demo](https://ai-sales-outreach-sandy.vercel.app)**

---

## 🎯 Overview

An intelligent sales automation tool that leverages AI to create personalized outreach messages at scale. The platform analyzes prospect data and generates contextually relevant email campaigns, improving response rates and reducing manual effort.

### Key Features

- 🤖 **AI-Powered Email Generation** - Uses NLP models to create personalized sales messages
- 📊 **Prospect Analysis** - Automatically extracts and analyzes relevant prospect information
- 🎨 **Responsive Web Interface** - Modern, user-friendly dashboard for campaign management
- ⚡ **Real-time Processing** - Fast email generation and preview
- 📈 **Campaign Tracking** - Monitor outreach performance and engagement

---

## 🛠️ Tech Stack

### Backend
- **Python** - Core backend logic
- **NLP/ML** - Text generation and personalization
- **RESTful API** - Endpoint architecture

### Frontend
- **JavaScript (ES6+)** - Interactive UI components
- **CSS3** - Responsive design
- **HTML5** - Semantic markup

### Deployment
- **Vercel** - Production hosting and CI/CD

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 14+ (for frontend development)
- npm or yarn

### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/enriquez13/ai-sales-outreach.git
   cd ai-sales-outreach
```

2. **Backend setup**
```bash
   cd backend
   pip install -r requirements.txt
   python app.py
```

3. **Frontend setup**
```bash
   cd frontend
   npm install
   npm start
```

4. **Access the application**
```
   Frontend: http://localhost:3000
   Backend API: http://localhost:5000
```

---

## 📁 Project Structure
```
ai-sales-outreach/
├── backend/           # Python backend API
│   ├── app.py        # Main application
│   └── ...           # AI models and utilities
├── frontend/         # JavaScript frontend
│   ├── index.html    # Main page
│   ├── styles/       # CSS styling
│   └── scripts/      # JS logic
└── README.md
```

---

## 💡 How It Works

1. **Input**: User provides prospect information (name, company, role, etc.)
2. **Analysis**: AI analyzes the data to understand context
3. **Generation**: NLP model creates personalized email content
4. **Review**: User can preview and edit generated messages
5. **Export**: Finalized emails ready for outreach campaigns

---

## 🎨 Screenshots
### App!
> <img alt="Image" width="1347" height="613" src="https://private-user-images.githubusercontent.com/45666593/546676103-da32d946-0a9f-4962-b87c-cb15c179cde2.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzA1MTA4OTksIm5iZiI6MTc3MDUxMDU5OSwicGF0aCI6Ii80NTY2NjU5My81NDY2NzYxMDMtZGEzMmQ5NDYtMGE5Zi00OTYyLWI4N2MtY2IxNWMxNzljZGUyLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjAyMDglMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwMjA4VDAwMjk1OVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTAwMWVjNGI1ZTVhOTVhMDYzMDEwNjBiNDMxZjhmY2ViOTkzNmNlN2YzZTg5NjVhNzQ1YWYxMGMwZjAyNjE4MzcmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.Kdy0fpDCC_AWsDNaCZthU_4ZrbYwf03s-j50Rd0KUmk">


### Email Generation Interface
> <img alt="Image" width="1103" height="523" src="https://private-user-images.githubusercontent.com/45666593/546676423-264b8ab8-50f2-43c1-8677-6832112e43d9.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzA1MTA2MDQsIm5iZiI6MTc3MDUxMDMwNCwicGF0aCI6Ii80NTY2NjU5My81NDY2NzY0MjMtMjY0YjhhYjgtNTBmMi00M2MxLTg2NzctNjgzMjExMmU0M2Q5LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjAyMDglMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwMjA4VDAwMjUwNFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTg4ZTA1MGNjOGE1MmMwODI2Y2M1MjhlMmYxNTY3MWMxNTEwNzVjNDUzZjY3ODQ2NGY1ZjE4OWI4MzRkOTUzNWYmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.B7JkbjNcLcY8Krw4Rg3CcSW6i4-MvlXc9IsaVPGY3gw">
 

---

## 🔮 Future Enhancements

- [ ] Integration with CRM platforms (HubSpot, Salesforce)
- [ ] A/B testing for email variants
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Email template library

---

## 📊 Performance

- **Generation Speed**: < 2 seconds per email
- **Personalization Quality**: AI-driven context analysis
- **Scalability**: Handles batch processing for large campaigns

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👤 Author

**Alejandro Enríquez**

- GitHub: [@enriquez13](https://github.com/enriquez13)
- LinkedIn: [alejandro-enriquez](https://www.linkedin.com/in/alejandro-enr%C3%ADquez-3611931b3/)
- Email: alejandroenriquez@usp.br

---

## 🌟 Acknowledgments

Built as part of exploring AI applications in sales automation and natural language generation.

---

**⭐ If you find this project useful, please consider giving it a star!**
