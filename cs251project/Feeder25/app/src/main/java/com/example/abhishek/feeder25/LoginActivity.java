package com.example.abhishek.feeder25;

import android.content.Intent;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.VolleyLog;
import com.android.volley.toolbox.HttpHeaderParser;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.util.HashMap;
import java.util.Map;

import static android.R.attr.name;
import static java.net.HttpURLConnection.HTTP_OK;

public class LoginActivity extends AppCompatActivity implements View.OnClickListener{

    public static final String LOGIN_URL = "http://10.0.2.2:8025/studentlogin/";

    public static final String KEY_USERNAME="LDAP";
    public static final String KEY_PASSWORD="password";
    public static final String KEY_JSON="JSONSTRING";


    private EditText Username;
    private EditText Password;
    private Button Login;

    private String username;
    private String password;

    private String jsonString;

//    int mStatusCode;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        Username = (EditText) findViewById(R.id.UserName);
        Password = (EditText) findViewById(R.id.PassWord);
        Login = (Button) findViewById(R.id.Login);

        Login.setOnClickListener(LoginActivity.this);

    }


    private void userLogin() {
        username = Username.getText().toString().trim();
        password = Password.getText().toString().trim();

        StringRequest stringRequest = new StringRequest(Request.Method.POST, LOGIN_URL,
           new Response.Listener<String>() {
               @Override
                public void onResponse(String response) {
//                   try {
//                    System.out.println(response.length());
                       if(response.length(  )!=0) {
//                           JSONArray jsonObject = new JSONArray(response);
                               SaveSharedPreference.setUserName(LoginActivity.this,username);
                               jsonString = response;
                               openProfile();
                           }
                       else{
                           AlertDialog.Builder builder = new AlertDialog.Builder(LoginActivity.this);
                           builder.setMessage("Login Failed")
                                   .setNegativeButton("Retry", null)
                                   .create()
                                   .show();
                       }
//                   }
//                   catch (JSONException e) {
//                       e.printStackTrace();
//                   }
                }
           },
            new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Toast.makeText(LoginActivity.this,error.toString(),Toast.LENGTH_LONG ).show();
            }
            }){
            @Override
            protected Map<String, String> getParams() throws AuthFailureError {
                Map<String,String> map = new HashMap<String,String>();
                map.put(KEY_USERNAME,username);
                map.put(KEY_PASSWORD,password);
                return map;
                }
            @Override
            protected Response<String> parseNetworkResponse(NetworkResponse response) {
//                mStatusCode = response.statusCode;
                return super.parseNetworkResponse(response);
            }
        };
        RequestQueue requestQueue = Volley.newRequestQueue(this);
        requestQueue.add(stringRequest);
    }

    private void openProfile(){
        Intent intent = new Intent(this, MainActivity.class);
        intent.putExtra(KEY_USERNAME, username);
        intent.putExtra(KEY_PASSWORD, password);
        intent.putExtra(KEY_JSON, jsonString);

        startActivity(intent);
    }

    @Override
    public void onClick(View v) {
         userLogin();
    }
}
