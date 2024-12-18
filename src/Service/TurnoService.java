package Service;

import Model.Turno;
import java.util.Date;
import java.util.List;

public interface TurnoService {
    List<Turno> obtenerTurnosPorFechaYMedico(Date fecha, int medicoId) throws ServiceException;
    void agregarTurno(Turno turno) throws ServiceException;
    void modificarTurno(Turno turno) throws ServiceException;
    void eliminarTurno(int id) throws ServiceException;
    List<Turno> obtenerTodosPorMedico(int medicoId) throws ServiceException;
    Turno obtenerPorId(int id) throws ServiceException;
    List<Turno> obtenerTodos() throws ServiceException;
    List<Turno> obtenerTurnosEntreFechas(int medicoId, Date fechaInicio, Date fechaFin) throws ServiceException;
    List<Turno> obtenerTurnosPorPaciente(int pacienteId) throws ServiceException;
    List<Turno> obtenerTurnosPorFecha(Date fecha) throws ServiceException;
} 