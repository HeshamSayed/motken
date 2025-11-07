import 'package:dio/dio.dart';
import '../models/package_model.dart';
import '../models/subscription_model.dart';
import '../models/transaction_model.dart';

class PaymentRemoteDataSource {
  final Dio dio;

  PaymentRemoteDataSource({required this.dio});

  Future<List<PackageModel>> getPackages() async {
    final response = await dio.get('/payments/packages/');
    final List<dynamic> results = response.data['results'] ?? response.data;
    return results.map((json) => PackageModel.fromJson(json)).toList();
  }

  Future<PackageModel> getPackageDetails(String packageId) async {
    final response = await dio.get('/payments/packages/$packageId/');
    return PackageModel.fromJson(response.data);
  }

  Future<Map<String, dynamic>> validateCoupon(String code) async {
    final response = await dio.post(
      '/payments/coupons/validate/',
      data: {'code': code},
    );
    return response.data;
  }

  Future<Map<String, dynamic>> initiatePayment({
    required String packageId,
    String? couponCode,
  }) async {
    final response = await dio.post(
      '/payments/transactions/initiate/',
      data: {
        'package_id': packageId,
        if (couponCode != null) 'coupon_code': couponCode,
      },
    );
    return response.data;
  }

  Future<SubscriptionModel> getMySubscription() async {
    final response = await dio.get('/payments/subscriptions/my_subscription/');
    return SubscriptionModel.fromJson(response.data);
  }

  Future<List<TransactionModel>> getTransactions() async {
    final response = await dio.get('/payments/transactions/');
    final List<dynamic> results = response.data['results'] ?? response.data;
    return results.map((json) => TransactionModel.fromJson(json)).toList();
  }

  Future<TransactionModel> getTransactionDetails(String transactionId) async {
    final response = await dio.get('/payments/transactions/$transactionId/');
    return TransactionModel.fromJson(response.data);
  }
}
