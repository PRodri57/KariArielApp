package com.tuempresa.gestorturnos.dao.impl;

import com.google.cloud.firestore.*;
import com.google.firebase.cloud.FirestoreClient;
import java.util.Optional;
import java.util.List;
import java.util.ArrayList;
import java.time.LocalDate;
import com.tuempresa.gestorturnos.model.Turno;
import com.tuempresa.gestorturnos.dao.TurnoDAO;
import com.google.api.core.ApiFuture;
import com.google.cloud.Timestamp;
import java.time.ZoneId;
import java.util.Date;
import com.tuempresa.gestorturnos.dao.TurnoListener;
import java.time.LocalDateTime;
import java.util.Map;

public class TurnoDAOImpl implements TurnoDAO {
    private final Firestore db;
    private ListenerRegistration listenerRegistration;

    public TurnoDAOImpl() {
        this.db = FirestoreClient.getFirestore();
    }

    @Override
    public void guardar(Turno turno) {
        try {
            DocumentReference docRef;
            if (turno.getId() == null || turno.getId().isEmpty()) {
                // Si no tiene ID, crear uno nuevo
                docRef = db.collection("turnos").document();
                turno.setId(docRef.getId());
            } else {
                // Si tiene ID, usar el existente
                docRef = db.collection("turnos").document(turno.getId());
            }
            
            ApiFuture<WriteResult> result = docRef.set(turno);
            result.get(); // Esperar a que se complete la operación
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException("Error al guardar el turno", e);
        }
    }

    @Override
    public Optional<Turno> buscarPorId(String id) {
        try {
            DocumentReference docRef = db.collection("turnos").document(id);
            DocumentSnapshot document = docRef.get().get();
            
            if (document.exists()) {
                return Optional.of(document.toObject(Turno.class));
            }
            return Optional.empty();
        } catch (Exception e) {
            throw new RuntimeException("Error al buscar el turno", e);
        }
    }

    @Override
    public List<Turno> buscarTodos() {
        try {
            List<Turno> turnos = new ArrayList<>();
            ApiFuture<QuerySnapshot> future = db.collection("turnos").get();
            QuerySnapshot documents = future.get();
            
            for (DocumentSnapshot document : documents) {
                turnos.add(document.toObject(Turno.class));
            }
            return turnos;
        } catch (Exception e) {
            throw new RuntimeException("Error al buscar todos los turnos", e);
        }
    }

    @Override
    public List<Turno> buscarPorFecha(LocalDate fecha, TurnoListener listener) {
        try {
            // Convertir LocalDate a Timestamp
            Timestamp inicioDelDia = Timestamp.of(Date.from(fecha.atStartOfDay(ZoneId.systemDefault()).toInstant()));
            Timestamp finDelDia = Timestamp.of(Date.from(fecha.atTime(23, 59, 59).atZone(ZoneId.systemDefault()).toInstant()));
            
            // Configurar el listener en tiempo real
            listenerRegistration = db.collection("turnos")
                .whereGreaterThanOrEqualTo("fechaHora", inicioDelDia)
                .whereLessThanOrEqualTo("fechaHora", finDelDia)
                .addSnapshotListener((snapshots, e) -> {
                    if (e != null) {
                        System.err.println("Error al escuchar cambios: " + e);
                        return;
                    }

                    if (snapshots == null) {
                        System.err.println("No hay snapshots disponibles");
                        return;
                    }

                    List<Turno> turnos = new ArrayList<>();
                    for (DocumentSnapshot document : snapshots.getDocuments()) {
                        Turno turno = document.toObject(Turno.class);
                        if (turno != null) {
                            turno.setId(document.getId());
                            turnos.add(turno);
                        }
                    }
                    
                    listener.onTurnosActualizados(turnos);
                });

            // Retornar la lista inicial
            ApiFuture<QuerySnapshot> future = db.collection("turnos")
                .whereGreaterThanOrEqualTo("fechaHora", inicioDelDia)
                .whereLessThanOrEqualTo("fechaHora", finDelDia)
                .get();
                
            List<Turno> turnosIniciales = new ArrayList<>();
            List<QueryDocumentSnapshot> documents = future.get().getDocuments();
            for (QueryDocumentSnapshot document : documents) {
                Turno turno = document.toObject(Turno.class);
                turno.setId(document.getId());
                turnosIniciales.add(turno);
            }
            
            return turnosIniciales;
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException("Error al buscar turnos por fecha", e);
        }
    }

    @Override
    public void actualizar(Turno turno) {
        try {
            DocumentReference docRef = db.collection("turnos").document(turno.getId());
            docRef.update(
                "fecha", turno.getFecha()
            ).get();
        } catch (Exception e) {
            throw new RuntimeException("Error al actualizar el turno", e);
        }
    }

    @Override
    public void eliminar(String id) {
        try {
            DocumentReference docRef = db.collection("turnos").document(id);
            docRef.delete().get();
        } catch (Exception e) {
            throw new RuntimeException("Error al eliminar el turno", e);
        }
    }

    // Método para detener la escucha cuando ya no sea necesaria
    public void detenerEscucha() {
        if (listenerRegistration != null) {
            listenerRegistration.remove();
        }
    }

    @Override
    public List<Turno> obtenerTodos() {
        try {
            List<Turno> turnos = new ArrayList<>();
            ApiFuture<QuerySnapshot> future = db.collection("turnos").get();
            QuerySnapshot documents = future.get();
            
            for (DocumentSnapshot document : documents) {
                Map<String, Object> data = document.getData();
                if (data != null && data.get("fecha") != null) {
                    Turno turno = new Turno();
                    turno.setId(document.getId());
                    
                    Object fechaObj = data.get("fecha");
                    if (fechaObj instanceof Timestamp) {
                        Timestamp timestamp = (Timestamp) fechaObj;
                        LocalDateTime fecha = LocalDateTime.ofInstant(
                            timestamp.toDate().toInstant(), 
                            ZoneId.systemDefault()
                        );
                        turno.setFecha(fecha);
                        turnos.add(turno);
                    }
                }
            }
            return turnos;
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException("Error al obtener todos los turnos: " + e.getMessage(), e);
        }
    }
} 