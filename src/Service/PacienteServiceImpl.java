package Service;

import DAO.DAOException;
import DAO.PacienteDAO;
import Model.Paciente;
import java.util.List;

public class PacienteServiceImpl implements PacienteService {
    private final PacienteDAO pacienteDAO;

    public PacienteServiceImpl(PacienteDAO pacienteDAO) {
        this.pacienteDAO = pacienteDAO;
    }

    @Override
    public void agregarPaciente(Paciente paciente) throws ServiceException {
        try {
            int nextId = obtenerSiguientePacientePorId();
            paciente.setId(nextId);
            pacienteDAO.agregar(paciente);
        } catch (DAOException e) {
            throw new ServiceException("Error agregando paciente", e);
        }
    }

    @Override
    public void modificarPaciente(Paciente paciente) throws ServiceException {
        try {
            pacienteDAO.modificar(paciente);
        } catch (DAOException e) {
            throw new ServiceException("Error modificando paciente", e);
        }
    }

    @Override
    public void eliminarPaciente(int id) throws ServiceException {
        try {
            pacienteDAO.eliminar(id);
        } catch (DAOException e) {
            throw new ServiceException("Error eliminando paciente", e);
        }
    }

    @Override
    public List<Paciente> obtenerTodos() throws ServiceException {
        try {
            return pacienteDAO.obtenerTodos();
        } catch (DAOException e) {
            throw new ServiceException("Error obteniendo pacientes", e);
        }
    }

    @Override
    public Paciente buscarPorEmail(String email) throws ServiceException {
        try {
            return pacienteDAO.buscarPorEmail(email);
        } catch (DAOException e) {
            throw new ServiceException("Error buscando paciente por email", e);
        }
    }

    @Override
    public int obtenerSiguientePacientePorId() throws ServiceException {
        try {
            List<Paciente> pacientes = pacienteDAO.obtenerTodos();
            int maxId = pacientes.stream().mapToInt(Paciente::getId).max().orElse(0);
            return maxId + 1;
        } catch (DAOException e) {
            throw new ServiceException("Error al obtener el siguiente ID", e);
        }
    }

    @Override
    public Paciente obtenerPacientePorId(int id) throws ServiceException {
        try {
            return pacienteDAO.obtenerPacientePorId(id);
        } catch (DAOException e) {
            throw new ServiceException("Error al obtener paciente por ID", e);
        }
    }
}
