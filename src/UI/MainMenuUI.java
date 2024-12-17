package UI;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionListener;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import DAO.MedicoDAOImpl;
import DAO.PacienteDAOImpl;
import DAO.TurnoDAOImpl;
import DAO.UsuarioDAOImpl;
import Service.MedicoService;
import Service.MedicoServiceImpl;
import Service.PacienteServiceImpl;
import Service.TurnoService;
import Service.TurnoServiceImpl;
import Service.UsuarioServiceImpl;
import Model.Usuario;

public class MainMenuUI {
    private JFrame mainFrame;
    private Connection conexion;
    private JPanel contentPanel;
    private CardLayout cardLayout;
    private Usuario usuarioActual;

    public MainMenuUI(Usuario usuario) {
        this.usuarioActual = usuario;
        initConnection();
        initComponents();
    }

    private void initConnection() {
        try {
            conexion = DriverManager.getConnection(
                "jdbc:h2:./database/TurneraMedica", 
                "sa", 
                ""
            );
        } catch (SQLException e) {
            JOptionPane.showMessageDialog(null, 
                "Error de conexión a la base de datos: " + e.getMessage(), 
                "Error", 
                JOptionPane.ERROR_MESSAGE);
            System.exit(1);
        }
    }

    private void initComponents() {
        mainFrame = new JFrame("Sistema de Gestión Médica");
        mainFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        mainFrame.setSize(800, 600);
        mainFrame.setLocationRelativeTo(null);

        cardLayout = new CardLayout();
        contentPanel = new JPanel(cardLayout);

        JPanel mainPanel = new JPanel();
        mainPanel.setLayout(new GridBagLayout());
        mainPanel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

        GridBagConstraints gbc = new GridBagConstraints();
        gbc.gridwidth = GridBagConstraints.REMAINDER;
        gbc.fill = GridBagConstraints.HORIZONTAL;
        gbc.insets = new Insets(10, 10, 10, 10);

        // Título con nombre de usuario y rol
        JLabel titleLabel = new JLabel("Sistema de Gestión Médica - " + 
            usuarioActual.getRol() + ": " + usuarioActual.getUsername(), 
            SwingConstants.CENTER);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 24));
        gbc.gridx = 0;
        gbc.gridy = 0;
        mainPanel.add(titleLabel, gbc);

        // Botones según rol
        if ("ADMIN".equals(usuarioActual.getRol())) {
            // Botones de administrador
            addButton(mainPanel, "Gestión de Pacientes", e -> abrirGestionPacientes(), gbc, 1);
            addButton(mainPanel, "Gestión de Médicos", e -> abrirGestionMedicos(), gbc, 2);
            addButton(mainPanel, "Gestión de Turnos", e -> abrirGestionTurnos(), gbc, 3);
            addButton(mainPanel, "Calendario de Turnos", e -> abrirCalendario(), gbc, 4);
            addButton(mainPanel, "Reportes Médicos", e -> abrirReportes(), gbc, 5);
        } else if ("MEDICO".equals(usuarioActual.getRol())) {
            // Botones de médico
            addButton(mainPanel, "Mis Turnos", e -> abrirMisTurnos(), gbc, 1);
            addButton(mainPanel, "Mi Reporte", e -> abrirMiReporte(), gbc, 2);
        }

        // Botón de cerrar sesión (común para ambos roles)
        addButton(mainPanel, "Cerrar Sesión", e -> cerrarSesion(), gbc, 6);

        contentPanel.add(mainPanel, "menu");
        mainFrame.add(contentPanel);
        mainFrame.setVisible(true);
    }

    private void addButton(JPanel panel, String text, ActionListener action, GridBagConstraints gbc, int y) {
        JButton button = new JButton(text);
        button.setFont(new Font("Arial", Font.PLAIN, 16));
        button.addActionListener(action);
        gbc.gridy = y;
        panel.add(button, gbc);
    }

    private void abrirGestionPacientes() {
        SwingUtilities.invokeLater(() -> {
            PacientePanelManager pacientePanel = new PacientePanelManager(this, conexion);
            contentPanel.add(pacientePanel.getMainPanel(), "pacientes");
            cardLayout.show(contentPanel, "pacientes");
        });
    }

    private void abrirGestionMedicos() {
        SwingUtilities.invokeLater(() -> {
            MedicoPanelManager medicoPanel = new MedicoPanelManager(this, conexion);
            contentPanel.add(medicoPanel.getMainPanel(), "medicos");
            cardLayout.show(contentPanel, "medicos");
        });
    }

    private void abrirGestionTurnos() {
        SwingUtilities.invokeLater(() -> {
            TurnoPanelManager turnoPanel = new TurnoPanelManager(this, conexion, 
                new MedicoServiceImpl(new MedicoDAOImpl(conexion)),
                new PacienteServiceImpl(new PacienteDAOImpl(conexion)));
            contentPanel.add(turnoPanel.getMainPanel(), "turnos");
            cardLayout.show(contentPanel, "turnos");
        });
    }

    private void abrirCalendario() {
        SwingUtilities.invokeLater(() -> {
            TurnoService turnoService = new TurnoServiceImpl(new TurnoDAOImpl(conexion));
            CalendarioTurnosUI calendarioUI = new CalendarioTurnosUI(turnoService, -1);
            contentPanel.add(calendarioUI, "calendario");
            cardLayout.show(contentPanel, "calendario");
        });
    }

    private void abrirReportes() {
        SwingUtilities.invokeLater(() -> {
            TurnoService turnoService = new TurnoServiceImpl(new TurnoDAOImpl(conexion));
            MedicoService medicoService = new MedicoServiceImpl(new MedicoDAOImpl(conexion));
            ConsultarReporteMedicoUI reporteUI = new ConsultarReporteMedicoUI(turnoService, medicoService, -1);
            contentPanel.add(reporteUI, "reportes");
            cardLayout.show(contentPanel, "reportes");
        });
    }

    private void abrirMisTurnos() {
        SwingUtilities.invokeLater(() -> {
            TurnoService turnoService = new TurnoServiceImpl(new TurnoDAOImpl(conexion));
            CalendarioTurnosUI calendarioUI = new CalendarioTurnosUI(turnoService, usuarioActual.getMedicoId());
            contentPanel.add(calendarioUI, "misTurnos");
            cardLayout.show(contentPanel, "misTurnos");
        });
    }

    private void abrirMiReporte() {
        SwingUtilities.invokeLater(() -> {
            TurnoService turnoService = new TurnoServiceImpl(new TurnoDAOImpl(conexion));
            MedicoService medicoService = new MedicoServiceImpl(new MedicoDAOImpl(conexion));
            ConsultarReporteMedicoUI reporteUI = new ConsultarReporteMedicoUI(
                turnoService, 
                medicoService, 
                usuarioActual.getMedicoId()
            );
            contentPanel.add(reporteUI, "miReporte");
            cardLayout.show(contentPanel, "miReporte");
        });
    }

    private void abrirMisTurnosPaciente() {
        SwingUtilities.invokeLater(() -> {
            TurnoService turnoService = new TurnoServiceImpl(new TurnoDAOImpl(conexion));
            TurnosPacienteUI turnosUI = new TurnosPacienteUI(turnoService, usuarioActual.getPacienteId());
            contentPanel.add(turnosUI, "misTurnosPaciente");
            cardLayout.show(contentPanel, "misTurnosPaciente");
        });
    }

    private void abrirSolicitarTurno() {
        SwingUtilities.invokeLater(() -> {
            TurnoService turnoService = new TurnoServiceImpl(new TurnoDAOImpl(conexion));
            MedicoService medicoService = new MedicoServiceImpl(new MedicoDAOImpl(conexion));
            SolicitarTurnoUI solicitarTurnoUI = new SolicitarTurnoUI(
                turnoService, 
                medicoService, 
                usuarioActual.getPacienteId()
            );
            contentPanel.add(solicitarTurnoUI, "solicitarTurno");
            cardLayout.show(contentPanel, "solicitarTurno");
        });
    }

    private void cerrarSesion() {
        try {
            if (conexion != null && !conexion.isClosed()) {
                conexion.close();
            }
            mainFrame.dispose();
            SwingUtilities.invokeLater(() -> {
                try {
                    Connection nuevaConexion = DriverManager.getConnection(
                        "jdbc:h2:./database/TurneraMedica", 
                        "sa", 
                        ""
                    );
                    new LoginUI(new UsuarioServiceImpl(new UsuarioDAOImpl(nuevaConexion))).setVisible(true);
                } catch (SQLException e) {
                    JOptionPane.showMessageDialog(null, 
                        "Error al reconectar: " + e.getMessage(), 
                        "Error", 
                        JOptionPane.ERROR_MESSAGE);
                }
            });
        } catch (SQLException e) {
            JOptionPane.showMessageDialog(null, 
                "Error al cerrar sesión: " + e.getMessage(), 
                "Error", 
                JOptionPane.ERROR_MESSAGE);
        }
    }

    public void mostrarMenuPrincipal() {
        cardLayout.show(contentPanel, "menu");
    }

} 