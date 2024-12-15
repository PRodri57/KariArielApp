package UI;

import javax.swing.*;
import java.awt.*;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import DAO.MedicoDAOImpl;
import DAO.PacienteDAOImpl;
import DAO.TurnoDAOImpl;
import Service.MedicoServiceImpl;
import Service.PacienteServiceImpl;
import Service.TurnoService;
import Service.TurnoServiceImpl;

public class MainMenuUI {
    private JFrame mainFrame;
    private Connection conexion;
    private JPanel contentPanel;
    private CardLayout cardLayout;

    public MainMenuUI() {
        initConnection();
        initComponents();
    }

    private void initConnection() {
        try {
            conexion = DriverManager.getConnection("jdbc:h2:C:\\Users\\BashDeep\\OneDrive - Universidad de Palermo\\Universidad\\3° Cuatrimestre\\LABORATORIO I (Final pendiente)\\TPLabJavaGithub\\TPFinalLabJavaGithub\\database\\TurneraMedica", "sa", "");
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

        cardLayout = new CardLayout();
        contentPanel = new JPanel(cardLayout);

        JPanel mainPanel = new JPanel();
        mainPanel.setLayout(new GridBagLayout());
        mainPanel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

        GridBagConstraints gbc = new GridBagConstraints();
        gbc.gridwidth = GridBagConstraints.REMAINDER;
        gbc.fill = GridBagConstraints.HORIZONTAL;
        gbc.insets = new Insets(10, 10, 10, 10);

        // Título
        JLabel titleLabel = new JLabel("Sistema de Gestión Médica", SwingConstants.CENTER);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 24));
        gbc.gridx = 0;
        gbc.gridy = 0;
        mainPanel.add(titleLabel, gbc);

        // Botones
        JButton gestionPacientesButton = new JButton("Gestión de Pacientes");
        gestionPacientesButton.setFont(new Font("Arial", Font.PLAIN, 16));
        gestionPacientesButton.addActionListener(e -> abrirGestionPacientes());
        gbc.gridy = 1;
        mainPanel.add(gestionPacientesButton, gbc);

        JButton gestionMedicosButton = new JButton("Gestión de Médicos");
        gestionMedicosButton.setFont(new Font("Arial", Font.PLAIN, 16));
        gestionMedicosButton.addActionListener(e -> abrirGestionMedicos());
        gbc.gridy = 2;
        mainPanel.add(gestionMedicosButton, gbc);

        JButton gestionTurnosButton = new JButton("Gestión de Turnos");
        gestionTurnosButton.setFont(new Font("Arial", Font.PLAIN, 16));
        gestionTurnosButton.addActionListener(e -> abrirGestionTurnos());
        gbc.gridy = 3;
        mainPanel.add(gestionTurnosButton, gbc);

        JButton calendarioButton = new JButton("Calendario de Turnos");
        calendarioButton.setFont(new Font("Arial", Font.PLAIN, 16));
        calendarioButton.addActionListener(e -> abrirCalendario());
        gbc.gridy = 4;
        mainPanel.add(calendarioButton, gbc);

        // Botón de salir
        JButton salirButton = new JButton("Salir");
        salirButton.setFont(new Font("Arial", Font.PLAIN, 16));
        salirButton.addActionListener(e -> cerrarAplicacion());
        gbc.gridy = 5;
        mainPanel.add(salirButton, gbc);

        contentPanel.add(mainPanel, "menu");
        mainFrame.add(contentPanel);
        mainFrame.setVisible(true);
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
            CalendarioTurnosUI calendarioUI = new CalendarioTurnosUI(turnoService);
            contentPanel.add(calendarioUI, "calendario");
            cardLayout.show(contentPanel, "calendario");
        });
    }

    private void cerrarAplicacion() {
        try {
            if (conexion != null && !conexion.isClosed()) {
                conexion.close();
            }
        } catch (SQLException e) {
            System.err.println("Error al cerrar la conexión: " + e.getMessage());
        }
        mainFrame.dispose();
        System.exit(0);
    }

    public void mostrarMenuPrincipal() {
        cardLayout.show(contentPanel, "menu");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new MainMenuUI());
    }
} 