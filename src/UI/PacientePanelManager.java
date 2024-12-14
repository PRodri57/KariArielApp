package UI;

import DAO.PacienteDAOImpl;
import Model.Paciente;
import Service.PacienteService;
import Service.PacienteServiceImpl;
import Service.ServiceException;

import javax.swing.table.DefaultTableModel;
import javax.swing.*;
import java.sql.Connection;

public class PacientePanelManager extends AbstractPanelManager {
    private PacienteService pacienteService;
    private AgregarPacienteUI agregarPacienteUI;
    private ModificarPacienteUI modificarPacienteUI;
    private EliminarPacienteUI eliminarPacienteUI;

    public PacientePanelManager(MainMenuUI mainMenuUI, Connection conexion) {
        super(mainMenuUI, conexion);
    }

    @Override
    protected void initDAO() {
        PacienteDAOImpl pacienteDAO = new PacienteDAOImpl(conexion);
        pacienteService = new PacienteServiceImpl(pacienteDAO);
        
        tableModel = new DefaultTableModel(
            new Object[]{"ID", "Nombre y Apellido", "DNI", "Teléfono", "Email", "Obra Social"}, 
            0
        ) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };
    }

    @Override
    protected void initUIComponents() {
        agregarPacienteUI = new AgregarPacienteUI(pacienteService, this);
        modificarPacienteUI = new ModificarPacienteUI(pacienteService, this);
        eliminarPacienteUI = new EliminarPacienteUI(this, pacienteService);

        contentPanel.add(mainPanel, "mainPanel");
        contentPanel.add(agregarPacienteUI, "agregar");
        contentPanel.add(modificarPacienteUI, "modificar");
        contentPanel.add(eliminarPacienteUI, "eliminar");
    }

    @Override
    protected void actualizarTabla() throws ServiceException {
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
    }

    @Override
    protected void buscarPorEmail() {
        String email = JOptionPane.showInputDialog(null, "Ingrese el email del paciente:");
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
                    JOptionPane.showMessageDialog(null, "No se encontró ningún paciente con ese email");
                }
            } catch (ServiceException e) {
                JOptionPane.showMessageDialog(null, "Error al buscar paciente: " + e.getMessage());
            }
        }
    }

    @Override
    protected void actualizarFormulariosConSeleccion() {
        int selectedRow = table.getSelectedRow();
        if (selectedRow != -1) {
            int id = (int) tableModel.getValueAt(selectedRow, 0);
            String nombreApellido = (String) tableModel.getValueAt(selectedRow, 1);
            String dni = (String) tableModel.getValueAt(selectedRow, 2);
            String telefono = (String) tableModel.getValueAt(selectedRow, 3);
            String email = (String) tableModel.getValueAt(selectedRow, 4);
            String obraSocial = (String) tableModel.getValueAt(selectedRow, 5);

            agregarPacienteUI.setFormData(id, nombreApellido, dni, telefono, email, obraSocial);
            modificarPacienteUI.setFormData(id, nombreApellido, dni, telefono, email, obraSocial);
            eliminarPacienteUI.setFormData(id, nombreApellido, dni, telefono, email, obraSocial);
        }
    }
}
