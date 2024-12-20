package com.tuempresa.gestorturnos.dao;

import java.util.List;
import java.util.Optional;
import java.time.LocalDate;
import com.tuempresa.gestorturnos.model.Turno;

public interface TurnoDAO {
    void guardar(Turno turno);
    Optional<Turno> buscarPorId(String id);
    List<Turno> buscarTodos();
    List<Turno> buscarPorFecha(LocalDate fecha, TurnoListener listener);
    void actualizar(Turno turno);
    void eliminar(String id);
    List<Turno> obtenerTodos();
} 