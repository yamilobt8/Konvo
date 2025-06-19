# Django Chat App: Feature Roadmap & Learning Concepts

---

## 🧱 1. Core Features

### 👥 User Authentication
- **Sign up / login / logout**
- **Password reset** (email-based)
- **User profile page** with:
  - List of subscribed channels
  - List of authored messages

### 🗂️ Channels
- View all available channels
- Create/edit/delete a channel  
  *(optional: admin or moderator role only)*
- View messages in a channel
- Subscribe/unsubscribe to a channel

### 💬 Messages
- Authenticated users can post messages in channels
- Message display (author, timestamp, content)
- *Optional:* Markdown or rich text support

### 📧 Email Notifications
- When a user posts a message, all subscribers of the channel receive an email containing:
  - Channel name
  - Author name
  - Message content
  - Link to view the message

---

## 🧠 2. Key Concepts You’ll Learn

| Area              | Concepts                                                                     |
|-------------------|------------------------------------------------------------------------------|
| **Django ORM**    | Relational modeling (channels ↔ messages ↔ subscriptions)                    |
| **Auth**          | Login system, session handling, user-specific views                          |
| **Email**         | Sending real email via SMTP, testing with console backend                    |
| **Forms**         | Creating + validating forms for posts, subscriptions                         |
| **Querysets**     | Filtering messages per channel, getting all subscribers                      |
| **Templates**     | Reusable templates with conditional logic                                    |
| **Background Jobs** (optional) | Use Celery for async email sending                      |
| **Permissions**   | Allow only authenticated users to post or subscribe                          |
| **UX**            | Dynamic updates with HTMX or JavaScript (optional)                           |

---

## 🛠 3. Suggested Workflow

### 🏁 Phase 1: Basic Structure
- Set up Django project and app
- Configure authentication (register, login, logout)
- Set up models for users, channels, and messages
- Build basic views/templates for:
  - Viewing channels
  - Viewing messages in a channel

### 🧱 Phase 2: Subscriptions
- Add ability for users to subscribe/unsubscribe to channels
- Update user profile to show subscriptions

### 📬 Phase 3: Notifications
- On message creation:
  - Get list of subscribers to the channel
  - Send them an email with message details

### 🚀 Phase 4: Enhancements
- Add search or filters for channels/messages
- Add markdown support or rich text editor
- Create a dashboard for users showing recent activity
- Use Celery + Redis to handle email sending asynchronously

### 🎯 Final Touches
- Add unit tests (especially for email logic and subscription rules)
- Use Django admin to manage content
- Deploy the app (Render, Railway, or Heroku)
- Add a clean UI (Tailwind CSS or Bootstrap)

---

## 📌 Stretch Features (for learning more)
- Real-time updates using Django Channels or WebSockets
- Comments/replies to messages
- “Digest” emails (daily summaries instead of instant notifications)
- Role-based permissions (e.g., channel moderators)