package UI;

import DAO.PacienteDAOImpl;
import Model.Medico;
import Model.Paciente;
import Service.PacienteService;
import Service.PacienteServiceImpl;
import Service.ServiceException;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.sql.Connection;

public class PacientePanelManager {
    private JFrame mainFrame;
    private CardLayout cardLayout;
    private JPanel contentPanel;
    private JTable table;
    private DefaultTableModel tableModel;
    private PacienteService pacienteService;
    private Connection conexion;

    private AgregarPacienteUI agregarPacienteUI;
    private ModificarPacienteUI modificarPacienteUI;
    private EliminarPacienteUI eliminarPacienteUI;

    private JPanel mainPanel;
    private JButton agregarButton;
    private JButton modificarButton;
    private JButton eliminarButton;
    protected JButton buscarPorEmailButton;

    public PacientePanelManager(JFrame mainFrame, Connection conexion) {
        this.mainFrame = mainFrame;
        this.conexion = conexion;
        PacienteDAOImpl pacienteDAO = new PacienteDAOImpl(conexion);
        pacienteService = new PacienteServiceImpl(pacienteDAO);
        initComponents();
    }

    private void initComponents() {
        mainFrame = new JFrame("Gestión de Pacientes");
        mainFrame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        cardLayout = new CardLayout();
        contentPanel = new JPanel(cardLayout);
        JPanel tablePanel = new JPanel(new BorderLayout());

        // Crear tabla dinámica
        tableModel = new DefaultTableModel(new Object[]{"ID", "Nombre y Apellido", "DNI", "Teléfono", "Email", "Obra Social"}, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false; // Deshabilitar edición de celdas
            }
        };
        table = new JTable(tableModel);
        table.getSelectionModel().addListSelectionListener(e -> actualizarFormulariosConSeleccion());
        JScrollPane scrollPane = new JScrollPane(table);
        tablePanel.add(scrollPane, BorderLayout.CENTER);

        // Pantalla principal sin formularios
        mainPanel = new JPanel(new BorderLayout());
        JPanel buttonPanel = new JPanel();
        agregarButton = new JButton("Agregar Paciente");
        modificarButton = new JButton("Modificar Paciente");
        eliminarButton = new JButton("Eliminar Paciente");
        buscarPorEmailButton = new JButton("Buscar por Email");

        agregarButton.addActionListener(e -> mostrarPanel("agregarPaciente"));
        modificarButton.addActionListener(e -> mostrarPanel("modificarPaciente"));
        eliminarButton.addActionListener(e -> mostrarPanel("eliminarPaciente"));
        buscarPorEmailButton.addActionListener(e -> buscarPorEmail());

        buttonPanel.add(agregarButton);
        buttonPanel.add(modificarButton);
        buttonPanel.add(eliminarButton);
        buttonPanel.add(buscarPorEmailButton);

        mainPanel.add(buttonPanel, BorderLayout.NORTH);
        mainPanel.add(tablePanel, BorderLayout.CENTER);

        // Agregar pantallas al contentPanel
        contentPanel.add(mainPanel, "mainPanel");

        // Inicializar los formularios
        agregarPacienteUI = new AgregarPacienteUI(pacienteService, this);
        modificarPacienteUI = new ModificarPacienteUI(pacienteService, this);
        eliminarPacienteUI = new EliminarPacienteUI(this, pacienteService);

        // Agregar formularios al contentPanel
        contentPanel.add(agregarPacienteUI, "agregarPaciente");
        contentPanel.add(modificarPacienteUI, "modificarPaciente");
        contentPanel.add(eliminarPacienteUI, "eliminarPaciente");

        mainFrame.add(contentPanel, BorderLayout.CENTER);

        mainFrame.pack();
        mainFrame.setVisible(true);

        // Mostrar la pantalla principal inicialmente
        mostrarPanel("mainPanel");

        // Botón para cerrar y volver al menú principal
        JButton volverButton = new JButton("Volver al Menú Principal");
        volverButton.addActionListener(e -> volverAlMenuPrincipal());
        // ... agregar el botón a la interfaz ...
    }

    private void buscarPorEmail() {
        String email = JOptionPane.showInputDialog(mainFrame, "Ingrese el email del médico:");
        if (email != null && !email.trim().isEmpty()) {
            try {
                Paciente paciente = pacienteService.buscarPorEmail(email);
                if (paciente != null) {
                    tableModel.setRowCount(0);
                    tableModel.addRow(new Object[]{
                            paciente.getId(),
                            paciente.getNombreYApellido(),
                            paciente.getDni(),
                            paciente.getTelefono(),
                            paciente.getEmail(),
                            paciente.getObraSocial()
                    });
                } else {
                    JOptionPane.showMessageDialog(mainFrame, "No se encontró ningún médico con ese email");
                }
            } catch (ServiceException e) {
                JOptionPane.showMessageDialog(mainFrame, "Error al buscar médico: " + e.getMessage());
            }
        }
    }

    public void mostrarPanel(String nombrePanel) {
        cardLayout.show(contentPanel, nombrePanel);
        actualizarTabla();
    }

    public void actualizarTabla() {
        try {
            tableModel.setRowCount(0);
            for (Paciente paciente : pacienteService.obtenerTodos()) {
                tableModel.addRow(new Object[]{
                        paciente.getId(),
                        paciente.getNombreYApellido(),
                        paciente.getDni(),
                        paciente.getTelefono(),
                        paciente.getEmail(),
                        paciente.getObraSocial()
                });
            }
        } catch (Exception e) {
            JOptionPane.showMessageDialog(null, "Error obteniendo pacientes: " + e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void actualizarFormulariosConSeleccion() {
        int selectedRow = table.getSelectedRow();
        if (selectedRow != -1) {
            int id = (int) tableModel.getValueAt(selectedRow, 0);
            String nombreApellido = (String) tableModel.getValueAt(selectedRow, 1);
            String dni = (String) tableModel.getValueAt(selectedRow, 2);
            String telefono = (String) tableModel.getValueAt(selectedRow, 3);
            String email = (String) tableModel.getValueAt(selectedRow, 4);
            String obraSocial = (String) tableModel.getValueAt(selectedRow, 5);

            // Actualizar los formularios con los datos seleccionados
            agregarPacienteUI.setFormData(id, nombreApellido, dni, telefono, email, obraSocial);
            modificarPacienteUI.setFormData(id, nombreApellido, dni, telefono, email, obraSocial);
            eliminarPacienteUI.setFormData(id, nombreApellido, dni, telefono, email, obraSocial);
        }
    }

    private void volverAlMenuPrincipal() {
        mainFrame.setVisible(true);
        // Cierra la ventana actual
        // Aquí puedes agregar código para cerrar la ventana actual si es necesario
    }
}
