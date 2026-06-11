# Database Design

## Tables

### Users
- user_id (Primary Key)
- name
- email
- password
- phone

### Complaints
- complaint_id (Primary Key)
- user_id (Foreign Key)
- location
- complaint_type
- description
- status
- complaint_date

### Admin
- admin_id (Primary Key)
- username
- password

## Relationships

- One User can submit many Complaints.
- Admin manages Complaints.
- Complaint status is updated by Admin.
