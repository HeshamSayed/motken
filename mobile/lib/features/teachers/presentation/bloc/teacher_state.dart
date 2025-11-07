import '../../data/models/teacher_model.dart';

abstract class TeacherState {}

class TeacherInitial extends TeacherState {}

class TeacherLoading extends TeacherState {}

class TeachersLoaded extends TeacherState {
  final List<TeacherModel> teachers;
  final String? appliedFilter;

  TeachersLoaded(this.teachers, {this.appliedFilter});
}

class TeacherDetailsLoaded extends TeacherState {
  final TeacherModel teacher;
  TeacherDetailsLoaded(this.teacher);
}

class TeacherReviewsLoaded extends TeacherState {
  final List<dynamic> reviews;
  TeacherReviewsLoaded(this.reviews);
}

class ReviewSubmitted extends TeacherState {}

class TeacherError extends TeacherState {
  final String message;
  TeacherError(this.message);
}
