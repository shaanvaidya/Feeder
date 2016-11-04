package com.example.abhishek.feeder25;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.toolbox.StringRequest;

import java.util.HashMap;
import java.util.Map;

public class LoginRequest extends StringRequest{

    private static final String Login_Request = "http://10.0.2.2:8025/studentlogin/";
    private Map<String, String> object;

    public LoginRequest(String ldap, String password, Response.Listener<String> listener) {
        super(Method.POST, Login_Request, listener, null);
        object = new HashMap<>();
//        object.put("secretkey", "MeraNaamJoker");
        object.put("LDAP", ldap);
        object.put("password", password);
    }

    public Map<String, String> getObject() {
        return object;
    }
}