import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class ApiService {
  final Dio _dio = Dio(BaseOptions(
    baseUrl: 'http://10.0.2.2:8000/api/', // 10.0.2.2 correspond à localhost pour l'émulateur Android
    connectTimeout: const Duration(seconds: 5),
    receiveTimeout: const Duration(seconds: 3),
  ));
  
  final _storage = const FlutterSecureStorage();

  ApiService() {
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        // Exigence 2.4 : Récupération sécurisée du token JWT au repos
        String? token = await _storage.read(key: 'access_token');
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        return handler.next(options);
      },
      onError: (DioException e, handler) async {
        // Exigence 2.4 : Logique de rafraîchissement des jetons en cas d'expiration (rotation de token)
        if (e.response?.statusCode == 401) {
          String? refreshToken = await _storage.read(key: 'refresh_token');
          if (refreshToken != null) {
            // Implémenter ici l'appel vers l'endpoint de rafraîchissement
          }
        }
        return handler.next(e);
      },
    ));
  }

  Dio get client => _dio;
}