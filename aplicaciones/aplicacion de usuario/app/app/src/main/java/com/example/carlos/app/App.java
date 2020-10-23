package com.example.carlos.app;

import android.Manifest;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.location.Location;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.FragmentActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.LatLngBounds;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.iid.FirebaseInstanceId;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

public class App extends FragmentActivity implements OnMapReadyCallback,
//        GoogleMap.OnCameraMoveStartedListener,
//        GoogleMap.OnCameraMoveListener,
//        GoogleMap.OnCameraMoveCanceledListener,
        GoogleMap.OnCameraIdleListener, GoogleMap.OnMarkerClickListener, GoogleMap.OnMapClickListener {

    public static final int GOOGLE_NAV = 5;
    public static boolean navegando = false;
    private GoogleMap mMap;
    private FusedLocationProviderClient mFusedLocationClient;
    private static final String TAG = "APP";
    private static LatLngBounds bounds;
    private RequestQueue requestQueue;
    private ArrayList<Ubicacion> ubicaciones;
    private Marker destino;
    private static boolean destino_activado;
    private static boolean destino_clickado;
    private BroadcastReceiver mReceiver;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestQueue = Volley.newRequestQueue(this);
        ubicaciones = new ArrayList<>();
        destino_activado = false;
        destino_clickado = false;


//        Toast.makeText(this, "On Create",
//                Toast.LENGTH_LONG).show();

        Log.i("Firebase", "token "+ FirebaseInstanceId.getInstance().getToken());
//        Log.i(TAG, "navegando " + navegando);
        setContentView(R.layout.activity_app);
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
        mFusedLocationClient = LocationServices.getFusedLocationProviderClient(this);

        IntentFilter filter = new IntentFilter();
        filter.addAction("close_app");
        registerReceiver(mReceiver, filter);

        mReceiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                Log.d("TAG" ,"onReceive ");
                finish();
            }
        };
    }

    @Override
    protected void onResume() {
        super.onResume();
//        Toast.makeText(this, "On Resume",
//                Toast.LENGTH_LONG).show();
//        Toast.makeText(this, "Navegando = "+navegando,
//                Toast.LENGTH_LONG).show();
        if (navegando){
            finishActivity(App.GOOGLE_NAV);
            navegando = false;
        }
        if(mMap != null)
            onMapReady(mMap);

        eliminarDestinoActivo();
    }

    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            Log.e(TAG, "No hay permiso de GPS");
            Toast.makeText(this, "No hay permiso de GPS",
                    Toast.LENGTH_LONG).show();
            return;
        }
        mFusedLocationClient.getLastLocation()
                .addOnSuccessListener(this, new OnSuccessListener<Location>() {
                    @Override
                    public void onSuccess(Location location) {
                        // Got last known location. In some rare situations this can be null.
                        if (location != null) {
                            Log.i(TAG, "Location: latitud=" + location.getLatitude() + " longitud=" + location.getLongitude());
                            LatLng point = new LatLng(location.getLatitude(), location.getLongitude());
                            mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(point, 15));
                            mMap.animateCamera(CameraUpdateFactory.zoomTo(15));
                            if (ActivityCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED &&
                                    ActivityCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
                                Log.e(TAG, "No hay permiso de localización");
                                Toast.makeText(getApplicationContext(), "No hay permiso de localización",
                                        Toast.LENGTH_LONG).show();
                                return;
                            }
                            mMap.setMyLocationEnabled(true);
                            App.bounds = mMap.getProjection().getVisibleRegion().latLngBounds;
                            getUbicaciones();
                        }
                    }
                });
        // Add a marker in Sydney and move the camera
//        LatLng sydney = new LatLng(-34, 151);
//        mMap.addMarker(new MarkerOptions().position(sydney).title("Marker in Sydney"));
//        mMap.moveCamera(CameraUpdateFactory.newLatLng(sydney));

        mMap.setOnCameraIdleListener(this);
        mMap.setOnMarkerClickListener(this);
        mMap.setOnMapClickListener(this);
        mMap.setOnInfoWindowClickListener(new GoogleMap.OnInfoWindowClickListener() {
            @Override
            public void onInfoWindowClick(Marker marker) {
                marker.hideInfoWindow();
            }
        });
//        mMap.setOnCameraMoveStartedListener(this);
//        mMap.setOnCameraMoveListener(this);
//        mMap.setOnCameraMoveCanceledListener(this);
    }

//    @Override
//    public void onCameraMoveStarted(int reason) {
//
//        if (reason == GoogleMap.OnCameraMoveStartedListener.REASON_GESTURE) {
//            Toast.makeText(this, "The user gestured on the map.",
//                    Toast.LENGTH_SHORT).show();
//        } else if (reason == GoogleMap.OnCameraMoveStartedListener
//                .REASON_API_ANIMATION) {
//            Toast.makeText(this, "The user tapped something on the map.",
//                    Toast.LENGTH_SHORT).show();
//        } else if (reason == GoogleMap.OnCameraMoveStartedListener
//                .REASON_DEVELOPER_ANIMATION) {
//            Toast.makeText(this, "The app moved the camera.",
//                    Toast.LENGTH_SHORT).show();
//        }
//    }
//
//    @Override
//    public void onCameraMove() {
//        Toast.makeText(this, "The camera is moving.",
//                Toast.LENGTH_SHORT).show();
//    }
//
//    @Override
//    public void onCameraMoveCanceled() {
//        Toast.makeText(this, "Camera movement canceled.",
//                Toast.LENGTH_SHORT).show();
//    }


    @Override
    public void onCameraIdle() {
        if (!destino_activado && !destino_clickado) {
//            Toast.makeText(this, "The camera has stopped moving.",
//                    Toast.LENGTH_SHORT).show();
            App.bounds = mMap.getProjection().getVisibleRegion().latLngBounds;
            getUbicaciones();
        }
        if (!destino_clickado) {
            if (destino != null)
                destino.remove();
        }
        destino_activado = false;
        destino_clickado = false;
    }

    @Override
    public boolean onMarkerClick(Marker marker) {
//        Toast.makeText(this, "Marker click "+marker.getTitle(),
//                Toast.LENGTH_SHORT).show();
        if (marker.equals(destino)) {
            AddDestinoUsuario(marker.getPosition().latitude, marker.getPosition().longitude);
            Intent i = new Intent(this, SeleccionarDestino.class);
            i.putExtra("latitud", marker.getPosition().latitude);
            i.putExtra("longitud", marker.getPosition().longitude);
            startActivity(i);
            destino.remove();
            destino_activado = false;
        } else {
            int id = Integer.parseInt(marker.getSnippet());
//            Toast.makeText(this, "ubicación " + id,
//                    Toast.LENGTH_SHORT).show();
            Intent i = new Intent(this, UbicacionDestino.class);
            i.putExtra("id", id);
            startActivity(i);
        }
        destino_clickado = true;
        return false;
    }

    @Override
    public void onMapClick(LatLng latLng) {
        if (!destino_activado) {
            destino = mMap.addMarker(
                    new MarkerOptions()
                            .position(latLng)
                            .title("Destino")
//                        .icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_BLUE))
            );
            destino_activado = true;
        }
    }

    private void getUbicaciones() {
        // /ubicaciones/{lat_min}&{lat_max}/{long_min}&{long_max}
        final String url = getString(R.string.url_servidor)+"ubicaciones/" +
                App.bounds.northeast.latitude + "&" + App.bounds.southwest.latitude + "/" +
                App.bounds.northeast.longitude + "&" + App.bounds.southwest.longitude;
        // To fully understand this, I'd recommend readng the office docs: https://developer.android.com/training/volley/index.html
        final JsonObjectRequest req = new JsonObjectRequest(Request.Method.GET, url,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        Log.i(TAG, "ubicaciones: " + response.toString());

                        try {
                            int num_ubicaciones = response.getInt("num_ubicaciones");
                            if (num_ubicaciones != 0) {
                                JSONArray lista = response.getJSONArray("ubicaciones");
                                ubicaciones.clear();
                                for (int i = 0; i < num_ubicaciones; i++) {
                                    JSONObject u = lista.getJSONObject(i);
                                    ubicaciones.add(new Ubicacion(
                                            u.getInt("id"),
                                            u.getString("direccion"),
                                            u.getDouble("latitud"),
                                            u.getDouble("longitud"),
                                            u.getInt("plazas_totales"),
                                            u.getInt("plazas_ocupadas"),
                                            u.getString("observaciones")
                                    ));
                                }
                                pintaUbicaciones();
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

    public void pintaUbicaciones() {
        mMap.clear();
        if (ubicaciones.size() != 0) {
            for (Ubicacion u : ubicaciones) {
                LatLng point = new LatLng(u.getLatitud(), u.getLongitud());
                mMap.addMarker(
                        new MarkerOptions()
                                .position(point)
                                .snippet(u.getId()+"")
//                                .icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_BLUE))
                        .icon(BitmapDescriptorFactory.fromResource(R.drawable.marker))
                );
            }
        }
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

    private void AddDestinoUsuario(double latitud, double longitud) {
        final String url = getString(R.string.url_servidor)+"destinos_usuario/"+latitud+"&"+longitud;

        // To fully understand this, I'd recommend readng the office docs: https://developer.android.com/training/volley/index.html

        final JsonObjectRequest req = new JsonObjectRequest(Request.Method.PUT, url,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        Log.i(TAG, "añadir destino usuario: "+ response.toString());
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
