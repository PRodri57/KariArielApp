package UI;

import DAO.MedicoDAOImpl;
import Model.Medico;
import Service.MedicoService;
import Service.MedicoServiceImpl;
import Service.ServiceException;
import javax.swing.table.DefaultTableModel;
import javax.swing.*;
import java.sql.Connection;

public class MedicoPanelManager extends AbstractPanelManager {
    private MedicoService medicoService;
    private AgregarMedicoUI agregarMedicoUI;
    private ModificarMedicoUI modificarMedicoUI;
    private EliminarMedicoUI eliminarMedicoUI;

    public MedicoPanelManager(MainMenuUI mainMenuUI, Connection conexion) {
        super(mainMenuUI, conexion);
        init();
    }

    @Override
    protected void initDAO() {
        MedicoDAOImpl medicoDAO = new MedicoDAOImpl(conexion);
        medicoService = new MedicoServiceImpl(medicoDAO);
        
        tableModel = new DefaultTableModel(
            new Object[]{"ID", "Nombre y Apellido", "DNI", "Teléfono", "Email", "Especialidad", "Matrícula", "Consultorio"}, 
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
        agregarMedicoUI = new AgregarMedicoUI(medicoService, this);
        modificarMedicoUI = new ModificarMedicoUI(medicoService, this);
        eliminarMedicoUI = new EliminarMedicoUI(this, medicoService);

        contentPanel.add(agregarMedicoUI, "agregar");
        contentPanel.add(modificarMedicoUI, "modificar");
        contentPanel.add(eliminarMedicoUI, "eliminar");
    }

    @Override
    protected void actualizarTabla() throws ServiceException {
        tableModel.setRowCount(0);
        for (Medico medico : medicoService.obtenerTodos()) {
            tableModel.addRow(new Object[]{
                medico.getId(),
                medico.getNombreYApellido(),
                medico.getDni(),
                medico.getTelefono(),
                medico.getEmail(),
                medico.getEspecialidad(),
                medico.getValorConsulta(),
                medico.getConsultorio()
            });
        }
    }

    @Override
    protected void buscarPorEmail() {
        String email = JOptionPane.showInputDialog(null, "Ingrese el email del médico:");
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
                        medico.getValorConsulta()
                    });
                } else {
                    JOptionPane.showMessageDialog(null, "No se encontró ningún médico con ese email");
                }
            } catch (ServiceException e) {
                JOptionPane.showMessageDialog(null, "Error al buscar médico: " + e.getMessage());
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
            String especialidad = (String) tableModel.getValueAt(selectedRow, 5);
            double valorConsulta = (double) tableModel.getValueAt(selectedRow, 6);
            int consultorio = (int) tableModel.getValueAt(selectedRow, 7);

            agregarMedicoUI.setFormData(id, nombreApellido, dni, telefono, email, especialidad, valorConsulta, consultorio);
            modificarMedicoUI.setFormData(id, nombreApellido, dni, telefono, email, especialidad, valorConsulta, consultorio);
            eliminarMedicoUI.setFormData(id, nombreApellido, dni, telefono, email, especialidad, valorConsulta, consultorio);
        }
    }
}