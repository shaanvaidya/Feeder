package com.example.abhishek.feeder25;

import android.content.Intent;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.roomorama.caldroid.CaldroidFragment;
import com.roomorama.caldroid.CaldroidListener;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity implements View.OnClickListener{

    public static final String LOGIN_URL = "http://10.0.2.2:8025/studentlogin/";

    public static final String KEY_USERNAME="LDAP";
    public static final String KEY_PASSWORD="password";
    public static final String KEY_JSON="JSONSTRING";

    private Button Logout;
//    private LinearLayout Listing;
//    private Button Refresh;


    private String username;
    private String password;
    private String jsonString;
    private ArrayList<Deadline> dead = new ArrayList<Deadline>();
    private ArrayList<Feedback> feed = new ArrayList<Feedback>();
    private HashMap<String, Integer> cold = new HashMap<String, Integer>();
//    private ColorDrawable[] col={};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
//        SaveSharedPreference.clearUserName(MainActivity.this);

        if (SaveSharedPreference.getUserName(MainActivity.this).length() == 0) {
            Intent intent = new Intent(this, LoginActivity.class);
            startActivity(intent);
        } else {
//            Log.d("debug",SaveSharedPreference.getUserName(MainActivity.this));

            Intent intent = getIntent();
            username = intent.getStringExtra(KEY_USERNAME);
            password = intent.getStringExtra(KEY_PASSWORD);
            jsonString = intent.getStringExtra(KEY_JSON);

            Logout = (Button) findViewById(R.id.Logout);
//            Listing = (LinearLayout) findViewById(R.id.Listing);
//            Refresh = (Button) findViewById(R.id.Refresh);

            Logout.setOnClickListener(MainActivity.this);
//            Refresh.setOnClickListener(MainActivity.this);

            final EditText Name = (EditText) findViewById(R.id.NameUser);
            Name.setText(username);


            //implements a basic calendar using Calendar and Caldroid
            CaldroidFragment caldroidFragment = new CaldroidFragment();
            Bundle args = new Bundle();
            Calendar cal = Calendar.getInstance();
            args.putInt(CaldroidFragment.MONTH, cal.get(Calendar.MONTH) + 1);
            args.putInt(CaldroidFragment.YEAR, cal.get(Calendar.YEAR));
            caldroidFragment.setArguments(args);

            FragmentTransaction t = getSupportFragmentManager().beginTransaction();
            t.replace(R.id.calendar, caldroidFragment);
            t.commit();

            try {
                JSONArray outer = new JSONArray(jsonString);

                for (int i = 0; i < outer.length(); i++) {
                    JSONObject inner = outer.getJSONObject(i);
//                    Log.e("x", inner.toString());
                    String course = inner.getString("code");
//                    System.out.println(course);
                    String name = inner.getString("name");
                    try {
                        JSONArray deadline = inner.getJSONArray("deadline_set");
                        cold.put(course, i % 6);
                        Deadline d = new Deadline();
                        if(deadline.length()!=0){
                        for (int j = 0; j < deadline.length(); j++) {
                            JSONObject deadlines = deadline.getJSONObject(j);
                            d.topic = deadlines.getString("topic");
                            d.code = course;
                            d.name = name;

                            SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
                            Date date = new Date();
                            try {
                                date = format.parse(deadlines.getString("due_date"));
                            } catch (ParseException e) {
                                e.printStackTrace();
                            }

                            d.due_date = date;
                            d.description = deadlines.getString("description");
                            dead.add(d);
                        }}

                        JSONArray feedback_set = inner.getJSONArray("feedback_set");
                        Feedback f = new Feedback();
                        f.code = course;
                        f.name = name;
                        if(feedback_set.length()!=0){
                        for (int k = 0; k < feedback_set.length(); k++) {
                            JSONObject feedback_sets = feedback_set.getJSONObject(k);
                            f.topic = feedback_sets.getString("topic");

                            SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
                            Date date = new Date();
                            try {
                                date = format.parse(feedback_sets.getString("due_date"));
    //                            System.out.println("wlergjbewlf");
                            } catch (ParseException e) {
                                e.printStackTrace();
                            }

                            f.due_date = date;
                            JSONArray rating = feedback_sets.getJSONArray("ratingquestion_set");
                            f.rquestions = new ArrayList<String>();

                            for (int m = 0; m < rating.length(); m++) {
                                //                        try {
                                f.rquestions.add(rating.getJSONObject(m).getString("q"));
                                //                        }
                            }
                            JSONArray subjective = feedback_sets.getJSONArray("subjectivequestion_set");
                            f.squestions = new ArrayList<String>();
//                            System.out.println("there you are");

                            for (int m = 0; m < rating.length(); m++) {
                                f.squestions.add(subjective.getJSONObject(m).getString("q"));
                            }
                            feed.add(f);
//                            System.out.println("finally");

                        }}
                    } catch (JSONException xx) {
//                        System.out.println("got you");

                        xx.printStackTrace();
                    }

                }

            } catch (JSONException e) {
                e.printStackTrace();
            }

            ColorDrawable green = new ColorDrawable(Color.GREEN);

            for (int i = 0; i < dead.size(); i++) {
//                System
                switch (cold.get(dead.get(i).code)) {
                    case 0:
                        caldroidFragment.setBackgroundDrawableForDate(green, dead.get(i).due_date);
                        break;
                    case 1:
                        ColorDrawable aqua = new ColorDrawable(Color.CYAN);
                        caldroidFragment.setBackgroundDrawableForDate(aqua, dead.get(i).due_date);
                        break;
                    case 2:
                        ColorDrawable blue = new ColorDrawable(Color.BLUE);
                        caldroidFragment.setBackgroundDrawableForDate(blue, dead.get(i).due_date);
                        break;
                    case 3:
                        ColorDrawable red = new ColorDrawable(Color.RED);
                        caldroidFragment.setBackgroundDrawableForDate(red, dead.get(i).due_date);
                        break;
                    case 4:
                        ColorDrawable yellow = new ColorDrawable(Color.YELLOW);
                        caldroidFragment.setBackgroundDrawableForDate(yellow, dead.get(i).due_date);
                        break;
                    case 5:
                        ColorDrawable magenta = new ColorDrawable(Color.MAGENTA);
                        caldroidFragment.setBackgroundDrawableForDate(magenta, dead.get(i).due_date);
                        break;
                }
            }
            for (int i = 0; i < feed.size(); i++) {
                switch (cold.get(feed.get(i).code)) {
                    case 0:
                        caldroidFragment.setBackgroundDrawableForDate(green, feed.get(i).due_date);
                        break;
                    case 1:
                        ColorDrawable aqua = new ColorDrawable(Color.CYAN);
                        caldroidFragment.setBackgroundDrawableForDate(aqua, feed.get(i).due_date);
                        break;
                    case 2:
                        ColorDrawable blue = new ColorDrawable(Color.BLUE);
                        caldroidFragment.setBackgroundDrawableForDate(blue, feed.get(i).due_date);
                        break;
                    case 3:
                        ColorDrawable red = new ColorDrawable(Color.RED);
                        caldroidFragment.setBackgroundDrawableForDate(red, feed.get(i).due_date);
                        break;
                    case 4:
                        ColorDrawable yellow = new ColorDrawable(Color.YELLOW);
                        caldroidFragment.setBackgroundDrawableForDate(yellow, feed.get(i).due_date);
                        break;
                    case 5:
                        ColorDrawable magenta = new ColorDrawable(Color.MAGENTA);
                        caldroidFragment.setBackgroundDrawableForDate(magenta, feed.get(i).due_date);
                        break;
                }
            }

            final CaldroidListener listener = new CaldroidListener() {

                @Override
                public void onSelectDate(Date date, View view) {

                    LinearLayout Listing = (LinearLayout) findViewById(R.id.Listing);
                    Listing.removeAllViews();
                    Listing.setOrientation(LinearLayout.VERTICAL);

                    for (int i = 0; i < dead.size(); i++) {
                        System.out.println(dead.get(i).due_date);
//                        System.out.println(date);
                        if (dead.get(i).due_date.equals(date)) {
//                            System.out.println("Hey there");

                            Button btn1 = new Button(MainActivity.this);
                            SimpleDateFormat localDateFormat = new SimpleDateFormat("HH:mm:ss");
                            String time = localDateFormat.format(dead.get(i).due_date);
                            btn1.setText(dead.get(i).code + ":" + dead.get(i).topic + time);

                            Listing.addView(btn1);
//                            System.out.println("Hey there");
                        }
                    }

                }

                @Override
                public void onChangeMonth(int month, int year) {
                    String text = "month: " + month + " year: " + year;
                    //                Toast.makeText(getApplicationContext(), text,
                    //                        Toast.LENGTH_SHORT).show();
                }

                @Override
                public void onLongClickDate(Date date, View view) {
                    //                Toast.makeText(getApplicationContext(),
                    //                        "Long click " + formatter.format(date),
                    //                        Toast.LENGTH_SHORT).show();
                }

                @Override
                public void onCaldroidViewCreated() {
                    //                Toast.makeText(getApplicationContext(),
                    //                        "Caldroid view is created",
                    //                        Toast.LENGTH_SHORT).show();
                }

            };

            caldroidFragment.setCaldroidListener(listener);
        }
    }





    private void Refresh() {
        StringRequest stringRequest = new StringRequest(Request.Method.POST, LOGIN_URL,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        jsonString = response;
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(MainActivity.this,error.toString(),Toast.LENGTH_LONG ).show();
                    }
                }){
            @Override
            protected Map<String, String> getParams() throws AuthFailureError {
                Map<String,String> map = new HashMap<String,String>();
                map.put(KEY_USERNAME,username);
                map.put(KEY_PASSWORD,password);
                return map;
            }
        };
        RequestQueue requestQueue = Volley.newRequestQueue(this);
        requestQueue.add(stringRequest);
    }

//    private void openProfile(){
//        Intent intent = new Intent(this, MainActivity.class);
//        intent.putExtra(KEY_USERNAME, username);
//        startActivity(intent);
//    }

    private  void userLogout(){
        SaveSharedPreference.clearUserName(MainActivity.this);
        Intent intent = new Intent(this, LoginActivity.class);
        startActivity(intent);
    }

    @Override
    public void onClick(View v) {
        if(v == Logout) {
            userLogout();
        }
//        if(v == Refresh){
//            Refresh();
//        }
    }
}