import 'package:flutter_bloc/flutter_bloc.dart';
import '../../data/datasources/teacher_remote_data_source.dart';
import 'teacher_event.dart';
import 'teacher_state.dart';

class TeacherBloc extends Bloc<TeacherEvent, TeacherState> {
  final TeacherRemoteDataSource remoteDataSource;

  TeacherBloc({required this.remoteDataSource}) : super(TeacherInitial()) {
    on<LoadTeachersEvent>(_onLoadTeachers);
    on<LoadTeacherDetailsEvent>(_onLoadTeacherDetails);
    on<LoadTeacherReviewsEvent>(_onLoadTeacherReviews);
    on<SubmitReviewEvent>(_onSubmitReview);
  }

  Future<void> _onLoadTeachers(
    LoadTeachersEvent event,
    Emitter<TeacherState> emit,
  ) async {
    emit(TeacherLoading());
    try {
      final teachers = await remoteDataSource.getTeachers(
        specialization: event.specialization,
        country: event.country,
        minRating: event.minRating,
        search: event.search,
      );
      emit(TeachersLoaded(teachers, appliedFilter: event.specialization));
    } catch (e) {
      emit(TeacherError(e.toString()));
    }
  }

  Future<void> _onLoadTeacherDetails(
    LoadTeacherDetailsEvent event,
    Emitter<TeacherState> emit,
  ) async {
    emit(TeacherLoading());
    try {
      final teacher = await remoteDataSource.getTeacherDetails(event.teacherId);
      emit(TeacherDetailsLoaded(teacher));
    } catch (e) {
      emit(TeacherError(e.toString()));
    }
  }

  Future<void> _onLoadTeacherReviews(
    LoadTeacherReviewsEvent event,
    Emitter<TeacherState> emit,
  ) async {
    emit(TeacherLoading());
    try {
      final reviews = await remoteDataSource.getTeacherReviews(event.teacherId);
      emit(TeacherReviewsLoaded(reviews));
    } catch (e) {
      emit(TeacherError(e.toString()));
    }
  }

  Future<void> _onSubmitReview(
    SubmitReviewEvent event,
    Emitter<TeacherState> emit,
  ) async {
    emit(TeacherLoading());
    try {
      await remoteDataSource.submitReview(
        teacherId: event.teacherId,
        overallRating: event.overallRating,
        teachingQuality: event.teachingQuality,
        communication: event.communication,
        punctuality: event.punctuality,
        patience: event.patience,
        reviewText: event.reviewText,
      );
      emit(ReviewSubmitted());
    } catch (e) {
      emit(TeacherError(e.toString()));
    }
  }
}
