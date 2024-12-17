package DAO;

import Model.Usuario;

public interface UsuarioDAO {
    Usuario autenticar(String username, String password) throws Exception;
    void agregar(Usuario usuario) throws Exception;
    void modificar(Usuario usuario) throws Exception;
    void eliminar(int id) throws Exception;
    Usuario obtenerPorId(int id) throws Exception;
    Usuario obtenerPorMedicoId(int medicoId) throws Exception;
} 