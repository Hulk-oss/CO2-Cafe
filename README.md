# CO2 Cafe ☕

![CO2 Cafe](images/Coffee-Shop.png)

Welcome to the **CO2 Cafe** repository! This project is a fully-featured, premium e-commerce and cafe website. It combines an elegantly crafted front-end design with a robust Python Flask back-end to handle user authentication, product cataloging, and cart management.

## 🌟 Features

- **Beautiful, Responsive UI**: Built with pure HTML, CSS, and Vanilla JavaScript for maximum performance and a premium feel.
- **Dark Mode Support**: Seamlessly toggles between light and dark themes based on user preference, with persistence.
- **User Authentication**: Secure JWT-based tokenization for user registration and login.
- **Persistent Shopping Cart**:
  - For guests: The cart is saved in the browser's `localStorage` so items never vanish when navigating across pages.
  - For logged-in users: Cart state is synced with the backend database for cross-session continuity.
- **Dynamic Content**: Interactions like reading journal entries, viewing menus, and simulating an e-commerce checkout flow.

## 🏗️ Architecture & Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript (ES6+).
- **Backend**: Python 3.x, Flask (`app.py`), PyJWT for Tokenization.
- **Database**: SQLite (managed via the built-in `sqlite3` module).

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need Python 3 installed on your machine.

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Hulk-oss/CO2-Cafe.git
   cd CO2-Cafe
   ```

2. **Install dependencies**
   It's recommended to use a virtual environment:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```
   *The SQLite database (`database.db`) will be automatically created on the first run.*

4. **Visit the Cafe**
   Open your browser and navigate to:
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 📡 API Endpoints

The Flask application exposes the following RESTful endpoints under `/api/`:

| Method | Endpoint | Description | Auth Required |
| --- | --- | --- | --- |
| `POST` | `/api/register` | Registers a new user account. | No |
| `POST` | `/api/login` | Authenticates a user and returns a JWT. | No |
| `GET` | `/api/cart` | Retrieves the authenticated user's cart. | Yes (JWT) |
| `POST` | `/api/cart` | Saves the user's cart to the database. | Yes (JWT) |
| `POST` | `/api/checkout` | Processes the checkout and clears the cart. | Yes (JWT) |

## 🛡️ Security

We take security seriously. Please refer to our [SECURITY.md](SECURITY.md) for information on our security policies, supported versions, and how to safely report vulnerabilities.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.

---
*Considered coffee. Generous hospitality. © 2026 CO2 Cafe*