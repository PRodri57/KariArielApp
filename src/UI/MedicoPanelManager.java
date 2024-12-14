package UI;

import DAO.MedicoDAOImpl;
import Model.Medico;
import Service.MedicoService;
import Service.MedicoServiceImpl;
import Service.ServiceException;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.sql.Connection;

public class MedicoPanelManager {
    private MainMenuUI mainMenuUI;
    private JPanel mainPanel;
    private JPanel contentPanel;
    private CardLayout cardLayout;
    private JTable table;
    private DefaultTableModel tableModel;
    private MedicoService medicoService;
    private Connection conexion;

    private AgregarMedicoUI agregarMedicoUI;
    private ModificarMedicoUI modificarMedicoUI;
    private EliminarMedicoUI eliminarMedicoUI;

    public MedicoPanelManager(MainMenuUI mainMenuUI, Connection conexion) {
        this.mainMenuUI = mainMenuUI;
        this.conexion = conexion;
        MedicoDAOImpl medicoDAO = new MedicoDAOImpl(conexion);
        medicoService = new MedicoServiceImpl(medicoDAO);
        initComponents();
    }

    private void initComponents() {
        cardLayout = new CardLayout();
        contentPanel = new JPanel(cardLayout);
        JPanel tablePanel = new JPanel(new BorderLayout());

        // Crear tabla dinámica
        tableModel = new DefaultTableModel(
            new Object[]{"ID", "Nombre y Apellido", "DNI", "Teléfono", "Email", "Especialidad", "Matrícula"}, 
            0
        ) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };
        table = new JTable(tableModel);
        table.getSelectionModel().addListSelectionListener(e -> actualizarFormulariosConSeleccion());
        JScrollPane scrollPane = new JScrollPane(table);
        tablePanel.add(scrollPane, BorderLayout.CENTER);

        // Panel principal con botones
        mainPanel = new JPanel(new BorderLayout());
        JPanel buttonPanel = new JPanel();
        JButton agregarButton = new JButton("Agregar Médico");
        JButton modificarButton = new JButton("Modificar Médico");
        JButton eliminarButton = new JButton("Eliminar Médico");
        JButton buscarPorEmailButton = new JButton("Buscar por Email");
        JButton volverButton = new JButton("Volver al Menú Principal");

        agregarButton.addActionListener(e -> mostrarPanel("agregarMedico"));
        modificarButton.addActionListener(e -> mostrarPanel("modificarMedico"));
        eliminarButton.addActionListener(e -> mostrarPanel("eliminarMedico"));
        buscarPorEmailButton.addActionListener(e -> buscarPorEmail());
        volverButton.addActionListener(e -> volverAlMenuPrincipal());

        buttonPanel.add(agregarButton);
        buttonPanel.add(modificarButton);
        buttonPanel.add(eliminarButton);
        buttonPanel.add(buscarPorEmailButton);
        buttonPanel.add(volverButton);

        mainPanel.add(buttonPanel, BorderLayout.NORTH);
        mainPanel.add(tablePanel, BorderLayout.CENTER);

        // Agregar pantallas al contentPanel
        contentPanel.add(mainPanel, "mainPanel");

        // Inicializar los formularios
        agregarMedicoUI = new AgregarMedicoUI(medicoService, this);
        modificarMedicoUI = new ModificarMedicoUI(medicoService, this);
        eliminarMedicoUI = new EliminarMedicoUI(this, medicoService);

        contentPanel.add(agregarMedicoUI, "agregarMedico");
        contentPanel.add(modificarMedicoUI, "modificarMedico");
        contentPanel.add(eliminarMedicoUI, "eliminarMedico");

        mostrarPanel("mainPanel");
        actualizarTabla();
    }

    private void buscarPorEmail() {
        String email = JOptionPane.showInputDialog(mainPanel, "Ingrese el email del médico:");
        if (email != null && !email.trim().isEmpty()) {
            try {
                Medico medico = medicoService.buscarPorEmail(email);
                if (medico != null) {
                    tableModel.setRowCount(0);
                    tableModel.addRow(new Object[]{
                        medico.getId(),
                        medico.getNombreYApellido(),
                        medico.getDni(),
                        medico.getTelefono(),
                        medico.getEmail(),
                        medico.getEspecialidad(),
                        medico.getMatricula()
                    });
                } else {
                    JOptionPane.showMessageDialog(mainPanel, "No se encontró ningún médico con ese email");
                }
            } catch (ServiceException e) {
                JOptionPane.showMessageDialog(mainPanel, "Error al buscar médico: " + e.getMessage());
            }
        }
    }

    public void mostrarPanel(String nombrePanel) {
        cardLayout.show(contentPanel, nombrePanel);
        if (nombrePanel.equals("mainPanel")) {
            actualizarTabla();
        }
    }

    public void actualizarTabla() {
        try {
            tableModel.setRowCount(0);
            for (Medico medico : medicoService.obtenerTodos()) {
                tableModel.addRow(new Object[]{
                    medico.getId(),
                    medico.getNombreYApellido(),
                    medico.getDni(),
                    medico.getTelefono(),
                    medico.getEmail(),
                    medico.getEspecialidad(),
                    medico.getMatricula()
                });
            }
        } catch (ServiceException e) {
            JOptionPane.showMessageDialog(mainPanel, "Error al obtener médicos: " + e.getMessage());
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
            String especialidad = (String) tableModel.getValueAt(selectedRow, 5);
            String matricula = (String) tableModel.getValueAt(selectedRow, 6);

            agregarMedicoUI.setFormData(id, nombreApellido, dni, telefono, email, especialidad, matricula);
            modificarMedicoUI.setFormData(id, nombreApellido, dni, telefono, email, especialidad, matricula);
            eliminarMedicoUI.setFormData(id, nombreApellido, dni, telefono, email, especialidad, matricula);
        }
    }

    private void volverAlMenuPrincipal() {
        mainMenuUI.mostrarMenuPrincipal();
    }

    public JPanel getMainPanel() {
        return contentPanel;
    }
}