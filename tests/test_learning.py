import unittest
from mrs import (
    Course, Module, VideoLesson,
    EnrollmentRepo, CourseRepo, LearningService
)


class TestLearningSystem(unittest.TestCase):

    def setUp(self):
        self.course_repo = CourseRepo()
        self.enrollment_repo = EnrollmentRepo()
        self.service = LearningService(self.enrollment_repo, self.course_repo)

        # Create course with lessons
        self.course = Course(1, "Python")
        module = Module(1, "Basics")
        module.add_lesson(VideoLesson(1, "Intro"))
        module.add_lesson(VideoLesson(2, "Variables"))

        self.course.add_module(module)
        self.course_repo.add(self.course)

    def test_enrollment(self):
        self.service.enroll_student(1, 1)
        enrollment = self.enrollment_repo.get(1, 1)

        self.assertIsNotNone(enrollment)

    def test_duplicate_enrollment(self):
        self.service.enroll_student(1, 1)
        with self.assertRaises(Exception):
            self.service.enroll_student(1, 1)

    def test_progress(self):
        self.service.enroll_student(1, 1)

        self.service.mark_lesson_complete(1, 1, 1)
        progress = self.service.get_progress(1, 1)

        self.assertEqual(progress, 50.0)

    def test_invalid_lesson(self):
        self.service.enroll_student(1, 1)

        with self.assertRaises(Exception):
            self.service.mark_lesson_complete(1, 1, 999)


if __name__ == "__main__":
    unittest.main()