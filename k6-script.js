import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
//    vus: 20,
//    iterations: 1,
//    duration: '20s',
    stages: [
      { duration: '10s', target: 10 },
      { duration: '1m', target: 100 },
      { duration: '1m', target: 200 },
    ],

  };

export default function() {
  var payload = JSON.stringify({
    'id':'fake_id',
    'name': 'xyz',
    'age': 5,
    'address': 'addressxyz'
  });

  var params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  var res = http.post('http://127.0.0.1:3000/patients', payload, params);
  //console.log("POST: " + JSON.stringify(res));
  var id = JSON.parse(res.body).id;
  //console.log("ID: " + id);


  res = http.get('http://127.0.0.1:3000/patients/' + id);
  //console.log("GET: " + JSON.stringify(res));


  payload = JSON.stringify({
    'id':id,
    'name': 'xyz_updated',
    'age': 10,
    'address': 'addressxyz_updated'
  });

  res = http.put('http://127.0.0.1:3000/patients/' + id, payload, params);
  //console.log("PUT: " + JSON.stringify(res));

  res = http.get('http://127.0.0.1:3000/patients/' + id);
  //console.log("GET: " + JSON.stringify(res));

  //res = http.get('http://127.0.0.1:3000/patients');
  //console.log("OPTIONS: " + JSON.stringify(res));

  res = http.get('http://127.0.0.1:3000/patients/' + id);
  //console.log("GET: " + JSON.stringify(res));

  res = http.del('http://127.0.0.1:3000/patients/' + id);
  //console.log("DELETE: " + JSON.stringify(res));

  // Should fail
  res = http.get('http://127.0.0.1:3000/patients/' + id);
  //console.log("GET: " + JSON.stringify(res));

  // Should fail
  res = http.put('http://127.0.0.1:3000/patients/' + id, payload, params);
  //console.log("PUT: " + JSON.stringify(res));

}
