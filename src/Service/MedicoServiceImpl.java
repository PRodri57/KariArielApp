package Service;

import DAO.MedicoDAO;
import Model.Medico;
import java.sql.SQLException;
import java.util.List;

public class MedicoServiceImpl implements MedicoService {
    private MedicoDAO medicoDAO;

    public MedicoServiceImpl(MedicoDAO medicoDAO) {
        this.medicoDAO = medicoDAO;
    }

    @Override
    public void agregar(Medico medico) throws ServiceException {
        try {
            medicoDAO.agregar(medico);
        } catch (SQLException e) {
            throw new ServiceException("Error al agregar médico: " + e.getMessage());
        }
    }

    @Override
    public Medico buscarPorEmail(String email) throws ServiceException {
        try {
            return medicoDAO.buscarPorEmail(email);
        } catch (SQLException e) {
            throw new ServiceException("Error al buscar médico por email: " + e.getMessage());
        }
    }

    @Override
    public void eliminar(int id) throws ServiceException {
        try {
            medicoDAO.eliminar(id);
        } catch (SQLException e) {
            throw new ServiceException("Error al eliminar médico: " + e.getMessage());
        }
    }

    @Override
    public Medico obtenerPorId(int id) throws ServiceException {
        try {
            return medicoDAO.obtenerPorId(id);
        } catch (SQLException e) {
            throw new ServiceException("Error al obtener médico por ID: " + e.getMessage());
        }
    }

    @Override
    public List<Medico> obtenerTodos() throws ServiceException {
        try {
            return medicoDAO.obtenerTodos();
        } catch (SQLException e) {
            throw new ServiceException("Error al obtener lista de médicos: " + e.getMessage());
        }
    }

    @Override
    public void modificar(Medico medico) throws ServiceException {
        try {
            medicoDAO.modificar(medico);
        } catch (SQLException e) {
            throw new ServiceException("Error al modificar médico: " + e.getMessage());
        }
    }

} 