package UI;

import Model.Paciente;
import Service.PacienteService;
import Service.ServiceException;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;

public class AgregarPacienteUI extends AbstractPanel<Paciente> {
    private final PacienteService pacienteService;
    private final PacientePanelManager pacientePanelManager;
    private DefaultTableModel tableModel;

    public AgregarPacienteUI(PacienteService pacienteService, PacientePanelManager pacientePanelManager) {
        this.pacienteService = pacienteService;
        this.pacientePanelManager = pacientePanelManager;
        initComponents();
        setUpLayout();
    }

    @Override
    protected void armarFormulario(JPanel formPanel) {
        formPanel.add(new JLabel("Nombre y Apellido:"));
        formPanel.add(nombreYApellidoField);
        formPanel.add(new JLabel("DNI:"));
        formPanel.add(dniField);
        formPanel.add(new JLabel("Teléfono:"));
        formPanel.add(telefonoField);
        formPanel.add(new JLabel("Email:"));
        formPanel.add(emailField);
        formPanel.add(new JLabel("Obra Social:"));
        formPanel.add(obraSocialField);
    }

    @Override
    protected void agregarItem() {
        Paciente paciente = new Paciente();
        paciente.setNombreYApellido(nombreYApellidoField.getText());
        paciente.setDni(dniField.getText());
        paciente.setTelefono(telefonoField.getText());
        paciente.setEmail(emailField.getText());
        paciente.setObraSocial(obraSocialField.getText());

        try {
            pacienteService.agregarPaciente(paciente);
            pacientePanelManager.actualizarTabla();
            clearForm();
        } catch (ServiceException e) {
            JOptionPane.showMessageDialog(this, "Error agregando paciente: " + e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    @Override
    protected void modificarItem() {
        // No necesario en este panel
    }

    @Override
    protected void eliminarItem() {
        // No necesario en este panel
    }

    @Override
    protected void actualizarTabla() {
        pacientePanelManager.actualizarTabla();
    }

    @Override
    protected void clearForm() {
        nombreYApellidoField.setText("");
        dniField.setText("");
        telefonoField.setText("");
        emailField.setText("");
        obraSocialField.setText("");
    }

    @Override
    public void setFormData(int id, String nombreApellido, String dni, String telefono, String email, String obraSocial) {
    }

    @Override
    protected void volver() {
        pacientePanelManager.mostrarPanel("mainPanel");
    }

}
