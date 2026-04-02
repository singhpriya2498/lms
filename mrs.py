from abc import ABC,abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class User(ABC):
    id: int
    name: str
    email: str

@dataclass
class Student(User):
    pass

@dataclass
class Instructor(User):
    pass

@dataclass
class Admin(User):
    pass

class Lesson(ABC):
    def __init__(self, lesson_id:int, title: str):
        self.id = lesson_id
        self.title = title
    
    @abstractmethod
    def complete(self):
        pass

class VideoLesson(Lesson):
    def complete(self):
        return "Video lesson complete"
    
class QuizLesson(Lesson):
    def complete(self):
        return "Quiz lesson complete"
    
class LiveWebinarLesson(Lesson):
    def complete(self):
        return "Webinar attended"
    
class Module:
    def __init__(self,module_id:int, title: str):
        self.id = module_id
        self.title = title
        self.lessons: List[Lesson] = []

    def add_lesson(self, lesson: Lesson):
        self.lessons.append(lesson)

class Course:
    def __init__(self,course_id: int, title: str):
        self.id = course_id
        self.title = title
        self.modules: List[Module] = []

    def add_module(self , module: Module):
        self.modules.append(module)

    def has_lesson(self, lesson_id: int)->bool:
        for module in self.modules:
            for lesson in module.lessons:
                if lesson.id == lesson_id:
                    return True
        return False
    
    def get_total_lessons(self) -> int:
        count = 0
        for module in self.modules:
            count += len(module.lessons)
        return count
    
class Enrollment:
    def __init__(self, student_id: int, course_id: int):
        self.student_id = student_id
        self.course_id = course_id
        self.completed_lessons: set[int] = set() #using set to keep distinct lessons
    def mark_complete(self, lesson_id: int):
        self.completed_lessons.add(lesson_id)

    def get_progress(self, total_lessons: int) -> float:
        if total_lessons == 0:
            return 0.0
        return (len(self.completed_lessons) / total_lessons) * 100
    
class EnrollmentRepo:
    def __init__(self):
        self.enrollments = {}

    def add(self, enrollment: Enrollment):
        key = (enrollment.student_id, enrollment.course_id)
        self.enrollments[key] = enrollment

    def get(self, student_id: int, course_id: int) -> Enrollment | None:
        return self.enrollments.get((student_id, course_id))
    
class CourseRepo:
    def __init__(self):
        self.courses = {}

    def add(self, course: Course):
        self.courses[course.id] = course

    def get(self, course_id: int) -> Course | None:
        return self.courses.get(course_id)
    

class LearningService:
    def __init__(self, enrollment_repo: EnrollmentRepo, course_repo: CourseRepo):
        self.enrollment_repo = enrollment_repo
        self.course_repo = course_repo

    def enroll_student(self, student_id: int, course_id: int):
        existing = self.enrollment_repo.get(student_id, course_id)

        if existing:
            raise Exception("Student already enrolled")

        enrollment = Enrollment(student_id, course_id)
        self.enrollment_repo.add(enrollment)

    def mark_lesson_complete(self, student_id: int, course_id: int, lesson_id: int):
        enrollment = self.enrollment_repo.get(student_id, course_id)

        if not enrollment:
            raise Exception("Student not enrolled in course")

        course = self.course_repo.get(course_id)
        if not course:
            raise Exception("Course not found")

        if not course.has_lesson(lesson_id):
            raise Exception("Lesson does not belong to this course")

        enrollment.mark_complete(lesson_id)

    def get_progress(self, student_id: int, course_id: int) -> float:
        enrollment = self.enrollment_repo.get(student_id, course_id)

        if not enrollment:
            raise Exception("Student not enrolled")

        course = self.course_repo.get(course_id)
        total_lessons = course.get_total_lessons()

        return enrollment.get_progress(total_lessons)