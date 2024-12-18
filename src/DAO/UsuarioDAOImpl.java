package DAO;

import Model.Usuario;
import java.sql.*;

public class UsuarioDAOImpl implements UsuarioDAO {
    private Connection conexion;

    public UsuarioDAOImpl(Connection conexion) {
        this.conexion = conexion;
    }

    @Override
    public Usuario autenticar(String username, String password) throws Exception {
        String sql = "SELECT * FROM usuarios WHERE username = ? AND password = ?";
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            stmt.setString(1, username);
            stmt.setString(2, password);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                return new Usuario(
                    rs.getInt("id"),
                    rs.getString("username"),
                    rs.getString("password"),
                    rs.getString("rol"),
                    rs.getObject("medico_id") != null ? rs.getInt("medico_id") : null,
                    rs.getObject("paciente_id") != null ? rs.getInt("paciente_id") : null  // Agregamos paciente_id
                );
            }
            return null;
        }
    }

    @Override
    public void agregar(Usuario usuario) throws Exception {
        String sql = "INSERT INTO usuarios (username, password, rol, medico_id) VALUES (?, ?, ?, ?)";
        try (PreparedStatement stmt = conexion.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            stmt.setString(1, usuario.getUsername());
            stmt.setString(2, usuario.getPassword());
            stmt.setString(3, usuario.getRol());
            if (usuario.getMedicoId() != null) {
                stmt.setInt(4, usuario.getMedicoId());
            } else {
                stmt.setNull(4, Types.INTEGER);
            }
            stmt.executeUpdate();
        }
    }

    @Override
    public void modificar(Usuario usuario) throws Exception {
        String sql = "UPDATE usuarios SET username = ?, password = ?, rol = ?, medico_id = ? WHERE id = ?";
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            stmt.setString(1, usuario.getUsername());
            stmt.setString(2, usuario.getPassword());
            stmt.setString(3, usuario.getRol());
            if (usuario.getMedicoId() != null) {
                stmt.setInt(4, usuario.getMedicoId());
            } else {
                stmt.setNull(4, Types.INTEGER);
            }
            stmt.setInt(5, usuario.getId());
            stmt.executeUpdate();
        }
    }

    @Override
    public void eliminar(int id) throws Exception {
        String sql = "DELETE FROM usuarios WHERE id = ?";
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            stmt.setInt(1, id);
            stmt.executeUpdate();
        }
    }

    @Override
    public Usuario obtenerPorId(int id) throws Exception {
        String sql = "SELECT * FROM usuarios WHERE id = ?";
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            stmt.setInt(1, id);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                return new Usuario(
                    rs.getInt("id"),
                    rs.getString("username"),
                    rs.getString("password"),
                    rs.getString("rol"),
                    rs.getObject("medico_id") != null ? rs.getInt("medico_id") : null,
                    rs.getObject("paciente_id") != null ? rs.getInt("paciente_id") : null  // Agregamos paciente_id
                );
            }
            return null;
        }
    }

    @Override
    public Usuario obtenerPorMedicoId(int medicoId) throws Exception {
        String sql = "SELECT * FROM usuarios WHERE medico_id = ?";
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            stmt.setInt(1, medicoId);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                return new Usuario(
                    rs.getInt("id"),
                    rs.getString("username"),
                    rs.getString("password"),
                    rs.getString("rol"),
                    rs.getInt("medico_id"),
                    rs.getInt("paciente_id")
                );
            }
            return null;
        }
    }

    // ... implementar otros métodos del DAO ...
} 