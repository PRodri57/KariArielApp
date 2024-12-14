package DAO;

import Model.*;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class PacienteDAOImpl implements PacienteDAO {
    private Connection conexion;

    public PacienteDAOImpl(Connection conexion) {
        this.conexion = conexion;
    }

    @Override
    public void agregar(Paciente paciente) throws DAOException {
        String sql = "INSERT INTO Pacientes (nombreYApellido, dni, telefono, email, obraSocial) VALUES (?, ?, ?, ?, ?)";
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            System.out.println("Consulta SQL ejecutada: " + sql);
            stmt.setString(1, paciente.getNombreYApellido());
            stmt.setString(2, paciente.getDni());
            stmt.setString(3, paciente.getTelefono());
            stmt.setString(4, paciente.getEmail());
            stmt.setString(5, paciente.getObraSocial());
            stmt.executeUpdate();
        } catch (SQLException e) {
            System.err.println("Error SQL en PacienteDAOImpl.agregar: " + e.getMessage());
            throw new DAOException("Error agregando paciente", e);
        }
    }



    @Override
    public void modificar(Paciente paciente) throws DAOException {
        String sql = "UPDATE PACIENTES SET nombreYApellido = ?, dni = ?, telefono = ?, email = ?, obraSocial = ? WHERE id = ?";
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            System.out.println("Consulta SQL ejecutada: " + sql);
            stmt.setString(1, paciente.getNombreYApellido());
            stmt.setString(2, paciente.getDni());
            stmt.setString(3, paciente.getTelefono());
            stmt.setString(4, paciente.getEmail());
            stmt.setString(5, paciente.getObraSocial());
            stmt.setInt(6, paciente.getId());
            stmt.executeUpdate();
        } catch (SQLException e) {
            throw new DAOException("Error modificando paciente", e);
        }
    }

    @Override
    public void eliminar(int id) throws DAOException {
        String sql = "DELETE FROM PACIENTES WHERE id = ?";
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            System.out.println("Consulta SQL ejecutada: " + sql);
            stmt.setInt(1, id);
            stmt.executeUpdate();
        } catch (SQLException e) {
            throw new DAOException("Error eliminando paciente", e);
        }
    }

    @Override
    public List<Paciente> obtenerTodos() throws DAOException {
        String sql = "SELECT * FROM PACIENTES";
        List<Paciente> pacientes = new ArrayList<>();
        try (Statement stmt = conexion.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            System.out.println("Consulta SQL ejecutada: " + sql);
            while (rs.next()) {
                Paciente paciente = new Paciente(
                        rs.getString("NombreyApellido"),
                        rs.getString("dni"),
                        rs.getString("telefono"),
                        rs.getString("email"),
                        rs.getString("obraSocial")
                );
                paciente.setId(rs.getInt("id"));
                pacientes.add(paciente);
            }
        } catch (SQLException e) {
            System.err.println("Error SQL en PacienteDAOImpl.obtenerTodos(): " + e.getMessage());
            throw new DAOException("Error obteniendo pacientes", e);
        }
        return pacientes;
    }


    @Override
    public Paciente buscarPorEmail(String email) throws DAOException {
        String sql = "SELECT * FROM pacientes WHERE email = ?";
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            stmt.setString(1, email);
            ResultSet rs = stmt.executeQuery();
            
            if (rs.next()) {
                return new Paciente(
                    rs.getInt("id"),
                    rs.getString("nombreyapellido"),
                    rs.getString("dni"),
                    rs.getString("telefono"),
                    rs.getString("email"),
                    rs.getString("obrasocial")
                );
            }
            return null;
        } catch (SQLException e) {
            throw new DAOException("Error buscando paciente por email", e);
        }
    }

    @Override
    public int obtenerSiguientePacientePorId() throws DAOException {
        String sql = "SELECT id FROM PACIENTES ORDER BY id DESC LIMIT 1"; // Selecciona el último ID en la tabla
        try (PreparedStatement stmt = conexion.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            if (rs.next()) {
                return rs.getInt(1) + 1; // Devuelve el siguiente ID
            } else {
                return 1; // Si la tabla está vacía, el siguiente ID es 1
            }
        } catch (SQLException e) {
            throw new DAOException("Error al obtener el siguiente ID de paciente", e); // Captura y relanza la excepción SQLException como DAOException
        }
    }


    @Override
    public Paciente obtenerPacientePorId(int id) throws DAOException {
        String sql = "SELECT * FROM PACIENTES WHERE id = ?";
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            stmt.setInt(1, id);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return new Paciente(
                            rs.getString("nombreYApellido"),
                            rs.getString("dni"),
                            rs.getString("telefono"),
                            rs.getString("email"),
                            rs.getString("obraSocial")
                    );
                } else {
                    return null; // No se encontró el paciente
                }
            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }
}
