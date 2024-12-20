package com.tuempresa.gestorturnos.service.impl;

import com.tuempresa.gestorturnos.service.TurnoService;
import com.tuempresa.gestorturnos.dao.TurnoDAO;
import com.tuempresa.gestorturnos.model.Turno;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import javafx.application.Platform;
import com.tuempresa.gestorturnos.ui.CalendarioView;

public class TurnoServiceImpl implements TurnoService {
    private final TurnoDAO turnoDAO;

    public TurnoServiceImpl(TurnoDAO turnoDAO) {
        this.turnoDAO = turnoDAO;
    }

    @Override
    public void agendarTurno(Turno turno) {
        if (existeSuperposicion(turno)) {
            throw new RuntimeException("Ya existe un turno en ese horario");
        }
        turnoDAO.guardar(turno);
    }

    @Override
    public void eliminarTurno(String turnoId) {
        turnoDAO.eliminar(turnoId);
    }

    @Override
    public void confirmarTurno(String turnoId) {
        turnoDAO.buscarPorId(turnoId).ifPresent(turno -> {
            turno.setConfirmado(true);
            turnoDAO.actualizar(turno);
        });
    }

    @Override
    public List<Turno> obtenerTurnosPorFecha(LocalDate fecha) {
        return turnoDAO.buscarPorFecha(fecha, turnos -> {
            Platform.runLater(() -> {
                actualizarVistaCalendario(turnos);
            });
        });
    }

    private void actualizarVistaCalendario(List<Turno> turnos) {
        CalendarioView.getInstance().actualizarTurnos(turnos);
    }

    @Override
    public boolean existeSuperposicion(Turno nuevoTurno) {
        LocalDate fecha = nuevoTurno.getFecha().toLocalDate();
        List<Turno> turnosDelDia = turnoDAO.buscarPorFecha(fecha, turnos -> {
            // No necesitamos hacer nada con las actualizaciones aquí
        });
        
        return turnosDelDia.stream().anyMatch(turno -> {
            LocalDateTime inicio = turno.getFecha();
            LocalDateTime fin = inicio.plusMinutes(30); // Duración fija de 30 minutos
            
            LocalDateTime nuevoInicio = nuevoTurno.getFecha();
            LocalDateTime nuevoFin = nuevoInicio.plusMinutes(30);
            
            return !(nuevoFin.isBefore(inicio) || nuevoInicio.isAfter(fin));
        });
    }

    @Override
    public List<Turno> obtenerTodos() {
        return turnoDAO.obtenerTodos();
    }

    @Override
    public void actualizarTurno(Turno turno) {
        if (existeSuperposicion(turno)) {
            throw new RuntimeException("Ya existe un turno en ese horario");
        }
        turnoDAO.actualizar(turno);
    }
} 