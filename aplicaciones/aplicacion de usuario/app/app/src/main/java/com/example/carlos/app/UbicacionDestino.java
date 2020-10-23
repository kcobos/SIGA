package com.example.carlos.app;

import android.content.Intent;
import android.net.Uri;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.firebase.iid.FirebaseInstanceId;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class UbicacionDestino extends AppCompatActivity {
    private static final String TAG = "Ubicacion destino";
    private int id;
    private RequestQueue requestQueue;
    private TextView direccion, plazas_totales, plazas_disponibles, observaciones;
    private Button ir;
    private double latitud, longitud;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ubicacion_destino);

        Intent i = getIntent();
        id = i.getIntExtra("id", 0);

        requestQueue = Volley.newRequestQueue(this);

        direccion = (TextView)findViewById(R.id.direccion);
        plazas_totales = (TextView)findViewById(R.id.plazas_totales);
        plazas_disponibles = (TextView)findViewById(R.id.plazas_disponibles);
        observaciones = (TextView)findViewById(R.id.observaciones);

        ir = (Button) findViewById(R.id.bt_ir);
        ir.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Uri gmmIntentUri = Uri.parse("google.navigation:q="+
                        latitud+","+longitud+"&mode=d");
                Intent mapIntent = new Intent(Intent.ACTION_VIEW, gmmIntentUri);
                mapIntent.setPackage("com.google.android.apps.maps");
//                Log.i("Firebase", "token "+ FirebaseInstanceId.getInstance().getToken());
                App.navegando = true;
                addDestinoActivo(id);
//                startActivityForResult(mapIntent, App.GOOGLE_NAV);
                startActivity(mapIntent);
                eliminarDestinoActivo();
//                App.navegando = false;
//                startActivity(mapIntent);
            }
        });

//        Toast.makeText(getApplicationContext(),
//                "id:" + id, Toast.LENGTH_LONG)
//                .show();
        getUbicacion();
    }

    @Override
    protected void onResume() {
        super.onResume();
        eliminarDestinoActivo();
    }

    private void getUbicacion() {
        final String url = getString(R.string.url_servidor)+"ubicacion/"+id;
        // To fully understand this, I'd recommend readng the office docs: https://developer.android.com/training/volley/index.html
        final JsonObjectRequest req = new JsonObjectRequest(Request.Method.GET, url,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        Log.i(TAG, "ubicaciones: " + response.toString());

                        try {
                            int id_nuevo = response.getInt("id");
                            if (id == id_nuevo){
                                direccion.setText(response.getString("direccion"));
                                plazas_totales.setText(response.getInt("plazas_totales")+"");
                                plazas_disponibles.setText(
                                        (response.getInt("plazas_totales")-response.getInt("plazas_ocupadas"))+"");
                                observaciones.setText(response.getString("observaciones"));
                                latitud = response.getDouble("latitud");
                                longitud = response.getDouble("longitud");
                            }
                        } catch (JSONException e) {
                            Log.e(TAG, "Casting JSON " + e.toString());
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // If there a HTTP error then add a note to our repo list.
                        Log.e("Volley", error.toString());
                    }
                }
        );

        // Add the request we just defined to our request queue.
        // The request queue will automatically handle the request as soon as it can.
        requestQueue.add(req);
    }

    private void addDestinoActivo(int id_ubicacion) {
        final String url = getString(R.string.url_servidor)+"destino_activo/nueva";
        final JSONObject json = new JSONObject();
        try {
            json.put("id_ubicacion", id_ubicacion);
            json.put("token", FirebaseInstanceId.getInstance().getToken());
        } catch (JSONException e) {
            e.printStackTrace();
        }

        // To fully understand this, I'd recommend readng the office docs: https://developer.android.com/training/volley/index.html

        final JsonObjectRequest req = new JsonObjectRequest(Request.Method.POST, url, json,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        Log.i(TAG, "alta destino activo: "+ response.toString());
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // If there a HTTP error then add a note to our repo list.
                        Log.e("Volley", error.toString());
                    }
                }
        );

        // Add the request we just defined to our request queue.
        // The request queue will automatically handle the request as soon as it can.
        requestQueue.add(req);
    }
    private void eliminarDestinoActivo() {
        final String url = getString(R.string.url_servidor)+"destino_activo/"+FirebaseInstanceId.getInstance().getToken();

        // To fully understand this, I'd recommend readng the office docs: https://developer.android.com/training/volley/index.html

        final JsonObjectRequest req = new JsonObjectRequest(Request.Method.DELETE, url,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        Log.i(TAG, "eliminar destino activo: "+ response.toString());
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // If there a HTTP error then add a note to our repo list.
                        Log.e("Volley", error.toString());
                    }
                }
        );

        // Add the request we just defined to our request queue.
        // The request queue will automatically handle the request as soon as it can.
        requestQueue.add(req);
    }
}
