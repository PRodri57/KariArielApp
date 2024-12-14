package Service;

import Model.Medico;
import java.util.List;

public interface MedicoService {
    void agregar(Medico medico) throws ServiceException;
    void modificar(Medico medico) throws ServiceException;
    void eliminar(int id) throws ServiceException;
    Medico obtenerPorId(int id) throws ServiceException;
    List<Medico> obtenerTodos() throws ServiceException;
    Medico buscarPorEmail(String email) throws ServiceException;
} 