package Service;

import Model.Usuario;

public interface UsuarioService {
    Usuario autenticar(String username, String password) throws ServiceException;
    void agregar(Usuario usuario) throws ServiceException;
    void modificar(Usuario usuario) throws ServiceException;
    void eliminar(int id) throws ServiceException;
    Usuario obtenerPorId(int id) throws ServiceException;
    Usuario obtenerPorMedicoId(int medicoId) throws ServiceException;
} 