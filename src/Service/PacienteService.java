package Service;

import Model.Paciente;
import java.util.List;

public interface PacienteService {
    void agregarPaciente(Paciente paciente) throws ServiceException;
    void modificarPaciente(Paciente paciente) throws ServiceException;
    void eliminarPaciente(int id) throws ServiceException;
    List<Paciente> obtenerTodos() throws ServiceException;
    Paciente buscarPorEmail(String email) throws ServiceException;
    int obtenerSiguientePacientePorId() throws ServiceException;
    Paciente obtenerPacientePorId(int id) throws ServiceException;
}
