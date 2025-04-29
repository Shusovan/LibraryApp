Library Management Application – Overview
Your Library Management Application is an enterprise-grade microservices-based system built using FastAPI. It streamlines the processes of managing books, users, borrowing, and administration in a library environment. The application is divided into multiple services, each with a dedicated responsibility, ensuring modularity and scalability.

Key Microservices -

AdminService :

Manages library admins and their roles (ADMIN, SUPER_ADMIN).

Handles admin registration and role assignment.

Exposes APIs for SecurityService to fetch admin credentials and roles.

UserService :

Manages user registrations and profiles.

Validates users and assigns unique 8-digit user IDs.

Sends requests to the librarian for user approval.

BookService :

Manages book records using uuid and book_id.

Stores details like title, author, description, genre, etc.

Future plan: integrate ML-based genre classification.

BorrowService :

Handles book borrowing requests.

Uses Kafka for communication with the Librarian for approval.

Records verified_by for tracking approvals.

SecurityService :

Manages authentication and JWT-based authorization.

Fetches hashed passwords, roles, and email from AdminService.

Implements role-based access control (RBAC).


Notable Features :-

1. JWT authentication using a centralized SecurityService.

2. Role-based access for users and admins.

3. Clean, modular structure suitable for scaling and integrating AI services.

4. Future integration planned for book description generation and smart genre tagging using Generative AI.
