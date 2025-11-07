import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../bloc/payment_bloc.dart';
import '../bloc/payment_event.dart';
import '../bloc/payment_state.dart';
import '../../data/models/package_model.dart';

class PackageDetailsPage extends StatefulWidget {
  final String packageId;

  const PackageDetailsPage({super.key, required this.packageId});

  @override
  State<PackageDetailsPage> createState() => _PackageDetailsPageState();
}

class _PackageDetailsPageState extends State<PackageDetailsPage> {
  final _couponController = TextEditingController();
  Map<String, dynamic>? _appliedCoupon;

  @override
  void dispose() {
    _couponController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Package Details'),
      ),
      body: BlocConsumer<PaymentBloc, PaymentState>(
        listener: (context, state) {
          if (state is CouponValid) {
            _appliedCoupon = state.couponData;
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Coupon applied successfully!')),
            );
          }
          if (state is CouponInvalid) {
            _appliedCoupon = null;
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text(state.message)),
            );
          }
          if (state is PaymentInitiated) {
            // TODO: Open payment URL in webview or browser
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Redirecting to payment...')),
            );
          }
          if (state is PaymentError) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text(state.message)),
            );
          }
        },
        builder: (context, state) {
          if (state is PackagesLoaded) {
            final package = state.packages.firstWhere(
              (p) => p.id == widget.packageId,
              orElse: () => state.packages.first,
            );

            return _buildPackageDetails(context, package, state);
          }

          return const Center(child: CircularProgressIndicator());
        },
      ),
    );
  }

  Widget _buildPackageDetails(
    BuildContext context,
    PackageModel package,
    PackagesLoaded state,
  ) {
    final discount = _appliedCoupon?['discount_amount'] ?? 0.0;
    final finalPrice = package.discountedPrice - discount;

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
                Text(
                  package.name,
                  style: const TextStyle(
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  package.description,
                  style: const TextStyle(
                    fontSize: 16,
                    color: Colors.white70,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 24),
                if (package.isFeatured)
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 6,
                    ),
                    decoration: BoxDecoration(
                      color: Colors.orange,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Text(
                      'MOST POPULAR',
                      style: TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
              ],
            ),
          ),

          Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Package Info
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      children: [
                        _InfoRow(
                          icon: Icons.play_circle_outline,
                          label: 'Total Sessions',
                          value: '${package.sessionCount} sessions',
                        ),
                        const SizedBox(height: 12),
                        _InfoRow(
                          icon: Icons.timer,
                          label: 'Session Duration',
                          value: '${package.sessionDuration} minutes',
                        ),
                        const SizedBox(height: 12),
                        _InfoRow(
                          icon: Icons.calendar_today,
                          label: 'Validity Period',
                          value: '${package.validityDays} days',
                        ),
                        const SizedBox(height: 12),
                        _InfoRow(
                          icon: Icons.attach_money,
                          label: 'Price per Session',
                          value: '\$${package.pricePerSession}/session',
                        ),
                      ],
                    ),
                  ),
                ),

                const SizedBox(height: 24),

                // Features
                if (package.features.isNotEmpty) ...[
                  const Text(
                    'Features Included',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 16),
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        children: package.features
                            .map(
                              (feature) => Padding(
                                padding: const EdgeInsets.only(bottom: 12),
                                child: Row(
                                  children: [
                                    const Icon(
                                      Icons.check_circle,
                                      color: Colors.green,
                                      size: 20,
                                    ),
                                    const SizedBox(width: 12),
                                    Expanded(
                                      child: Text(
                                        feature,
                                        style: const TextStyle(fontSize: 16),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            )
                            .toList(),
                      ),
                    ),
                  ),
                  const SizedBox(height: 24),
                ],

                // Coupon Code
                const Text(
                  'Have a Coupon Code?',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 12),
                Row(
                  children: [
                    Expanded(
                      child: TextField(
                        controller: _couponController,
                        decoration: InputDecoration(
                          hintText: 'Enter coupon code',
                          prefixIcon: const Icon(Icons.local_offer),
                          suffixIcon: _appliedCoupon != null
                              ? IconButton(
                                  icon: const Icon(Icons.close),
                                  onPressed: () {
                                    setState(() {
                                      _appliedCoupon = null;
                                      _couponController.clear();
                                    });
                                    context.read<PaymentBloc>().add(ClearCouponEvent());
                                  },
                                )
                              : null,
                        ),
                        enabled: _appliedCoupon == null,
                      ),
                    ),
                    const SizedBox(width: 8),
                    ElevatedButton(
                      onPressed: _appliedCoupon != null ||
                              state is CouponValidating
                          ? null
                          : () {
                              if (_couponController.text.isNotEmpty) {
                                context.read<PaymentBloc>().add(
                                      ValidateCouponEvent(_couponController.text),
                                    );
                              }
                            },
                      child: state is CouponValidating
                          ? const SizedBox(
                              width: 20,
                              height: 20,
                              child: CircularProgressIndicator(strokeWidth: 2),
                            )
                          : const Text('Apply'),
                    ),
                  ],
                ),

                if (_appliedCoupon != null) ...[
                  const SizedBox(height: 12),
                  Card(
                    color: Colors.green.shade50,
                    child: Padding(
                      padding: const EdgeInsets.all(12),
                      child: Row(
                        children: [
                          Icon(Icons.check_circle, color: Colors.green.shade700),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Text(
                              'Coupon applied! You save \$${discount.toStringAsFixed(2)}',
                              style: TextStyle(
                                color: Colors.green.shade700,
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],

                const SizedBox(height: 32),

                // Price Summary
                Card(
                  color: Colors.blue.shade50,
                  child: Padding(
                    padding: const EdgeInsets.all(20),
                    child: Column(
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            const Text('Package Price:'),
                            Text('\$${package.price.toStringAsFixed(2)}'),
                          ],
                        ),
                        if (package.discountPercent > 0) ...[
                          const SizedBox(height: 8),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text('Discount (${package.discountPercent}%):'),
                              Text(
                                '-\$${(package.price - package.discountedPrice).toStringAsFixed(2)}',
                                style: const TextStyle(color: Colors.green),
                              ),
                            ],
                          ),
                        ],
                        if (_appliedCoupon != null) ...[
                          const SizedBox(height: 8),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              const Text('Coupon Discount:'),
                              Text(
                                '-\$${discount.toStringAsFixed(2)}',
                                style: const TextStyle(color: Colors.green),
                              ),
                            ],
                          ),
                        ],
                        const Divider(height: 24),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            const Text(
                              'Total:',
                              style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            Text(
                              '\$${finalPrice.toStringAsFixed(2)}',
                              style: const TextStyle(
                                fontSize: 24,
                                fontWeight: FontWeight.bold,
                                color: Colors.blue,
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),

                const SizedBox(height: 24),

                // Purchase Button
                ElevatedButton(
                  onPressed: state is PaymentLoading
                      ? null
                      : () {
                          context.read<PaymentBloc>().add(
                                InitiatePaymentEvent(
                                  packageId: package.id,
                                  couponCode: _couponController.text.isEmpty
                                      ? null
                                      : _couponController.text,
                                ),
                              );
                        },
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                  child: state is PaymentLoading
                      ? const CircularProgressIndicator()
                      : const Text('Purchase Package'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _InfoRow extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;

  const _InfoRow({
    required this.icon,
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(icon, color: Theme.of(context).primaryColor),
        const SizedBox(width: 12),
        Expanded(
          child: Text(
            label,
            style: TextStyle(
              color: Colors.grey.shade700,
              fontSize: 14,
            ),
          ),
        ),
        Text(
          value,
          style: const TextStyle(
            fontWeight: FontWeight.w500,
            fontSize: 16,
          ),
        ),
      ],
    );
  }
}
