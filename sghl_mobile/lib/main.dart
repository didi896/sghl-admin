import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

void main() {
  runApp(const SghlPatientApp());
}

class SghlPatientApp extends StatelessWidget {
  const SghlPatientApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SGHL Portail Patient',
      theme: ThemeData(
        primarySwatch: Colors.teal,
        textTheme: GoogleFonts.poppinsTextTheme(Theme.of(context).textTheme),
        useMaterial3: true,
      ),
      home: const PatientDashboard(),
    );
  }
}

class PatientDashboard extends StatelessWidget {
  const PatientDashboard({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('SGHL - Espace Patient', style: TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: Colors.teal,
        foregroundColor: Colors.white,
        actions: [
          IconButton(icon: const Icon(Icons.notifications_active), onPressed: () {}),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Section Informations Générales
            _buildWelcomeCard(),
            const SizedBox(height: 24),
            
            // Axe 1 : Observance (Rappels Médicamenteux Critiques)
            _buildSectionTitle('Traitement & Observance'),
            const SizedBox(height: 8),
            _buildReminderCard('Amoxicilline 500mg', 'Prochaine prise à 14:00', Icons.medication),
            const SizedBox(height: 20),

            // Axes 2 & 3 : Actions (Prise de RDV, Historique)
            _buildSectionTitle('Services en ligne'),
            const SizedBox(height: 8),
            GridView.count(
              crossAxisCount: 2,
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              crossAxisSpacing: 12,
              mainAxisSpacing: 12,
              children: [
                _buildServiceButton(context, 'Prendre RDV', Icons.calendar_month, Colors.blue),
                _buildServiceButton(context, 'Mes Examens', Icons.science, Colors.purple),
                _buildServiceButton(context, 'Dossier Médical', Icons.folder_shared, Colors.orange),
                _buildServiceButton(context, 'Messagerie', Icons.chat, Colors.green),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildWelcomeCard() {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      color: Colors.teal.shade50,
      child: const Padding(
        padding: EdgeInsets.all(16.0),
        child: Row(
          children: [
            CircleAvatar(radius: 30, backgroundColor: Colors.teal, child: Icon(Icons.person, color: Colors.white, size: 30)),
            SizedBox(width: 16),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Bienvenue, Patient', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                Text('IPP: IPP-2026-98745', style: TextStyle(color: Colors.grey)),
              ],
            )
          ],
        ),
      ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.black87));
  }

  Widget _buildReminderCard(String med, String time, IconData icon) {
    return Card(
      color: Colors.red.shade50,
      shape: RoundedRectangleBorder(side: BorderSide(color: Colors.red.shade200), borderRadius: BorderRadius.circular(12)),
      child: ListTile(
        leading: Icon(icon, color: Colors.red, size: 28),
        title: Text(med, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Text(time),
        trailing: const Icon(Icons.alarm, color: Colors.red),
      ),
    );
  }

  Widget _buildServiceButton(BuildContext context, String title, IconData icon, Color color) {
    return InkWell(
      onTap: () {},
      child: Card(
        elevation: 1,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 40, color: color),
            const SizedBox(height: 8),
            Text(title, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14), textAlign: TextAlign.center),
          ],
        ),
      ),
    );
  }
}