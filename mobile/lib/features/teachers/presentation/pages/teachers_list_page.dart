import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../bloc/teacher_bloc.dart';
import '../bloc/teacher_event.dart';
import '../bloc/teacher_state.dart';
import '../../data/models/teacher_model.dart';

class TeachersListPage extends StatefulWidget {
  const TeachersListPage({super.key});

  @override
  State<TeachersListPage> createState() => _TeachersListPageState();
}

class _TeachersListPageState extends State<TeachersListPage> {
  String? _selectedSpecialization;
  double _maxPrice = 100;
  double _minRating = 0;

  @override
  void initState() {
    super.initState();
    // Load teachers on init
    context.read<TeacherBloc>().add(LoadTeachersEvent());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Find Teachers'),
        actions: [
          IconButton(
            icon: const Icon(Icons.filter_list),
            onPressed: _showFilterDialog,
          ),
        ],
      ),
      body: Column(
        children: [
          // Filter Chips
          _buildFilterChips(),

          // Teachers List
          Expanded(
            child: _buildTeachersList(),
          ),
        ],
      ),
    );
  }

  Widget _buildFilterChips() {
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      padding: const EdgeInsets.all(16),
      child: Row(
        children: [
          FilterChip(
            label: const Text('All'),
            selected: _selectedSpecialization == null,
            onSelected: (selected) {
              setState(() => _selectedSpecialization = null);
              context.read<TeacherBloc>().add(LoadTeachersEvent());
            },
          ),
          const SizedBox(width: 8),
          FilterChip(
            label: const Text('Tajweed'),
            selected: _selectedSpecialization == 'tajweed',
            onSelected: (selected) {
              setState(() => _selectedSpecialization = selected ? 'tajweed' : null);
              context.read<TeacherBloc>().add(LoadTeachersEvent(
                specialization: _selectedSpecialization,
              ));
            },
          ),
          const SizedBox(width: 8),
          FilterChip(
            label: const Text('Memorization'),
            selected: _selectedSpecialization == 'memorization',
            onSelected: (selected) {
              setState(() => _selectedSpecialization = selected ? 'memorization' : null);
              context.read<TeacherBloc>().add(LoadTeachersEvent(
                specialization: _selectedSpecialization,
              ));
            },
          ),
          const SizedBox(width: 8),
          FilterChip(
            label: const Text('Reading'),
            selected: _selectedSpecialization == 'reading',
            onSelected: (selected) {
              setState(() => _selectedSpecialization = selected ? 'reading' : null);
              context.read<TeacherBloc>().add(LoadTeachersEvent(
                specialization: _selectedSpecialization,
              ));
            },
          ),
        ],
      ),
    );
  }

  Widget _buildTeachersList() {
    return BlocBuilder<TeacherBloc, TeacherState>(
      builder: (context, state) {
        if (state is TeacherLoading) {
          return const Center(child: CircularProgressIndicator());
        }

        if (state is TeacherError) {
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.error_outline, size: 64, color: Colors.red),
                const SizedBox(height: 16),
                Text(state.message),
                const SizedBox(height: 16),
                ElevatedButton(
                  onPressed: () {
                    context.read<TeacherBloc>().add(LoadTeachersEvent());
                  },
                  child: const Text('Retry'),
                ),
              ],
            ),
          );
        }

        if (state is TeachersLoaded) {
          if (state.teachers.isEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.school_outlined, size: 64, color: Colors.grey.shade400),
                  const SizedBox(height: 16),
                  Text(
                    'No teachers found',
                    style: TextStyle(fontSize: 18, color: Colors.grey.shade600),
                  ),
                  if (state.appliedFilter != null) ...[
                    const SizedBox(height: 8),
                    TextButton(
                      onPressed: () {
                        setState(() => _selectedSpecialization = null);
                        context.read<TeacherBloc>().add(LoadTeachersEvent());
                      },
                      child: const Text('Clear filters'),
                    ),
                  ],
                ],
              ),
            );
          }

          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: state.teachers.length,
            itemBuilder: (context, index) {
              return _buildTeacherCard(state.teachers[index]);
            },
          );
        }

        return const SizedBox.shrink();
      },
    );
  }

  Widget _buildTeacherCard(TeacherModel teacher) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      child: InkWell(
        onTap: () {
          Navigator.pushNamed(
            context,
            '/book-session',
            arguments: teacher.id,
          );
        },
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              // Avatar
              CircleAvatar(
                radius: 40,
                backgroundColor: Colors.blue.shade100,
                child: Text(
                  teacher.firstName.isNotEmpty ? teacher.firstName[0].toUpperCase() : 'T',
                  style: const TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(width: 16),

              // Info
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      teacher.fullName,
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                    const SizedBox(height: 4),
                    Row(
                      children: [
                        const Icon(Icons.star, size: 16, color: Colors.amber),
                        const SizedBox(width: 4),
                        Text(teacher.averageRating.toStringAsFixed(1)),
                        const SizedBox(width: 8),
                        Text('(${teacher.totalRatings} reviews)'),
                      ],
                    ),
                    const SizedBox(height: 8),
                    Wrap(
                      spacing: 8,
                      children: [
                        ...teacher.specializations.take(2).map((spec) => Chip(
                          label: Text(spec),
                          labelStyle: const TextStyle(fontSize: 12),
                          padding: EdgeInsets.zero,
                          materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                        )),
                        if (teacher.yearsOfExperience > 0)
                          Chip(
                            label: Text('${teacher.yearsOfExperience}+ years'),
                            labelStyle: const TextStyle(fontSize: 12),
                            padding: EdgeInsets.zero,
                            materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                          ),
                      ],
                    ),
                  ],
                ),
              ),

              // Price
              Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  Text(
                    '\$${teacher.session30minRate.toStringAsFixed(0)}',
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          color: Theme.of(context).colorScheme.primary,
                          fontWeight: FontWeight.bold,
                        ),
                  ),
                  const Text('per 30 min'),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _showFilterDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Filter Teachers'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Max Price: \$${_maxPrice.round()}'),
            Slider(
              value: _maxPrice,
              min: 10,
              max: 100,
              divisions: 18,
              label: '\$${_maxPrice.round()}',
              onChanged: (value) {
                setState(() => _maxPrice = value);
              },
            ),
            const SizedBox(height: 16),
            Text('Min Rating: ${_minRating.toStringAsFixed(1)}'),
            Slider(
              value: _minRating,
              min: 0,
              max: 5,
              divisions: 10,
              label: _minRating.toStringAsFixed(1),
              onChanged: (value) {
                setState(() => _minRating = value);
              },
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(context);
              context.read<TeacherBloc>().add(LoadTeachersEvent(
                specialization: _selectedSpecialization,
                minRating: _minRating > 0 ? _minRating : null,
              ));
            },
            child: const Text('Apply'),
          ),
        ],
      ),
    );
  }
}
