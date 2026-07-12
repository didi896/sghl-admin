class PatientModel {
  final int id;
  final String nom;
  final String prenom;
  final String ipp;

  PatientModel({required this.id, required this.nom, required this.prenom, required this.ipp});

  factory PatientModel.fromJson(Map<String, dynamic> json) {
    return PatientModel(
      id: json['id'],
      nom: json['nom'],
      prenom: json['prenom'],
      ipp: json['ipp'],
    );
  }
}