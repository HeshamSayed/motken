import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../bloc/session_bloc.dart';
import '../bloc/session_event.dart';
import '../bloc/session_state.dart';

class BookSessionPage extends StatefulWidget {
  final String teacherId;

  const BookSessionPage({super.key, required this.teacherId});

  @override
  State<BookSessionPage> createState() => _BookSessionPageState();
}

class _BookSessionPageState extends State<BookSessionPage> {
  DateTime _selectedDate = DateTime.now().add(const Duration(days: 1));
  TimeOfDay _selectedTime = const TimeOfDay(hour: 10, minute: 0);
  int _selectedDuration = 30;
  final _curriculumController = TextEditingController();
  final _topicController = TextEditingController();

  @override
  void dispose() {
    _curriculumController.dispose();
    _topicController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return BlocListener<SessionBloc, SessionState>(
      listener: (context, state) {
        if (state is SessionBooked) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Session booked successfully!')),
          );
          Navigator.pop(context);
        }
        if (state is SessionError) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Error: ${state.message}')),
          );
        }
      },
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Book Session'),
        ),
        body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Date Selection
            Card(
              child: ListTile(
                leading: const Icon(Icons.calendar_today),
                title: const Text('Date'),
                subtitle: Text(
                  '${_selectedDate.day}/${_selectedDate.month}/${_selectedDate.year}',
                ),
                trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                onTap: _selectDate,
              ),
            ),
            const SizedBox(height: 16),

            // Time Selection
            Card(
              child: ListTile(
                leading: const Icon(Icons.access_time),
                title: const Text('Time'),
                subtitle: Text(_selectedTime.format(context)),
                trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                onTap: _selectTime,
              ),
            ),
            const SizedBox(height: 16),

            // Duration Selection
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Session Duration',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    const SizedBox(height: 16),
                    SegmentedButton<int>(
                      segments: const [
                        ButtonSegment(
                          value: 30,
                          label: Text('30 min'),
                          icon: Icon(Icons.timer),
                        ),
                        ButtonSegment(
                          value: 45,
                          label: Text('45 min'),
                          icon: Icon(Icons.timer),
                        ),
                        ButtonSegment(
                          value: 60,
                          label: Text('60 min'),
                          icon: Icon(Icons.timer),
                        ),
                      ],
                      selected: {_selectedDuration},
                      onSelectionChanged: (Set<int> selection) {
                        setState(() {
                          _selectedDuration = selection.first;
                        });
                      },
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Curriculum
            TextField(
              controller: _curriculumController,
              decoration: const InputDecoration(
                labelText: 'Curriculum',
                hintText: 'e.g., Tajweed Basics',
                prefixIcon: Icon(Icons.book),
              ),
            ),
            const SizedBox(height: 16),

            // Lesson Topic
            TextField(
              controller: _topicController,
              decoration: const InputDecoration(
                labelText: 'Lesson Topic',
                hintText: 'e.g., Noon Saakin rules',
                prefixIcon: Icon(Icons.topic),
              ),
              maxLines: 2,
            ),
            const SizedBox(height: 24),

            // Price Summary
            Card(
              color: Colors.blue.shade50,
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('Session Price:'),
                        Text(
                          '\$${_calculatePrice()}',
                          style: const TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    Text(
                      '$_selectedDuration minutes session',
                      style: TextStyle(
                        color: Colors.grey.shade700,
                        fontSize: 12,
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Book Button
            ElevatedButton(
              onPressed: _bookSession,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
              child: const Text('Book Session'),
            ),
          ],
        ),
      ),
      ),
    );
  }

  Future<void> _selectDate() async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: _selectedDate,
      firstDate: DateTime.now(),
      lastDate: DateTime.now().add(const Duration(days: 90)),
    );

    if (picked != null && picked != _selectedDate) {
      setState(() {
        _selectedDate = picked;
      });
    }
  }

  Future<void> _selectTime() async {
    final TimeOfDay? picked = await showTimePicker(
      context: context,
      initialTime: _selectedTime,
    );

    if (picked != null && picked != _selectedTime) {
      setState(() {
        _selectedTime = picked;
      });
    }
  }

  String _calculatePrice() {
    final priceMap = {
      30: '15.00',
      45: '20.00',
      60: '25.00',
    };
    return priceMap[_selectedDuration] ?? '15.00';
  }

  Future<void> _bookSession() async {
    if (_curriculumController.text.isEmpty || _topicController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please fill in curriculum and topic')),
      );
      return;
    }

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Confirm Booking'),
        content: Text(
          'Book a $_selectedDuration minute session on '
          '${_selectedDate.day}/${_selectedDate.month}/${_selectedDate.year} '
          'at ${_selectedTime.format(context)}?',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(context);

              // Format date and time for API
              final scheduledDate = '${_selectedDate.year}-'
                  '${_selectedDate.month.toString().padLeft(2, '0')}-'
                  '${_selectedDate.day.toString().padLeft(2, '0')}';
              final scheduledTime = '${_selectedTime.hour.toString().padLeft(2, '0')}:'
                  '${_selectedTime.minute.toString().padLeft(2, '0')}:00';

              // Submit booking via BLoC
              context.read<SessionBloc>().add(BookSessionEvent(
                teacherId: widget.teacherId,
                scheduledDate: scheduledDate,
                scheduledTime: scheduledTime,
                duration: _selectedDuration,
                curriculum: _curriculumController.text,
                lessonTopic: _topicController.text,
              ));
            },
            child: const Text('Confirm'),
          ),
        ],
      ),
    );
  }
}
