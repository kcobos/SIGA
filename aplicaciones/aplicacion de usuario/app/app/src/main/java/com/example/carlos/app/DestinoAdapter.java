package com.example.carlos.app;

import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import java.text.DecimalFormat;
import java.util.List;

public class DestinoAdapter extends RecyclerView.Adapter<DestinoAdapter.MyViewHolder> {
    private List<Ubicacion> ubicaciones;

    public class MyViewHolder extends RecyclerView.ViewHolder {
        public TextView direccion, totales, libres, distancia;

        public MyViewHolder(View view) {
            super(view);
            direccion = (TextView) view.findViewById(R.id.direccion);
            totales = (TextView) view.findViewById(R.id.totales);
            libres = (TextView) view.findViewById(R.id.libres);
            distancia = (TextView) view.findViewById(R.id.distancia);
        }
    }

    class VHHeader extends RecyclerView.ViewHolder {
        public VHHeader(View itemView) {
            super(itemView);
        }
    }

    public DestinoAdapter(List<Ubicacion> ubicaciones) {
        this.ubicaciones = ubicaciones;
    }

    @Override
    public MyViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        return new MyViewHolder(LayoutInflater.from(parent.getContext())
                .inflate(R.layout.destino_fila, parent, false));
    }

    @Override
    public void onBindViewHolder(MyViewHolder holder, int position) {
        Ubicacion u = ubicaciones.get(position);
        holder.direccion.setText(u.getDireccion());
        holder.totales.setText(u.getPlazas_totales() + "");
        holder.libres.setText((u.getPlazas_totales()-u.getPlazas_ocupadas()) + "");
        holder.distancia.setText(new DecimalFormat("#.##").format(u.getDistancia()) + "m");
    }

    @Override
    public int getItemCount() {
        return ubicaciones.size();
    }
}
