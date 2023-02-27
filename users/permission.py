from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and user.quizuser.is_student:
            return True
        return False

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and not  user.quizuser.is_student:
            return True
        return False
# permission class for the user having number saved in databse.
class HaveNumber(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        
        if user.is_authenticated and user.quizuser.number!='0' and not user.quizuser.number_verified:
            return True
        return False