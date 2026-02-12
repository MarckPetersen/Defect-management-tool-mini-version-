# 🐛 Defect Management Tool (Mini Version)

A lightweight web-based defect management tool for structured defect tracking during software testing. This tool provides a simple, user-friendly interface for managing software defects with comprehensive tracking capabilities.

## ✨ Features

### Core Functionality
- **Create Defects**: Add new defects with detailed information
- **Update Defects**: Edit existing defects to reflect current status
- **Assign Defects**: Assign defects to team members for ownership
- **Delete Defects**: Remove defects when no longer needed

### Defect Fields
Each defect includes the following fields:
- **Title**: Brief description of the defect
- **Description**: Detailed explanation of the issue
- **Severity**: Impact level (Critical, High, Medium, Low)
- **Priority**: Urgency level (P1-Urgent, P2-High, P3-Medium, P4-Low)
- **Status**: Current state in workflow (New, In Progress, Resolved, Closed)
- **Owner**: Person assigned to handle the defect
- **Timestamps**: Creation and last update dates

### Status Workflow
The tool supports a defined status workflow:
1. **New** → Initial state when defect is created
2. **In Progress** → Defect is being actively worked on
3. **Resolved** → Fix has been implemented
4. **Closed** → Defect has been verified and closed

### Filter & Search
- **Search**: Filter defects by title or description keywords
- **Status Filter**: View defects by status
- **Severity Filter**: View defects by severity level
- **Priority Filter**: View defects by priority level
- **Clear Filters**: Reset all filters to view all defects

## 🚀 Getting Started

### Prerequisites
- A modern web browser (Chrome, Firefox, Safari, Edge)
- No server or installation required!

### Usage

1. **Open the Application**
   - Simply open `index.html` in your web browser
   - Or serve it using any HTTP server

2. **Create a Defect**
   - Fill in all required fields in the form
   - Click "Create Defect" to save

3. **Manage Defects**
   - **Edit**: Click the "Edit" button on any defect card
   - **Delete**: Click the "Delete" button to remove a defect
   - **Update Status**: Edit a defect and change its status to reflect progress

4. **Filter Defects**
   - Use the search box to find defects by keywords
   - Use dropdown filters to narrow down by status, severity, or priority
   - Click "Clear Filters" to reset

## 💾 Data Storage

The application uses browser localStorage for data persistence:
- All defects are stored locally in your browser
- Data persists across browser sessions
- No backend server required
- Data is specific to each browser/device

## 🛠️ Technical Stack

- **HTML5**: Structure and content
- **CSS3**: Styling with modern design
- **JavaScript (ES6+)**: Application logic
- **localStorage**: Client-side data persistence

## 📝 Project Structure

```
.
├── index.html      # Main HTML structure
├── styles.css      # Styling and layout
├── app.js          # Application logic
└── README.md       # Documentation
```

## 🎨 Design Features

- Clean, modern interface with gradient background
- Responsive design for mobile and desktop
- Color-coded badges for status, severity, and priority
- Smooth transitions and hover effects
- Intuitive form layout with validation

## 🔒 Security

- Input sanitization to prevent XSS attacks
- Client-side only (no server-side vulnerabilities)
- No external dependencies or CDN requirements

## 📈 Use Cases

- Software testing teams tracking bugs
- QA teams managing defect lifecycles
- Small projects requiring simple defect tracking
- Learning and demonstration purposes
- Quick defect logging during testing sessions

## 🤝 Contributing

This is a mini version designed for simplicity. Feel free to fork and extend with:
- User authentication
- Export/import functionality
- Comments and attachments
- Email notifications
- Integration with issue trackers

## 📄 License

Free to use for any purpose.

## 👤 Author

MarckPetersen

---

**Note**: This is a lightweight, client-side only application designed for simplicity and ease of use. For enterprise-scale defect management, consider tools like Jira, Bugzilla, or similar platforms.