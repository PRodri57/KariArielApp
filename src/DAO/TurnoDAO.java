package DAO;

import Model.Turno;
import java.util.Date;
import java.util.List;

public interface TurnoDAO {
    void agregar(Turno turno) throws Exception;
    void modificar(Turno turno) throws Exception;
    void eliminar(int id) throws Exception;
    Turno obtenerPorId(int id) throws Exception;
    List<Turno> obtenerTodosPorMedico(int medicoId) throws Exception;
    List<Turno> obtenerPorFechaYMedico(Date fecha, int medicoId) throws Exception;
    List<Turno> obtenerTodos() throws Exception;
} 