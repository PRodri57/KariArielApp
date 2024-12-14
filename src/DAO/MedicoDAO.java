package DAO;

import Model.Medico;
import java.util.List;
import java.sql.SQLException;

public interface MedicoDAO {
    void agregar(Medico medico) throws SQLException;
    void modificar(Medico medico) throws SQLException;
    void eliminar(int id) throws SQLException;
    Medico obtenerPorId(int id) throws SQLException;
    List<Medico> obtenerTodos() throws SQLException;
    Medico buscarPorEmail(String email) throws SQLException;
} 