# College ERP – MySQL Schema Design

Scalable schema with 14 tables: primary keys, foreign keys, relationships, and indexes.

---

## Entity Relationship Overview

```
roles ──┬── users ──┬── students ──┬── enrollments ── courses ── departments
        │           │              │        │              │
        │           │              │        └──────────────┘
        │           │              ├── attendance ── subjects ── courses
        │           │              ├── submissions ── assignments ── subjects
        │           │              └── results ────── subjects
        │           │
        │           └── faculty ──── departments
        │
        └── notices (created_by)   timetable ── courses, subjects, faculty
```

---

## Tables

### 1. `roles`

Lookup table for user roles (student, faculty, admin).

| Column       | Type         | Constraints        | Description        |
|-------------|--------------|--------------------|--------------------|
| id          | INT          | PK, AUTO_INCREMENT | Primary key        |
| name        | VARCHAR(50) | NOT NULL, UNIQUE   | Role name          |
| description | VARCHAR(255)| NULL               | Optional description |

**Indexes:** `PRIMARY (id)`, `UNIQUE (name)`.

---

### 2. `users`

Central identity and authentication; links to `roles`.

| Column          | Type         | Constraints        | Description        |
|-----------------|--------------|--------------------|--------------------|
| id              | INT          | PK, AUTO_INCREMENT | Primary key        |
| email           | VARCHAR(255) | NOT NULL, UNIQUE   | Login email        |
| full_name       | VARCHAR(255) | NOT NULL           | Display name       |
| hashed_password | VARCHAR(255) | NOT NULL           | Password hash      |
| role_id         | INT          | NOT NULL, FK→roles | Role               |
| is_active       | TINYINT(1)   | NOT NULL, DEFAULT 1| Active flag        |
| created_at      | DATETIME     | NOT NULL           | Creation time      |
| updated_at      | DATETIME     | NOT NULL           | Last update        |

**Foreign keys:** `role_id` → `roles(id)`.

**Indexes:** `PRIMARY (id)`, `UNIQUE (email)`, `INDEX (role_id)`.

---

### 3. `departments`

Academic departments (e.g. CSE, ECE).

| Column      | Type         | Constraints        | Description        |
|-------------|--------------|--------------------|--------------------|
| id          | INT          | PK, AUTO_INCREMENT | Primary key        |
| name        | VARCHAR(100) | NOT NULL           | Department name    |
| code        | VARCHAR(20)  | NOT NULL, UNIQUE   | Short code         |
| description | TEXT         | NULL               | Optional           |
| created_at  | DATETIME     | NOT NULL           | Creation time      |
| updated_at  | DATETIME     | NOT NULL           | Last update        |

**Indexes:** `PRIMARY (id)`, `UNIQUE (code)`.

---

### 4. `courses`

Programs offered by departments (e.g. B.Tech CSE, MCA).

| Column         | Type         | Constraints           | Description        |
|----------------|--------------|------------------------|--------------------|
| id             | INT          | PK, AUTO_INCREMENT    | Primary key        |
| name           | VARCHAR(150) | NOT NULL              | Course name        |
| code           | VARCHAR(30)  | NOT NULL, UNIQUE      | Course code        |
| department_id  | INT          | NOT NULL, FK→departments | Department      |
| duration_years | TINYINT      | NOT NULL              | Duration in years  |
| created_at     | DATETIME     | NOT NULL              | Creation time      |
| updated_at     | DATETIME     | NOT NULL              | Last update        |

**Foreign keys:** `department_id` → `departments(id)`.

**Indexes:** `PRIMARY (id)`, `UNIQUE (code)`, `INDEX (department_id)`.

---

### 5. `subjects`

Subjects under a course (and semester).

| Column      | Type         | Constraints        | Description        |
|-------------|--------------|--------------------|--------------------|
| id          | INT          | PK, AUTO_INCREMENT | Primary key        |
| name        | VARCHAR(150) | NOT NULL           | Subject name       |
| code        | VARCHAR(30)  | NOT NULL           | Subject code       |
| course_id   | INT          | NOT NULL, FK→courses | Course           |
| semester    | TINYINT      | NOT NULL           | Semester number   |
| credits     | DECIMAL(4,2) | NULL               | Credit hours      |
| created_at  | DATETIME     | NOT NULL           | Creation time      |
| updated_at  | DATETIME     | NOT NULL           | Last update        |

**Foreign keys:** `course_id` → `courses(id)`.

**Indexes:** `PRIMARY (id)`, `UNIQUE (course_id, code)`, `INDEX (course_id)`.

---

### 6. `students`

Student profile; one-to-one with `users`.

| Column         | Type         | Constraints           | Description        |
|----------------|--------------|------------------------|--------------------|
| id             | INT          | PK, AUTO_INCREMENT    | Primary key        |
| user_id        | INT          | NOT NULL, UNIQUE, FK→users | User identity  |
| roll_number    | VARCHAR(50)  | NOT NULL, UNIQUE      | Roll number        |
| department_id  | INT          | NOT NULL, FK→departments | Department     |
| course_id      | INT          | NOT NULL, FK→courses  | Enrolled course    |
| batch          | VARCHAR(20)  | NOT NULL              | Batch / year       |
| created_at     | DATETIME     | NOT NULL              | Creation time      |
| updated_at     | DATETIME     | NOT NULL              | Last update        |

**Foreign keys:** `user_id` → `users(id)`, `department_id` → `departments(id)`, `course_id` → `courses(id)`.

**Indexes:** `PRIMARY (id)`, `UNIQUE (user_id)`, `UNIQUE (roll_number)`, `INDEX (department_id)`, `INDEX (course_id)`, `INDEX (batch)`.

---

### 7. `faculty`

Faculty profile; one-to-one with `users`.

| Column        | Type         | Constraints           | Description        |
|---------------|--------------|------------------------|--------------------|
| id            | INT          | PK, AUTO_INCREMENT    | Primary key        |
| user_id       | INT          | NOT NULL, UNIQUE, FK→users | User identity  |
| employee_id   | VARCHAR(50)  | NOT NULL, UNIQUE      | Employee ID        |
| department_id | INT          | NOT NULL, FK→departments | Department     |
| designation   | VARCHAR(100) | NULL                  | Designation        |
| created_at    | DATETIME     | NOT NULL              | Creation time      |
| updated_at    | DATETIME     | NOT NULL              | Last update        |

**Foreign keys:** `user_id` → `users(id)`, `department_id` → `departments(id)`.

**Indexes:** `PRIMARY (id)`, `UNIQUE (user_id)`, `UNIQUE (employee_id)`, `INDEX (department_id)`.

---

### 8. `enrollments`

Student enrollment in a course for an academic year.

| Column        | Type         | Constraints              | Description        |
|---------------|--------------|---------------------------|--------------------|
| id            | INT          | PK, AUTO_INCREMENT       | Primary key        |
| student_id    | INT          | NOT NULL, FK→students    | Student            |
| course_id     | INT          | NOT NULL, FK→courses     | Course             |
| academic_year | VARCHAR(20)  | NOT NULL                 | e.g. 2023-24       |
| enrolled_at   | DATETIME     | NOT NULL                 | Enrollment date    |
| status        | VARCHAR(20)  | NOT NULL                 | active/dropped/completed |
| created_at    | DATETIME     | NOT NULL                 | Creation time      |
| updated_at    | DATETIME     | NOT NULL                 | Last update        |

**Foreign keys:** `student_id` → `students(id)`, `course_id` → `courses(id)`.

**Indexes:** `PRIMARY (id)`, `UNIQUE (student_id, course_id, academic_year)`, `INDEX (student_id)`, `INDEX (course_id)`, `INDEX (academic_year)`.

---

### 9. `attendance`

Per-student, per-subject, per-date attendance.

| Column     | Type         | Constraints           | Description        |
|------------|--------------|------------------------|--------------------|
| id         | INT          | PK, AUTO_INCREMENT    | Primary key        |
| student_id | INT          | NOT NULL, FK→students | Student            |
| subject_id | INT          | NOT NULL, FK→subjects  | Subject            |
| date       | DATE         | NOT NULL              | Attendance date    |
| status     | VARCHAR(20)  | NOT NULL              | present/absent/late |
| remarks    | VARCHAR(255) | NULL                  | Optional remarks   |
| created_at | DATETIME     | NOT NULL              | Creation time      |

**Foreign keys:** `student_id` → `students(id)`, `subject_id` → `subjects(id)`.

**Indexes:** `PRIMARY (id)`, `UNIQUE (student_id, subject_id, date)`, `INDEX (student_id, date)`, `INDEX (subject_id, date)`.

---

### 10. `assignments`

Assignments for a subject, created by faculty.

| Column        | Type         | Constraints           | Description        |
|---------------|--------------|------------------------|--------------------|
| id            | INT          | PK, AUTO_INCREMENT    | Primary key        |
| subject_id    | INT          | NOT NULL, FK→subjects | Subject            |
| created_by_id | INT          | NOT NULL, FK→faculty  | Creator (faculty)  |
| title         | VARCHAR(255) | NOT NULL              | Title              |
| description   | TEXT         | NULL                  | Description        |
| due_at        | DATETIME     | NOT NULL              | Due date/time      |
| status        | VARCHAR(20)  | NOT NULL              | draft/published/closed |
| created_at    | DATETIME     | NOT NULL              | Creation time      |
| updated_at    | DATETIME     | NOT NULL              | Last update        |

**Foreign keys:** `subject_id` → `subjects(id)`, `created_by_id` → `faculty(id)`.

**Indexes:** `PRIMARY (id)`, `INDEX (subject_id)`, `INDEX (created_by_id)`, `INDEX (due_at)`, `INDEX (status)`.

---

### 11. `submissions`

Student submission for an assignment.

| Column        | Type         | Constraints              | Description        |
|---------------|--------------|---------------------------|--------------------|
| id            | INT          | PK, AUTO_INCREMENT       | Primary key        |
| assignment_id | INT          | NOT NULL, FK→assignments | Assignment         |
| student_id    | INT          | NOT NULL, FK→students    | Student            |
| submitted_at  | DATETIME     | NOT NULL                 | Submission time    |
| file_path     | VARCHAR(500) | NULL                     | Stored file path   |
| content       | TEXT         | NULL                     | Inline content     |
| marks_given   | DECIMAL(5,2) | NULL                     | Marks awarded      |
| feedback      | TEXT         | NULL                     | Feedback           |
| created_at    | DATETIME     | NOT NULL                 | Creation time      |
| updated_at    | DATETIME     | NOT NULL                 | Last update        |

**Foreign keys:** `assignment_id` → `assignments(id)`, `student_id` → `students(id)`.

**Indexes:** `PRIMARY (id)`, `UNIQUE (assignment_id, student_id)`, `INDEX (assignment_id)`, `INDEX (student_id)`.

---

### 12. `results`

Exam results per student, per subject, per exam type and year.

| Column         | Type         | Constraints           | Description        |
|----------------|--------------|------------------------|--------------------|
| id             | INT          | PK, AUTO_INCREMENT    | Primary key        |
| student_id     | INT          | NOT NULL, FK→students | Student            |
| subject_id     | INT          | NOT NULL, FK→subjects | Subject            |
| exam_type      | VARCHAR(20)  | NOT NULL              | mid_term/final     |
| academic_year  | VARCHAR(20)  | NOT NULL              | e.g. 2023-24       |
| marks_obtained | DECIMAL(5,2) | NOT NULL              | Marks              |
| max_marks      | DECIMAL(5,2) | NOT NULL              | Maximum marks      |
| grade          | VARCHAR(10)  | NULL                  | Grade              |
| created_at     | DATETIME     | NOT NULL              | Creation time      |
| updated_at     | DATETIME     | NOT NULL              | Last update        |

**Foreign keys:** `student_id` → `students(id)`, `subject_id` → `subjects(id)`.

**Indexes:** `PRIMARY (id)`, `UNIQUE (student_id, subject_id, exam_type, academic_year)`, `INDEX (student_id)`, `INDEX (subject_id)`, `INDEX (academic_year)`.

---

### 13. `notices`

Announcements; optional department and audience.

| Column          | Type         | Constraints           | Description        |
|-----------------|--------------|------------------------|--------------------|
| id              | INT          | PK, AUTO_INCREMENT    | Primary key        |
| title           | VARCHAR(255) | NOT NULL              | Title              |
| content         | TEXT         | NOT NULL              | Body               |
| created_by_id   | INT          | NOT NULL, FK→users    | Author             |
| target_audience | VARCHAR(20)  | NOT NULL              | all/students/faculty |
| department_id   | INT          | NULL, FK→departments  | Scope (null = all) |
| created_at      | DATETIME     | NOT NULL              | Creation time      |
| updated_at      | DATETIME     | NOT NULL              | Last update        |

**Foreign keys:** `created_by_id` → `users(id)`, `department_id` → `departments(id)`.

**Indexes:** `PRIMARY (id)`, `INDEX (created_by_id)`, `INDEX (department_id)`, `INDEX (created_at)`.

---

### 14. `timetable`

Class slots: course, subject, faculty, day, time, room.

| Column        | Type         | Constraints           | Description        |
|---------------|--------------|------------------------|--------------------|
| id            | INT          | PK, AUTO_INCREMENT    | Primary key        |
| course_id     | INT          | NOT NULL, FK→courses  | Course             |
| subject_id    | INT          | NOT NULL, FK→subjects | Subject            |
| faculty_id    | INT          | NOT NULL, FK→faculty  | Faculty            |
| day_of_week   | TINYINT      | NOT NULL              | 1=Mon … 7=Sun      |
| start_time    | TIME         | NOT NULL              | Start time         |
| end_time      | TIME         | NOT NULL              | End time           |
| room          | VARCHAR(50)  | NULL                  | Room               |
| academic_year | VARCHAR(20)  | NOT NULL              | e.g. 2023-24       |
| created_at    | DATETIME     | NOT NULL              | Creation time      |
| updated_at    | DATETIME     | NOT NULL              | Last update        |

**Foreign keys:** `course_id` → `courses(id)`, `subject_id` → `subjects(id)`, `faculty_id` → `faculty(id)`.

**Indexes:** `PRIMARY (id)`, `INDEX (course_id, day_of_week)`, `INDEX (faculty_id, day_of_week)`, `INDEX (academic_year)`.

---

## Summary of Relationships

| From table   | To table    | Relationship        |
|-------------|-------------|---------------------|
| users       | roles       | N:1 (role_id)       |
| students    | users       | 1:1 (user_id)       |
| students    | departments | N:1                 |
| students    | courses     | N:1                 |
| faculty     | users       | 1:1 (user_id)       |
| faculty     | departments | N:1                 |
| courses     | departments | N:1                 |
| subjects    | courses     | N:1                 |
| enrollments | students    | N:1                 |
| enrollments | courses     | N:1                 |
| attendance  | students    | N:1                 |
| attendance  | subjects    | N:1                 |
| assignments | subjects    | N:1                 |
| assignments | faculty     | N:1                 |
| submissions | assignments | N:1                 |
| submissions | students    | N:1                 |
| results     | students    | N:1                 |
| results     | subjects    | N:1                 |
| notices     | users       | N:1                 |
| notices     | departments | N:1 (optional)      |
| timetable   | courses     | N:1                 |
| timetable   | subjects    | N:1                 |
| timetable   | faculty     | N:1                 |

---

## Index Summary

- **Primary keys** on all 14 tables.
- **Unique constraints** where needed: `users.email`, `students.roll_number`, `students.user_id`, `faculty.user_id`, `faculty.employee_id`, `departments.code`, `courses.code`, `(subjects.course_id, subjects.code)`, `(enrollments.student_id, course_id, academic_year)`, `(attendance.student_id, subject_id, date)`, `(submissions.assignment_id, student_id)`, `(results.student_id, subject_id, exam_type, academic_year)`.
- **Non-unique indexes** on all foreign keys and on frequently filtered columns (e.g. dates, academic_year, status) for scalable queries.
