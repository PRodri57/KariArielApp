package DAO;

import Model.Turno;
import Model.Medico;
import Model.Paciente;
import java.sql.*;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class TurnoDAOImpl implements TurnoDAO {
    private Connection conexion;
    private MedicoDAO medicoDAO;
    private PacienteDAO pacienteDAO;

    public TurnoDAOImpl(Connection conexion) {
        this.conexion = conexion;
        this.medicoDAO = new MedicoDAOImpl(conexion);
        this.pacienteDAO = new PacienteDAOImpl(conexion);
    }

    @Override
    public void agregar(Turno turno) throws Exception {
        // Primero verificamos si el médico ya tiene un turno en ese horario
        String checkMedicoSql = "SELECT COUNT(*) FROM turnos " +
                               "WHERE medico_id = ? AND fecha = ? AND hora = ?";
                             
        try (PreparedStatement checkMedicoStmt = conexion.prepareStatement(checkMedicoSql)) {
            checkMedicoStmt.setInt(1, turno.getMedicoId());
            checkMedicoStmt.setDate(2, new java.sql.Date(turno.getFecha().getTime()));
            checkMedicoStmt.setTime(3, new java.sql.Time(turno.getHora().getTime()));
            
            ResultSet rs = checkMedicoStmt.executeQuery();
            if (rs.next() && rs.getInt(1) > 0) {
                throw new Exception("El médico ya tiene un turno asignado en ese horario");
            }
        }

        // Luego verificamos si el consultorio está disponible
        String checkConsultorioSql = "SELECT COUNT(*) FROM turnos t " +
                                    "JOIN medicos m ON t.medico_id = m.id " +
                                    "WHERE m.consultorio = (SELECT consultorio FROM medicos WHERE id = ?) " +
                                    "AND t.fecha = ? AND t.hora = ?";
                             
        try (PreparedStatement checkConsultorioStmt = conexion.prepareStatement(checkConsultorioSql)) {
            checkConsultorioStmt.setInt(1, turno.getMedicoId());
            checkConsultorioStmt.setDate(2, new java.sql.Date(turno.getFecha().getTime()));
            checkConsultorioStmt.setTime(3, new java.sql.Time(turno.getHora().getTime()));
            
            ResultSet rs = checkConsultorioStmt.executeQuery();
            if (rs.next() && rs.getInt(1) > 0) {
                throw new Exception("El consultorio ya está ocupado en ese horario");
            }
        }

        // Si pasó todas las validaciones, procedemos con la inserción
        String sql = "INSERT INTO turnos (fecha, hora, medico_id, paciente_id, estado) VALUES (?, ?, ?, ?, ?)";
        try (PreparedStatement stmt = conexion.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            stmt.setDate(1, new java.sql.Date(turno.getFecha().getTime()));
            stmt.setTime(2, new java.sql.Time(turno.getHora().getTime()));
            stmt.setInt(3, turno.getMedicoId());
            stmt.setInt(4, turno.getPacienteId());
            stmt.setString(5, turno.getEstado());
            stmt.executeUpdate();

            ResultSet rs = stmt.getGeneratedKeys();
            if (rs.next()) {
                turno.setId(rs.getInt(1));
            }
        }
    }

    @Override
    public void modificar(Turno turno) throws Exception {
        String sql = "UPDATE turnos SET fecha = ?, hora = ?, medico_id = ?, paciente_id = ?, estado = ? WHERE id = ?";
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            stmt.setDate(1, new java.sql.Date(turno.getFecha().getTime()));
            stmt.setTime(2, new java.sql.Time(turno.getHora().getTime()));
            stmt.setInt(3, turno.getMedico().getId());
            stmt.setInt(4, turno.getPaciente().getId());
            stmt.setString(5, turno.getEstado());
            stmt.setInt(6, turno.getId());
            stmt.executeUpdate();
        }
    }

    @Override
    public void eliminar(int id) throws Exception {
        String sql = "DELETE FROM turnos WHERE id = ?";
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            stmt.setInt(1, id);
            stmt.executeUpdate();
        }
    }

    @Override
    public Turno obtenerPorId(int id) throws Exception {
        String sql = "SELECT * FROM turnos WHERE id = ?";
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            stmt.setInt(1, id);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                return crearTurnoDesdeResultSet(rs);
            }
            return null;
        }
    }

    @Override
    public List<Turno> obtenerTodosPorMedico(int medicoId) throws Exception {
        String sql = "SELECT * FROM turnos WHERE medico_id = ? ORDER BY fecha, hora";
        List<Turno> turnos = new ArrayList<>();
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            stmt.setInt(1, medicoId);
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                turnos.add(crearTurnoDesdeResultSet(rs));
            }
        }
        return turnos;
    }

    @Override
    public List<Turno> obtenerPorFechaYMedico(Date fecha, int medicoId) throws Exception {
        String sql = "SELECT * FROM turnos WHERE medico_id = ? AND fecha = ? ORDER BY hora";
        List<Turno> turnos = new ArrayList<>();
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            stmt.setInt(1, medicoId);
            stmt.setDate(2, new java.sql.Date(fecha.getTime()));
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                turnos.add(crearTurnoDesdeResultSet(rs));
            }
        }
        return turnos;
    }

    @Override
    public List<Turno> obtenerTodos() throws Exception {
        String sql = "SELECT * FROM turnos ORDER BY fecha, hora";
        List<Turno> turnos = new ArrayList<>();
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                turnos.add(crearTurnoDesdeResultSet(rs));
            }
        }
        return turnos;
    }

    @Override
    public List<Turno> obtenerTurnosEntreFechas(int medicoId, Date fechaInicio, Date fechaFin) throws Exception {
        String sql = "SELECT t.ID, t.FECHA, t.HORA, t.MEDICO_ID, t.PACIENTE_ID, t.ESTADO " +
                    "FROM TURNOS t " +
                    "WHERE t.MEDICO_ID = ? " +
                    "AND t.FECHA BETWEEN ? AND ?";
        
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            stmt.setInt(1, medicoId);
            stmt.setDate(2, new java.sql.Date(fechaInicio.getTime()));
            stmt.setDate(3, new java.sql.Date(fechaFin.getTime()));
            
            ResultSet rs = stmt.executeQuery();
            List<Turno> turnos = new ArrayList<>();
            
            while (rs.next()) {
                Turno turno = new Turno(
                    rs.getInt("ID"),
                    rs.getDate("FECHA"),
                    rs.getTime("HORA"),
                    medicoDAO.obtenerPorId(rs.getInt("MEDICO_ID")),
                    pacienteDAO.obtenerPacientePorId(rs.getInt("PACIENTE_ID")),
                    rs.getString("ESTADO")
                );
                turnos.add(turno);
            }
            
            return turnos;
        }
    }

    @Override
    public List<Turno> obtenerTodosPorPaciente(int pacienteId) throws Exception {
        String sql = "SELECT * FROM turnos WHERE paciente_id = ? ORDER BY fecha, hora";
        List<Turno> turnos = new ArrayList<>();
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            stmt.setInt(1, pacienteId);
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                turnos.add(crearTurnoDesdeResultSet(rs));
            }
        }
        return turnos;
    }

    @Override
    public List<Turno> obtenerTurnosPorFechaYMedico(Date fecha, int medicoId) throws Exception {
        String sql = "SELECT * FROM turnos WHERE CAST(fecha AS DATE) = ? AND medico_id = ? ORDER BY hora";
        List<Turno> turnos = new ArrayList<>();
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            stmt.setDate(1, new java.sql.Date(fecha.getTime()));
            stmt.setInt(2, medicoId);
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                turnos.add(crearTurnoDesdeResultSet(rs));
            }
        }
        return turnos;
    }

    @Override
    public List<Turno> obtenerTurnosPorFecha(Date fecha) throws Exception {
        String sql = "SELECT * FROM turnos WHERE CAST(fecha AS DATE) = ? ORDER BY hora";
        List<Turno> turnos = new ArrayList<>();
        try (PreparedStatement stmt = conexion.prepareStatement(sql)) {
            stmt.setDate(1, new java.sql.Date(fecha.getTime()));
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                turnos.add(crearTurnoDesdeResultSet(rs));
            }
        }
        return turnos;
    }

    private Turno crearTurnoDesdeResultSet(ResultSet rs) throws Exception {
        Medico medico = medicoDAO.obtenerPorId(rs.getInt("medico_id"));
        Paciente paciente = pacienteDAO.obtenerPacientePorId(rs.getInt("paciente_id"));
        
        return new Turno(
            rs.getInt("id"),
            rs.getDate("fecha"),
            rs.getTime("hora"),
            medico,
            paciente,
            rs.getString("estado")
        );
    }
} 