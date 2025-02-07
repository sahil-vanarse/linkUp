TokneX - Peer-to-Peer Learning Platform 🌟
TokneX is a real-time peer-to-peer learning platform that enables collaborative learning through topic-based rooms. Users can create, join, and participate in discussions with instant messaging capabilities.

✨ Features
💬 Real-time Communication
✔ WebSocket-powered instant messaging
✔ Live participant tracking
✔ Message read receipts

🎓 Learning Rooms
✔ Topic-based organization
✔ Multi-participant support
✔ Resource sharing capabilities

👥 User Management
✔ Custom user profiles
✔ Authentication system

⚡ Performance
✔ InMemory caching for fast responses
✔ Optimized PostgreSQL queries
✔ WebSocket connection pooling for scalability

🛠️ Tech Stack
🔹 Backend: Django 4.2
🔹 Database: PostgreSQL
🔹 Caching: InMemory
🔹 Real-time: Django Channels
🔹 Frontend: JavaScript, HTML5, CSS3
🔹 Deployment: Render


Images :


![erd_diagram](https://github.com/user-attachments/assets/2a0671c3-624a-4957-964c-7012c5b72bea)

![e2f1457680a94863ab968aea6da3d68a](https://github.com/user-attachments/assets/62eeb9f5-b06e-4394-95dd-6b4d6953087d)

![d7a9c5fb0de14bbf991bf7a247f89adf](https://github.com/user-attachments/assets/35e155d8-6c66-4604-ae1c-96662addfac6)

![e1196630085d46989f20deaedeaca561](https://github.com/user-attachments/assets/5fd95561-f317-4c8f-85c4-7a922b8d418e)

![cb4b33bd511c411e9b01ece020f7e469](https://github.com/user-attachments/assets/5bb45d18-32c2-4e65-a8fd-9c57af212a85)

![616bcff3a49c4af0a91440e61c1a4018](https://github.com/user-attachments/assets/dcdcf071-096c-4b5e-9f3b-4ed3a37f5d61)

![5b69dd5b34be49529f21b01e1894aa04](https://github.com/user-attachments/assets/66262416-e1de-4a8e-ad7e-d353d391ed37)

![c1d413df128041f7b6617d52f31550b7](https://github.com/user-attachments/assets/fb4ee2f5-fa0f-4131-ba4b-46ec8a2c78aa)

![b4fdc7b1809445c1b84350a1fa0f8e36](https://github.com/user-attachments/assets/66df5abe-b9bb-45f2-9305-d58cee684c5b)

![81fa1b8c707d4246ac4786137b59914f](https://github.com/user-attachments/assets/84bdba20-344f-44a4-b711-26761c321c88)

![ae3c82f31c5642e0bac86939baaca29e](https://github.com/user-attachments/assets/bfc051d9-a44b-4d2f-9d8a-badee31c7a57)

![043d9ba3b55b4abc83e33e4923402efe](https://github.com/user-attachments/assets/cadb47d3-3c3b-4d67-9cc9-7f7d207c35b4)

![3c70754bb2c942fdb9b6e7c27403e0a1](https://github.com/user-attachments/assets/34096950-e57f-46e2-8e3b-ddc550eb83bf)



📥 Installation![Uploading e1196630085d46989f20deaedeaca561.jpg…]()

# Clone the repository
git clone https://github.com/sahil-vanarse/linkup.git
cd linkup

# Create virtual environment
python -m venv env
source env/Scripts/activate  # Windows
source env/bin/activate      # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your configurations

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver


🛠️ Testing
# Run tests
python manage.py test

# Run with coverage
coverage run manage.py test
coverage report


📬 Contact
👤 Sahil Vanarse
🚀 Project Live Link: [TokneX on Render](https://toknex.onrender.com/)
🔗 GitHub Repository: [TokneX Repo
](https://github.com/sahil-vanarse/linkUp/)
