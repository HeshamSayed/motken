import 'package:flutter/material.dart';

class TeachersListPage extends StatefulWidget {
  const TeachersListPage({super.key});

  @override
  State<TeachersListPage> createState() => _TeachersListPageState();
}

class _TeachersListPageState extends State<TeachersListPage> {
  String _selectedSpecialization = 'all';
  double _maxPrice = 100;
  double _minRating = 0;

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
            label: const Text('Tajweed'),
            selected: _selectedSpecialization == 'tajweed',
            onSelected: (selected) {
              setState(() {
                _selectedSpecialization = selected ? 'tajweed' : 'all';
              });
            },
          ),
          const SizedBox(width: 8),
          FilterChip(
            label: const Text('Memorization'),
            selected: _selectedSpecialization == 'memorization',
            onSelected: (selected) {
              setState(() {
                _selectedSpecialization = selected ? 'memorization' : 'all';
              });
            },
          ),
          const SizedBox(width: 8),
          FilterChip(
            label: const Text('Reading'),
            selected: _selectedSpecialization == 'reading',
            onSelected: (selected) {
              setState(() {
                _selectedSpecialization = selected ? 'reading' : 'all';
              });
            },
          ),
        ],
      ),
    );
  }

  Widget _buildTeachersList() {
    // TODO: Implement actual teacher list with BLoC
    // For now, showing placeholder
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: 10,
      itemBuilder: (context, index) {
        return _buildTeacherCard(index);
      },
    );
  }

  Widget _buildTeacherCard(int index) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      child: InkWell(
        onTap: () {
          // TODO: Navigate to teacher detail
          // context.go('/teacher/123');
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
                  'T${index + 1}',
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
                      'Teacher ${index + 1}',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                    const SizedBox(height: 4),
                    Row(
                      children: [
                        const Icon(Icons.star, size: 16, color: Colors.amber),
                        const SizedBox(width: 4),
                        Text('4.${8 - (index % 3)}'),
                        const SizedBox(width: 8),
                        Text('(${50 + index * 5} reviews)'),
                      ],
                    ),
                    const SizedBox(height: 8),
                    Wrap(
                      spacing: 8,
                      children: [
                        Chip(
                          label: const Text('Tajweed'),
                          labelStyle: const TextStyle(fontSize: 12),
                          padding: EdgeInsets.zero,
                          materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                        ),
                        Chip(
                          label: const Text('10+ years'),
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
                    '\$${15 + index * 2}',
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
              // TODO: Apply filters
            },
            child: const Text('Apply'),
          ),
        ],
      ),
    );
  }
}
