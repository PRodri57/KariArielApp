package com.tuempresa.gestorturnos.model;

import java.time.LocalDateTime;

public class Turno {
    private String id;
    private LocalDateTime fecha;
    private boolean confirmado;

    // Constructor por defecto requerido por Firestore
    public Turno() {
        this.fecha = LocalDateTime.now(); // Valor por defecto
    }

    public String getId() {
        return id != null ? id : "";
    }

    public void setId(String id) {
        this.id = id;
    }

    public LocalDateTime getFecha() {
        return fecha != null ? fecha : LocalDateTime.now();
    }

    public void setFecha(LocalDateTime fecha) {
        this.fecha = fecha != null ? fecha : LocalDateTime.now();
    }

    public boolean isConfirmado() {
        return confirmado;
    }

    public void setConfirmado(boolean confirmado) {
        this.confirmado = confirmado;
    }
} 