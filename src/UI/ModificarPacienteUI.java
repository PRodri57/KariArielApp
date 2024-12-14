package UI;

import Model.Paciente;
import Service.PacienteService;
import Service.ServiceException;

import javax.swing.*;

public class ModificarPacienteUI extends AbstractPanel<Paciente> {
    private final PacienteService pacienteService;
    private final PacientePanelManager pacientePanelManager;

    public ModificarPacienteUI(PacienteService pacienteService, PacientePanelManager pacientePanelManager) {
        this.pacienteService = pacienteService;
        this.pacientePanelManager = pacientePanelManager;
        initComponents();
        setUpLayout();
    }

    @Override
    protected void armarFormulario(JPanel formPanel) {
        formPanel.add(new JLabel("ID:"));
        formPanel.add(idField);
        idField.setEditable(true);
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
        // Dejar vacío, no necesario en este panel
    }

    @Override
    protected void modificarItem() {
        Paciente paciente = new Paciente();
        paciente.setId(Integer.parseInt(idField.getText()));
        paciente.setNombreYApellido(nombreYApellidoField.getText());
        paciente.setDni(dniField.getText());
        paciente.setTelefono(telefonoField.getText());
        paciente.setEmail(emailField.getText());
        paciente.setObraSocial(obraSocialField.getText());

        try {
            pacienteService.modificarPaciente(paciente);
            pacientePanelManager.actualizarTabla();
            clearForm();
        } catch (ServiceException e) {
            JOptionPane.showMessageDialog(this, "Error modificando paciente: " + e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
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
        idField.setText("");
        nombreYApellidoField.setText("");
        dniField.setText("");
        telefonoField.setText("");
        emailField.setText("");
        obraSocialField.setText("");
    }

    @Override
    public void setFormData(int id, String nombreApellido, String dni, String telefono, String email, String obraSocial) {
        idField.setText(String.valueOf(id));
        nombreYApellidoField.setText(nombreApellido);
        dniField.setText(dni);
        telefonoField.setText(telefono);
        emailField.setText(email);
        obraSocialField.setText(obraSocial);
    }

    @Override
    protected void volver() {
        pacientePanelManager.mostrarPanel("mainPanel");
    }
}