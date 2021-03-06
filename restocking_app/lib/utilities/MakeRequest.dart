import 'package:http/http.dart' as http;


import 'package:restocking_app/model/Query.dart';
import 'package:restocking_app/Serializers.dart';
import 'package:restocking_app/model/Order.dart';
import 'package:restocking_app/model/RestockingList.dart';
import 'package:restocking_app/model/Product.dart';



class MakeRequest{
  static const String conn = 'http://192.168.1.186:8000/restocking/rest';
  static Future<http.Response> getRequest(Query query) async{
    final response = await http.get('$conn/${query.model}/${query.query}');
    return response;
  }

  ///Returns the items on an order.
  static Future<Order> encodeOrder(Query query) async{
    final response = await http.get('$conn/${query.model}/${query.query}');

    if (response.statusCode == 200) {
      //Serialise the response from the Django server into an order object.
      return Serializers.orderSerializer(response.body);
    }else{
      return null;
    } 
  }

  static Future<RestockingList> encodeRestockingList(Query query) async{
    final response = await http.get('$conn/${query.model}/${query.query}');
    if (response.statusCode == 200) {
      //Serialise the response from the Django server into a restocking object.
      return Serializers.restockingListSerializer(response.body);
    }else{
      return null;
    } 
  }

  static Future<RestockingList> recommendProduct(Query query)async{
    final response = await http.get('$conn/${query.model}/${query.query}');
    if (response.statusCode == 200) {
      //Serialise the response from the Django server into a restocking object.
      return Serializers.productSerializerRecommend(response.body);
    }else{
      return null;
    } 
  }

  static Future<http.Response> patchRequest(Query query, String data) async{
    print(data);
    final response = await http.patch(
      '$conn/${query.model}/${query.query}',
      body: data,
      headers: {"Content-Type" : "application/json"}
    );
    return response;
  }

  static Future<http.Response> postRequest(Query query, String data) async{
    final response = await http.post(
      '$conn/${query.model}/${query.query}',
      body: data,
      headers: {"Content-Type" : "application/json"}
    );
    return response;
  }

  static Future<String> basicRequest(Query query) async{
    final response = await http.get('$conn/${query.model}/${query.query}');
    if (response.statusCode == 200) {
      //return the raw response text
      return response.body;
    }else{
      return null;
    } 
  }
}