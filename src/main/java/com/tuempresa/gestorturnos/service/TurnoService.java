package com.tuempresa.gestorturnos.service;

import java.time.LocalDate;
import java.util.List;
import com.tuempresa.gestorturnos.model.Turno;

public interface TurnoService {
    void agendarTurno(Turno turno);
    void eliminarTurno(String turnoId);
    void confirmarTurno(String turnoId);
    void actualizarTurno(Turno turno);
    List<Turno> obtenerTurnosPorFecha(LocalDate fecha);
    boolean existeSuperposicion(Turno turno);
    List<Turno> obtenerTodos();
} 