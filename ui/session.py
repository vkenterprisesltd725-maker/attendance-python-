class AppSession:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppSession, cls).__new__(cls)
            cls._instance.clear()
        return cls._instance

    def clear(self):
        self.username = None
        self.role = None
        self.student_id = None

    def login(self, username: str, role: str, student_id: str = None):
        self.username = username
        self.role = role
        self.student_id = student_id

    def is_logged_in(self) -> bool:
        return self.username is not None

    def is_admin(self) -> bool:
        return self.role == 'admin'

    def is_student(self) -> bool:
        return self.role == 'student'

# Global session instance
session = AppSession()
