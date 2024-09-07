import 'package:flutter/material.dart';
import 'package:flutter_nfc_kit/flutter_nfc_kit.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String _nfcData = 'NFC data will appear here';
  TextEditingController _textFieldController = TextEditingController();
  TextEditingController _textFieldControllerDate = TextEditingController();

  Future<void> _sendDataToServer() async {
    final url = Uri.parse('https://82e1-211-75-133-2.ngrok-free.app/set_isEntry');
    final response = await http.post(
      url,
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        'location': _textFieldController.text,
        'date': _textFieldControllerDate.text,
      }),
    );

    if (response.statusCode == 200) {
      // If the server returns a 200 OK response, parse the JSON
      print('Data sent successfully');
      // You can add more logic here to handle the response
    } else {
      // If the server did not return a 200 OK response,
      // throw an exception or handle the error
      print('Failed to send data. Status code: ${response.statusCode}');
    }
  }

  @override
  void dispose() {
    _textFieldController.dispose();
    super.dispose();
  }

  void _readNFC() async {
  try {
    NFCTag tag = await FlutterNfcKit.poll(
      timeout: Duration(seconds: 30), // 增加超時時間
      iosAlertMessage: "Hold your phone near the NFC   tag"
    );
    setState(() { 
      _nfcData = tag.id.toString();
    });
    await _sendDataToServer();
  } catch (e) {
    // 處理錯誤或通知用戶
      print(e);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('NFC Reader'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            TextField(
              controller: _textFieldControllerDate,
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Enter date here',
              ),
              onChanged: (value) {
                // You can handle the text change here if needed
              },
            ),
            SizedBox(height: 20), // Add some space between TextField and Button
            TextField(
              controller: _textFieldController,
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Enter location here',
              ),
              onChanged: (value) {
                // You can handle the text change here if needed
              },
            ),
            SizedBox(height: 20), // Add some space between TextField and Button
            ElevatedButton(
              onPressed: _readNFC,
              child: Text('Read NFC'),
            ),
            Text(_nfcData),
          ],
        ),
      ),
    );
  }
}