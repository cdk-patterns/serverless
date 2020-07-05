const AWS = require('aws-sdk');
AWS.config.update({region:'us-east-1'});
var client = new AWS.SecretsManager({
      region: 'us-east-1'
});
var mysql = require('mysql');
const fs = require('fs');

exports.handler = async function(event:any) {
  console.log("request:", JSON.stringify(event, undefined, 2));

  console.log(`Getting secret for ${process.env.RDS_SECRET_NAME}`);
  
  if(event.rawPath === '/favicon.ico'){
    return sendRes(404, 'no favicon here');
  }

  const secret = await client.getSecretValue({SecretId: process.env.RDS_SECRET_NAME}).promise();
  let {username, password} = JSON.parse(secret.SecretString);
  process.env.PROXY_ENDPOINT;
  
  var connection = mysql.createConnection({
    host     :  process.env.PROXY_ENDPOINT,
    user     :  username,
    password :  password,
    ssl  : {
      ca : fs.readFileSync(__dirname + '/AmazonRootCA1.pem')
    }
  });
  
  
  let queryResult = await new Promise( (resolve,reject) => {
    connection.query('CREATE DATABASE IF NOT EXISTS cdkpatterns', function (error:any, results:any, fields:any) {
      if (error) throw error;
      // connected!
      resolve('CREATE DATABASES query returned '+JSON.stringify(results));
    });
  }).catch((error)=>{
    return JSON.stringify(error);
  });
  
  connection.destroy();
  
  connection = mysql.createConnection({
    host     :  process.env.PROXY_ENDPOINT,
    user     :  username,
    password :  password,
    database: 'cdkpatterns',
    ssl  : {
      ca : fs.readFileSync(__dirname + '/AmazonRootCA1.pem')
    }
  });
  
  queryResult = await new Promise( (resolve,reject) => {
    connection.query('CREATE TABLE IF NOT EXISTS rds_proxy (id INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(20))', function (error:any, results:any, fields:any) {
      if (error) throw error;
      // connected!
      resolve('CREATE Table query returned '+JSON.stringify(results));
    });
  }).catch((error)=>{
    return JSON.stringify(error);
  });
  
  
  queryResult = await new Promise( (resolve,reject) => {
    connection.query(`INSERT INTO rds_proxy(url) VALUES ('${event.rawPath}')`, function (error:any, results:any, fields:any) {
      if (error) throw error;
      // connected!
      resolve('INSERT query returned '+JSON.stringify(results));
    });
  }).catch((error)=>{
    return JSON.stringify(error);
  });
  
  queryResult = await new Promise( (resolve,reject) => {
    connection.query(`SELECT * FROM rds_proxy`, function (error:any, results:any, fields:any) {
      if (error) throw error;
      // connected!
      let tableString = "<table><tr><th>ID</th><th>URL</th></tr>";
      for(let value of results) {
        tableString += `<tr><td>${value.id}</td><td>${value.url}</td></tr>`;
      }
      tableString += "</table>";
      
      resolve('All Current Data in rds_proxy Table (url is whatever url you hit on the HTTP API, try another random url like /hello) '+tableString);
    });
  }).catch((error)=>{
    return JSON.stringify(error);
  });
  
  connection.destroy();

  // return response back to upstream caller
  return sendRes(200, `You have connected with the RDS Proxy! <br /><br /> ${queryResult}`);
};

const sendRes = (status:number, body:string) => {
  var response = {
    statusCode: status,
    headers: {
      "Content-Type": "text/html"
    },
    body: body
  };
  return response;
};