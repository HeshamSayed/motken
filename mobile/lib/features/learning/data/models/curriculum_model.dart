import 'package:json_annotation/json_annotation.dart';

part 'curriculum_model.g.dart';

@JsonSerializable()
class CurriculumModel {
  final String id;
  final String name;
  final String slug;
  @JsonKey(name: 'curriculum_type')
  final String curriculumType;
  final String difficulty;
  final String description;
  final String? objectives;
  @JsonKey(name: 'estimated_duration_weeks')
  final int estimatedDurationWeeks;
  @JsonKey(name: 'total_lessons')
  final int totalLessons;
  @JsonKey(name: 'is_published')
  final bool isPublished;
  @JsonKey(name: 'is_featured')
  final bool isFeatured;
  @JsonKey(name: 'created_at')
  final String createdAt;

  CurriculumModel({
    required this.id,
    required this.name,
    required this.slug,
    required this.curriculumType,
    required this.difficulty,
    required this.description,
    this.objectives,
    required this.estimatedDurationWeeks,
    required this.totalLessons,
    required this.isPublished,
    required this.isFeatured,
    required this.createdAt,
  });

  factory CurriculumModel.fromJson(Map<String, dynamic> json) =>
      _$CurriculumModelFromJson(json);

  Map<String, dynamic> toJson() => _$CurriculumModelToJson(this);

  String get difficultyDisplay {
    switch (difficulty) {
      case 'beginner':
        return 'Beginner';
      case 'intermediate':
        return 'Intermediate';
      case 'advanced':
        return 'Advanced';
      default:
        return difficulty;
    }
  }

  String get typeDisplay {
    switch (curriculumType) {
      case 'reading':
        return 'Quran Reading';
      case 'tajweed':
        return 'Tajweed';
      case 'memorization':
        return 'Memorization';
      case 'understanding':
        return 'Understanding';
      case 'tafseer':
        return 'Tafseer';
      case 'recitation':
        return 'Recitation';
      default:
        return curriculumType;
    }
  }
}
