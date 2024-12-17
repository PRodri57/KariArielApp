package UI;

import Model.Medico;
import Service.MedicoService;
import Service.ServiceException;

import javax.swing.*;
import java.awt.*;

public class ModificarMedicoUI extends JPanel {
    private MedicoService medicoService;
    private MedicoPanelManager panelManager;
    private int currentId;
    
    private JTextField nombreField;
    private JTextField dniField;
    private JTextField telefonoField;
    private JTextField emailField;
    private JTextField especialidadField;
    private JTextField valorConsultaField;
    
    public ModificarMedicoUI(MedicoService medicoService, MedicoPanelManager panelManager) {
        this.medicoService = medicoService;
        this.panelManager = panelManager;
        initComponents();
    }
    
    private void initComponents() {
        setLayout(new BorderLayout());
        
        JPanel formPanel = new JPanel(new GridLayout(7, 2, 5, 5));
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
        
        formPanel.add(new JLabel("Especialidad:"));
        especialidadField = new JTextField();
        formPanel.add(especialidadField);
        
        formPanel.add(new JLabel("Valor Consulta:"));
        valorConsultaField = new JTextField();
        formPanel.add(valorConsultaField);
        
        JPanel buttonPanel = new JPanel();
        JButton guardarButton = new JButton("Guardar Cambios");
        JButton cancelarButton = new JButton("Cancelar");
        
        guardarButton.addActionListener(e -> modificarMedico());
        cancelarButton.addActionListener(e -> panelManager.mostrarPanel("mainPanel"));
        
        buttonPanel.add(guardarButton);
        buttonPanel.add(cancelarButton);
        
        add(formPanel, BorderLayout.CENTER);
        add(buttonPanel, BorderLayout.SOUTH);
    }
    
    private void modificarMedico() {
        try {
            Medico medico = new Medico(
                currentId,
                nombreField.getText(),
                dniField.getText(),
                telefonoField.getText(),
                emailField.getText(),
                especialidadField.getText(),
                Double.parseDouble(valorConsultaField.getText())
            );
            
            medicoService.modificar(medico);
            JOptionPane.showMessageDialog(this, "Médico modificado exitosamente");
            panelManager.mostrarPanel("mainPanel");
        } catch (NumberFormatException e) {
            JOptionPane.showMessageDialog(this, "El valor de consulta debe ser un número válido");
        } catch (ServiceException e) {
            JOptionPane.showMessageDialog(this, "Error al modificar médico: " + e.getMessage());
        }
    }
    
    public void setFormData(int id, String nombre, String dni, String telefono, String email, 
                          String especialidad, double valorConsulta) {
        this.currentId = id;
        nombreField.setText(nombre);
        dniField.setText(dni);
        telefonoField.setText(telefono);
        emailField.setText(email);
        especialidadField.setText(especialidad);
        valorConsultaField.setText(String.valueOf(valorConsulta));
    }
} 