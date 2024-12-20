package com.tuempresa.gestorturnos.dao;

import java.util.List;
import com.tuempresa.gestorturnos.model.Turno;

public interface TurnoListener {
    void onTurnosActualizados(List<Turno> turnos);
} 