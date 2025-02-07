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


📥 Installation
# Clone the repository
git clone https://github.com/yourusername/linkup.git
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
