package DAO;

import Model.*;

import java.util.List;

public interface PacienteDAO {
    void agregar(Paciente paciente) throws DAOException;
    void modificar(Paciente paciente) throws DAOException;
    void eliminar(int id) throws DAOException;
    List<Paciente> obtenerTodos() throws DAOException;
    Paciente buscarPorEmail(String email) throws DAOException;
    int obtenerSiguientePacientePorId() throws DAOException;
    Paciente obtenerPacientePorId(int id) throws DAOException;
}
