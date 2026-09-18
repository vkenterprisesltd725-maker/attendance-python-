# Privacy and Security Guidelines

## Data Storage
- All student records are stored locally in an `SQLite` database (`student_data.db`).
- There is no unnecessary external data transfer, meaning no data leaves the machine unless explicitly exported.

## Authentication
- Passwords are securely hashed using `PBKDF2 HMAC SHA256`. 
- Plaintext passwords are never stored in the database or logs.
- The `session` state drops all credentials upon logout.

## Authorization (Role-Based Access)
- **Admin**: Has overarching access to search all students, run predictions, view analytics, and generate reports.
- **Student**: Operates in an isolated view. The system strictly enforces that a student account can only retrieve, view, and analyze its own specific `student_id`. Unauthorized lookup is blocked at the session layer.

## Database Security
- All interactions with SQLite use parameterized queries to prevent SQL Injection (SQLi) attacks. The GUI layer has no direct SQL access and must route through the Service Layer.

*Note: This system does not claim compliance with specific laws like GDPR or FERPA, as it is an educational demo.*
