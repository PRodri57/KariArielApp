package Service;

import DAO.UsuarioDAO;
import Model.Usuario;

public class UsuarioServiceImpl implements UsuarioService {
    private UsuarioDAO usuarioDAO;

    public UsuarioServiceImpl(UsuarioDAO usuarioDAO) {
        this.usuarioDAO = usuarioDAO;
    }

    @Override
    public Usuario autenticar(String username, String password) throws ServiceException {
        try {
            return usuarioDAO.autenticar(username, password);
        } catch (Exception e) {
            throw new ServiceException("Error al autenticar usuario: " + e.getMessage());
        }
    }

    @Override
    public void agregar(Usuario usuario) throws ServiceException {
        try {
            usuarioDAO.agregar(usuario);
        } catch (Exception e) {
            throw new ServiceException("Error al agregar usuario: " + e.getMessage());
        }
    }

    @Override
    public void modificar(Usuario usuario) throws ServiceException {
        try {
            usuarioDAO.modificar(usuario);
        } catch (Exception e) {
            throw new ServiceException("Error al modificar usuario: " + e.getMessage());
        }
    }

    @Override
    public void eliminar(int id) throws ServiceException {
        try {
            usuarioDAO.eliminar(id);
        } catch (Exception e) {
            throw new ServiceException("Error al eliminar usuario: " + e.getMessage());
        }
    }

    @Override
    public Usuario obtenerPorId(int id) throws ServiceException {
        try {
            return usuarioDAO.obtenerPorId(id);
        } catch (Exception e) {
            throw new ServiceException("Error al obtener usuario: " + e.getMessage());
        }
    }

    @Override
    public Usuario obtenerPorMedicoId(int medicoId) throws ServiceException {
        try {
            return usuarioDAO.obtenerPorMedicoId(medicoId);
        } catch (Exception e) {
            throw new ServiceException("Error al obtener usuario por médico: " + e.getMessage());
        }
    }

    // ... implementar otros métodos del servicio ...
} 