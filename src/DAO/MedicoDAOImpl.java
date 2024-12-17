package DAO;

import Model.Medico;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class MedicoDAOImpl implements MedicoDAO {
    private Connection conexion;

    public MedicoDAOImpl(Connection conexion) {
        this.conexion = conexion;
    }

    @Override
    public void agregar(Medico medico) throws SQLException {
        String sql = "INSERT INTO medicos (nombre_y_apellido, dni, telefono, email, especialidad, valor_consulta) VALUES (?, ?, ?, ?, ?, ?)";
        try (PreparedStatement stmt = conexion.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            stmt.setString(1, medico.getNombreYApellido());
            stmt.setString(2, medico.getDni());
            stmt.setString(3, medico.getTelefono());
            stmt.setString(4, medico.getEmail());
            stmt.setString(5, medico.getEspecialidad());
            stmt.setDouble(6, medico.getValorConsulta());
            stmt.executeUpdate();
        } catch (SQLException e) {
            System.err.println("Error SQL en MedicoDAOImpl.agregar: " + e.getMessage());
            throw new SQLException("Error agregando medico", e);
        }
    }

    @Override
    public Medico buscarPorEmail(String email) throws SQLException {
        String sql = "SELECT * FROM medicos WHERE email = ?";
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            stmt.setString(1, email);
            ResultSet rs = stmt.executeQuery();
            
            if (rs.next()) {
                return new Medico(
                    rs.getInt("id"),
                    rs.getString("nombre_y_apellido"),
                    rs.getString("dni"),
                    rs.getString("telefono"),
                    rs.getString("email"),
                    rs.getString("especialidad"),
                    rs.getDouble("valor_consulta")
                );
            }
            return null;
        }
    }

    @Override
    public void eliminar(int id) throws SQLException {
        String sql = "DELETE FROM medicos WHERE id = ?";
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            stmt.setInt(1, id);
            stmt.executeUpdate();
        }
    }

    @Override
    public Medico obtenerPorId(int id) throws SQLException {
        String sql = "SELECT * FROM medicos WHERE id = ?";
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            stmt.setInt(1, id);
            ResultSet rs = stmt.executeQuery();
            
            if (rs.next()) {
                return new Medico(
                    rs.getInt("id"),
                    rs.getString("nombre_y_apellido"),
                    rs.getString("dni"),
                    rs.getString("telefono"),
                    rs.getString("email"),
                    rs.getString("especialidad"),
                    rs.getDouble("valor_consulta")
                );
            }
            return null;
        }
    }

    @Override
    public List<Medico> obtenerTodos() throws SQLException {
        List<Medico> medicos = new ArrayList<>();
        String sql = "SELECT * FROM medicos";
        try (PreparedStatement stmt = conexion.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            
            while (rs.next()) {
                medicos.add(new Medico(
                    rs.getInt("id"),
                    rs.getString("nombre_y_apellido"),
                    rs.getString("dni"),
                    rs.getString("telefono"),
                    rs.getString("email"),
                    rs.getString("especialidad"),
                    rs.getDouble("valor_consulta")
                ));
            }
            return medicos;
        }
    }

    @Override
    public void modificar(Medico medico) throws SQLException {
        String sql = "UPDATE medicos SET nombre_y_apellido = ?, dni = ?, telefono = ?, email = ?, especialidad = ?, matricula = ? WHERE id = ?";
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            stmt.setString(1, medico.getNombreYApellido());
            stmt.setString(2, medico.getDni());
            stmt.setString(3, medico.getTelefono());
            stmt.setString(4, medico.getEmail());
            stmt.setString(5, medico.getEspecialidad());
            stmt.setDouble(6, medico.getValorConsulta());
            stmt.setInt(7, medico.getId());
            stmt.executeUpdate();
        }
    }

    // Implementar los demás métodos de manera similar a PacienteDAOImpl
} 