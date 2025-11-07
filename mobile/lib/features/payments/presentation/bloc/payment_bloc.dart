import 'package:flutter_bloc/flutter_bloc.dart';
import '../../data/datasources/payment_remote_data_source.dart';
import 'payment_event.dart';
import 'payment_state.dart';

class PaymentBloc extends Bloc<PaymentEvent, PaymentState> {
  final PaymentRemoteDataSource remoteDataSource;

  PaymentBloc({required this.remoteDataSource}) : super(PaymentInitial()) {
    on<LoadPackagesEvent>(_onLoadPackages);
    on<SelectPackageEvent>(_onSelectPackage);
    on<ValidateCouponEvent>(_onValidateCoupon);
    on<InitiatePaymentEvent>(_onInitiatePayment);
    on<LoadSubscriptionEvent>(_onLoadSubscription);
    on<LoadTransactionsEvent>(_onLoadTransactions);
    on<ClearCouponEvent>(_onClearCoupon);
  }

  Future<void> _onLoadPackages(
    LoadPackagesEvent event,
    Emitter<PaymentState> emit,
  ) async {
    emit(PaymentLoading());
    try {
      final packages = await remoteDataSource.getPackages();
      emit(PackagesLoaded(packages));
    } catch (e) {
      emit(PaymentError(e.toString()));
    }
  }

  Future<void> _onSelectPackage(
    SelectPackageEvent event,
    Emitter<PaymentState> emit,
  ) async {
    if (state is PackagesLoaded) {
      final currentState = state as PackagesLoaded;
      final selectedPackage = currentState.packages.firstWhere(
        (pkg) => pkg.id == event.packageId,
      );
      emit(currentState.copyWith(selectedPackage: selectedPackage));
    }
  }

  Future<void> _onValidateCoupon(
    ValidateCouponEvent event,
    Emitter<PaymentState> emit,
  ) async {
    emit(CouponValidating());
    try {
      final couponData = await remoteDataSource.validateCoupon(event.couponCode);

      if (state is PackagesLoaded) {
        final currentState = state as PackagesLoaded;
        emit(currentState.copyWith(couponData: couponData));
      } else {
        emit(CouponValid(couponData));
      }
    } catch (e) {
      emit(CouponInvalid(e.toString()));

      // Restore previous state
      if (state is PackagesLoaded) {
        emit(state as PackagesLoaded);
      }
    }
  }

  Future<void> _onInitiatePayment(
    InitiatePaymentEvent event,
    Emitter<PaymentState> emit,
  ) async {
    emit(PaymentLoading());
    try {
      final result = await remoteDataSource.initiatePayment(
        packageId: event.packageId,
        couponCode: event.couponCode,
      );

      final paymentUrl = result['payment_url'] as String;
      final transactionId = result['transaction_id'] as String;

      emit(PaymentInitiated(paymentUrl, transactionId));
    } catch (e) {
      emit(PaymentError(e.toString()));
    }
  }

  Future<void> _onLoadSubscription(
    LoadSubscriptionEvent event,
    Emitter<PaymentState> emit,
  ) async {
    emit(PaymentLoading());
    try {
      final subscription = await remoteDataSource.getMySubscription();
      emit(SubscriptionLoaded(subscription));
    } catch (e) {
      emit(PaymentError(e.toString()));
    }
  }

  Future<void> _onLoadTransactions(
    LoadTransactionsEvent event,
    Emitter<PaymentState> emit,
  ) async {
    emit(PaymentLoading());
    try {
      final transactions = await remoteDataSource.getTransactions();
      emit(TransactionsLoaded(transactions));
    } catch (e) {
      emit(PaymentError(e.toString()));
    }
  }

  Future<void> _onClearCoupon(
    ClearCouponEvent event,
    Emitter<PaymentState> emit,
  ) async {
    if (state is PackagesLoaded) {
      final currentState = state as PackagesLoaded;
      emit(currentState.copyWith(clearCoupon: true));
    }
  }
}
