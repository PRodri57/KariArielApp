package UI;

import Model.Paciente;
import Service.PacienteService;
import Service.ServiceException;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;

public class EliminarPacienteUI extends AbstractPanel<Paciente> {
    private PacienteService pacienteService;
    private PacientePanelManager pacientePanelManager;
    private DefaultTableModel tableModel;

    public EliminarPacienteUI(PacientePanelManager pacientePanelManager, PacienteService pacienteService) {
        this.pacientePanelManager = pacientePanelManager;
        this.pacienteService = pacienteService;
    }

    @Override
    protected void armarFormulario(JPanel formPanel) {
        formPanel.add(new JLabel("ID:"));
        formPanel.add(idField);
    }

    @Override
    protected void agregarItem() {
        // No necesario en este panel
    }

    @Override
    protected void modificarItem() {
        // No necesario en este panel
    }

    @Override
    protected void eliminarItem() {
        try {
            int id = Integer.parseInt(idField.getText());
            pacienteService.eliminarPaciente(id);
            actualizarTabla();
            clearForm();
        } catch (ServiceException | NumberFormatException e) {
            JOptionPane.showMessageDialog(this, "Error eliminando paciente: " + e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }


    @Override
    protected void clearForm() {
        idField.setText("");
    }

    @Override
    protected void volver() {
        pacientePanelManager.mostrarPanel("mainPanel");
    }

    @Override
    public void setFormData(int id, String nombreApellido, String dni, String telefono, String email, String obraSocial) {
        idField.setText(String.valueOf(id));
    }

    @Override
    protected void actualizarTabla() {
        pacientePanelManager.actualizarTabla();
    }
}
