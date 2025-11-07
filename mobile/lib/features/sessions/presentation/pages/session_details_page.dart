import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:intl/intl.dart';
import 'package:url_launcher/url_launcher.dart';
import '../bloc/session_bloc.dart';
import '../bloc/session_event.dart';
import '../bloc/session_state.dart';

class SessionDetailsPage extends StatefulWidget {
  final String sessionId;

  const SessionDetailsPage({super.key, required this.sessionId});

  @override
  State<SessionDetailsPage> createState() => _SessionDetailsPageState();
}

class _SessionDetailsPageState extends State<SessionDetailsPage> {
  @override
  void initState() {
    super.initState();
    context.read<SessionBloc>().add(LoadSessionDetailsEvent(widget.sessionId));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Session Details'),
      ),
      body: BlocConsumer<SessionBloc, SessionState>(
        listener: (context, state) {
          if (state is SessionJoinReady) {
            _launchUrl(state.joinUrl);
          }
          if (state is SessionCancelled) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Session cancelled successfully')),
            );
            Navigator.pop(context);
          }
        },
        builder: (context, state) {
          if (state is SessionLoading) {
            return const Center(child: CircularProgressIndicator());
          }

          if (state is SessionError) {
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
                      context.read<SessionBloc>().add(
                          LoadSessionDetailsEvent(widget.sessionId));
                    },
                    child: const Text('Retry'),
                  ),
                ],
              ),
            );
          }

          if (state is SessionDetailsLoaded) {
            final session = state.session;
            final dateFormat = DateFormat('EEEE, MMMM dd, yyyy');
            final timeFormat = DateFormat('hh:mm a');

            return SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Header
                  Container(
                    padding: const EdgeInsets.all(24),
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        colors: [
                          Theme.of(context).primaryColor,
                          Theme.of(context).primaryColor.withOpacity(0.7),
                        ],
                      ),
                    ),
                    child: Column(
                      children: [
                        Icon(
                          session.isCompleted
                              ? Icons.check_circle
                              : Icons.video_call,
                          size: 64,
                          color: Colors.white,
                        ),
                        const SizedBox(height: 16),
                        Text(
                          session.statusDisplay,
                          style: const TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                          ),
                        ),
                      ],
                    ),
                  ),

                  // Details
                  Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _DetailCard(
                          title: 'Teacher Information',
                          children: [
                            _DetailRow(
                              icon: Icons.person,
                              label: 'Teacher',
                              value: session.teacherName ?? 'Unknown',
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),
                        _DetailCard(
                          title: 'Session Details',
                          children: [
                            _DetailRow(
                              icon: Icons.calendar_today,
                              label: 'Date',
                              value: dateFormat.format(session.scheduledDateTime),
                            ),
                            const SizedBox(height: 12),
                            _DetailRow(
                              icon: Icons.access_time,
                              label: 'Time',
                              value: timeFormat.format(session.scheduledDateTime),
                            ),
                            const SizedBox(height: 12),
                            _DetailRow(
                              icon: Icons.timer,
                              label: 'Duration',
                              value: '${session.duration} minutes',
                            ),
                            if (session.curriculum != null) ...[
                              const SizedBox(height: 12),
                              _DetailRow(
                                icon: Icons.book,
                                label: 'Curriculum',
                                value: session.curriculum!,
                              ),
                            ],
                            if (session.lessonTopic != null) ...[
                              const SizedBox(height: 12),
                              _DetailRow(
                                icon: Icons.topic,
                                label: 'Topic',
                                value: session.lessonTopic!,
                              ),
                            ],
                          ],
                        ),
                        if (session.sessionPrice != null) ...[
                          const SizedBox(height: 16),
                          _DetailCard(
                            title: 'Payment',
                            children: [
                              _DetailRow(
                                icon: Icons.attach_money,
                                label: 'Price',
                                value: '\$${session.sessionPrice}',
                              ),
                            ],
                          ),
                        ],
                        if (session.recordingUrl != null) ...[
                          const SizedBox(height: 16),
                          _DetailCard(
                            title: 'Recording',
                            children: [
                              ElevatedButton.icon(
                                onPressed: () => _launchUrl(session.recordingUrl!),
                                icon: const Icon(Icons.play_circle),
                                label: const Text('Watch Recording'),
                              ),
                            ],
                          ),
                        ],
                        if (session.cancellationReason != null) ...[
                          const SizedBox(height: 16),
                          _DetailCard(
                            title: 'Cancellation Details',
                            children: [
                              Text(
                                session.cancellationReason!,
                                style: const TextStyle(fontSize: 14),
                              ),
                            ],
                          ),
                        ],
                      ],
                    ),
                  ),

                  // Actions
                  if (session.isScheduled) ...[
                    Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          if (session.canJoin)
                            ElevatedButton.icon(
                              onPressed: () {
                                context.read<SessionBloc>().add(
                                    JoinSessionEvent(session.id));
                              },
                              icon: const Icon(Icons.video_call),
                              label: const Text('Join Session'),
                              style: ElevatedButton.styleFrom(
                                padding: const EdgeInsets.symmetric(vertical: 16),
                              ),
                            ),
                          if (session.canCancel) ...[
                            const SizedBox(height: 12),
                            OutlinedButton.icon(
                              onPressed: () => _showCancelDialog(context),
                              icon: const Icon(Icons.cancel),
                              label: const Text('Cancel Session'),
                              style: OutlinedButton.styleFrom(
                                padding: const EdgeInsets.symmetric(vertical: 16),
                                foregroundColor: Colors.red,
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),
                  ],
                ],
              ),
            );
          }

          return const SizedBox.shrink();
        },
      ),
    );
  }

  Future<void> _launchUrl(String url) async {
    final uri = Uri.parse(url);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    } else {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Could not launch URL')),
        );
      }
    }
  }

  void _showCancelDialog(BuildContext context) {
    final reasonController = TextEditingController();

    showDialog(
      context: context,
      builder: (dialogContext) => AlertDialog(
        title: const Text('Cancel Session'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text(
              'Are you sure you want to cancel this session? This action cannot be undone.',
            ),
            const SizedBox(height: 16),
            TextField(
              controller: reasonController,
              decoration: const InputDecoration(
                labelText: 'Reason for cancellation',
                border: OutlineInputBorder(),
              ),
              maxLines: 3,
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialogContext),
            child: const Text('No, Keep It'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(dialogContext);
              context.read<SessionBloc>().add(
                    CancelSessionEvent(
                      widget.sessionId,
                      reasonController.text.isEmpty
                          ? 'No reason provided'
                          : reasonController.text,
                    ),
                  );
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.red,
            ),
            child: const Text('Yes, Cancel'),
          ),
        ],
      ),
    );
  }
}

class _DetailCard extends StatelessWidget {
  final String title;
  final List<Widget> children;

  const _DetailCard({required this.title, required this.children});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 16),
            ...children,
          ],
        ),
      ),
    );
  }
}

class _DetailRow extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;

  const _DetailRow({
    required this.icon,
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(icon, size: 20, color: Theme.of(context).primaryColor),
        const SizedBox(width: 12),
        Expanded(
          child: Text(
            label,
            style: TextStyle(color: Colors.grey.shade700),
          ),
        ),
        Flexible(
          child: Text(
            value,
            style: const TextStyle(fontWeight: FontWeight.w500),
            textAlign: TextAlign.right,
          ),
        ),
      ],
    );
  }
}
