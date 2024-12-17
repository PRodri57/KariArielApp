package Service;

import DAO.TurnoDAO;
import Model.Turno;
import java.util.Date;
import java.util.List;

public class TurnoServiceImpl implements TurnoService {
    private TurnoDAO turnoDAO;

    public TurnoServiceImpl(TurnoDAO turnoDAO) {
        this.turnoDAO = turnoDAO;
    }

    @Override
    public List<Turno> obtenerTurnosPorFechaYMedico(Date fecha, int medicoId) throws ServiceException {
        try {
            return turnoDAO.obtenerTurnosPorFechaYMedico(fecha, medicoId);
        } catch (Exception e) {
            throw new ServiceException("Error al obtener turnos por fecha y médico: " + e.getMessage());
        }
    }

    @Override
    public List<Turno> obtenerTurnosPorFecha(Date fecha) throws ServiceException {
        try {
            return turnoDAO.obtenerTurnosPorFecha(fecha);
        } catch (Exception e) {
            throw new ServiceException("Error al obtener turnos por fecha: " + e.getMessage());
        }
    }

    @Override
    public List<Turno> obtenerTurnosEntreFechas(int medicoId, Date fechaInicio, Date fechaFin) throws ServiceException {
        try {
            return turnoDAO.obtenerTurnosEntreFechas(medicoId, fechaInicio, fechaFin);
        } catch (Exception e) {
            throw new ServiceException("Error al obtener turnos entre fechas: " + e.getMessage());
        }
    }

    @Override
    public void agregarTurno(Turno turno) throws ServiceException {
        try {
            turnoDAO.agregar(turno);
        } catch (Exception e) {
            throw new ServiceException("Error al agregar turno: " + e.getMessage());
        }
    }

    @Override
    public void modificarTurno(Turno turno) throws ServiceException {
        try {
            turnoDAO.modificar(turno);
        } catch (Exception e) {
            throw new ServiceException("Error al modificar turno: " + e.getMessage());
        }
    }

    @Override
    public void eliminarTurno(int id) throws ServiceException {
        try {
            turnoDAO.eliminar(id);
        } catch (Exception e) {
            throw new ServiceException("Error al eliminar turno: " + e.getMessage());
        }
    }

    @Override
    public Turno obtenerPorId(int id) throws ServiceException {
        try {
            return turnoDAO.obtenerPorId(id);
        } catch (Exception e) {
            throw new ServiceException("Error al obtener turno: " + e.getMessage());
        }
    }

    @Override
    public List<Turno> obtenerTodos() throws ServiceException {
        try {
            return turnoDAO.obtenerTodos();
        } catch (Exception e) {
            throw new ServiceException("Error al obtener turnos: " + e.getMessage());
        }
    }

    @Override
    public List<Turno> obtenerTodosPorPaciente(int pacienteId) throws ServiceException {
        try {
            return turnoDAO.obtenerTodosPorPaciente(pacienteId);
        } catch (Exception e) {
            throw new ServiceException("Error al obtener turnos por paciente: " + e.getMessage());
        }
    }

    @Override
    public List<Turno> obtenerTodosPorMedico(int medicoId) throws ServiceException {
        try {
            return turnoDAO.obtenerTodosPorMedico(medicoId);
        } catch (Exception e) {
            throw new ServiceException("Error al obtener turnos por médico: " + e.getMessage());
        }
    }
} 