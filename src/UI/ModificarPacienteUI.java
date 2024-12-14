package UI;

import Model.Paciente;
import Service.PacienteService;
import Service.ServiceException;

import javax.swing.*;
import java.awt.*;

public class ModificarPacienteUI extends JPanel {
    private PacienteService pacienteService;
    private PacientePanelManager panelManager;
    private int currentId;
    
    private JTextField nombreField;
    private JTextField dniField;
    private JTextField telefonoField;
    private JTextField emailField;
    private JTextField obraSocialField;
    
    public ModificarPacienteUI(PacienteService pacienteService, PacientePanelManager panelManager) {
        this.pacienteService = pacienteService;
        this.panelManager = panelManager;
        initComponents();
    }
    
    private void initComponents() {
        setLayout(new BorderLayout());
        
        // Panel para el formulario
        JPanel formPanel = new JPanel(new GridLayout(6, 2, 5, 5));
        formPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        
        formPanel.add(new JLabel("Nombre y Apellido:"));
        nombreField = new JTextField();
        formPanel.add(nombreField);
        
        formPanel.add(new JLabel("DNI:"));
        dniField = new JTextField();
        formPanel.add(dniField);
        
        formPanel.add(new JLabel("Teléfono:"));
        telefonoField = new JTextField();
        formPanel.add(telefonoField);
        
        formPanel.add(new JLabel("Email:"));
        emailField = new JTextField();
        formPanel.add(emailField);
        
        formPanel.add(new JLabel("Obra Social:"));
        obraSocialField = new JTextField();
        formPanel.add(obraSocialField);
        
        // Panel para botones
        JPanel buttonPanel = new JPanel();
        JButton guardarButton = new JButton("Guardar Cambios");
        JButton cancelarButton = new JButton("Cancelar");
        
        guardarButton.addActionListener(e -> modificarPaciente());
        cancelarButton.addActionListener(e -> panelManager.mostrarPanel("mainPanel"));
        
        buttonPanel.add(guardarButton);
        buttonPanel.add(cancelarButton);
        
        add(formPanel, BorderLayout.CENTER);
        add(buttonPanel, BorderLayout.SOUTH);
    }
    
    private void modificarPaciente() {
        try {
            Paciente paciente = new Paciente(
                currentId,
                nombreField.getText(),
                dniField.getText(),
                telefonoField.getText(),
                emailField.getText(),
                obraSocialField.getText()
            );
            
            pacienteService.modificarPaciente(paciente);
            JOptionPane.showMessageDialog(this, "Paciente modificado exitosamente");
            panelManager.mostrarPanel("mainPanel");
        } catch (ServiceException e) {
            JOptionPane.showMessageDialog(this, "Error al modificar paciente: " + e.getMessage());
        }
    }
    
    public void setFormData(int id, String nombre, String dni, String telefono, String email, 
                          String obraSocial) {
        this.currentId = id;
        nombreField.setText(nombre);
        dniField.setText(dni);
        telefonoField.setText(telefono);
        emailField.setText(email);
        obraSocialField.setText(obraSocial);
    }
}