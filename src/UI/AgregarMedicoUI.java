package UI;

import Model.Medico;
import Service.MedicoService;
import Service.ServiceException;

import javax.swing.*;
import java.awt.*;

public class AgregarMedicoUI extends JPanel {
    private MedicoService medicoService;
    private MedicoPanelManager panelManager;
    
    private JTextField nombreField;
    private JTextField dniField;
    private JTextField telefonoField;
    private JTextField emailField;
    private JTextField especialidadField;
    private JTextField valorConsultaField;
    private JTextField consultorioField;
    
    public AgregarMedicoUI(MedicoService medicoService, MedicoPanelManager panelManager) {
        this.medicoService = medicoService;
        this.panelManager = panelManager;
        initComponents();
    }
    
    private void initComponents() {
        setLayout(new BorderLayout());
        
        // Panel para el formulario
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
        
        formPanel.add(new JLabel("Consultorio:"));
        consultorioField = new JTextField();
        formPanel.add(consultorioField);
        
        // Panel para botones
        JPanel buttonPanel = new JPanel();
        JButton guardarButton = new JButton("Guardar");
        JButton cancelarButton = new JButton("Cancelar");
        
        guardarButton.addActionListener(e -> guardarMedico());
        cancelarButton.addActionListener(e -> panelManager.mostrarPanel("mainPanel"));
        
        buttonPanel.add(guardarButton);
        buttonPanel.add(cancelarButton);
        
        add(formPanel, BorderLayout.CENTER);
        add(buttonPanel, BorderLayout.SOUTH);
    }
    
    private void guardarMedico() {
        try {
            double valorConsulta = Double.parseDouble(valorConsultaField.getText());
            int consultorio = Integer.parseInt(consultorioField.getText());
            
            Medico medico = new Medico(
                0,
                nombreField.getText(),
                dniField.getText(),
                telefonoField.getText(),
                emailField.getText(),
                especialidadField.getText(),
                valorConsulta,
                consultorio
            );
            
            medicoService.agregar(medico);
            JOptionPane.showMessageDialog(this, "Médico agregado exitosamente");
            limpiarCampos();
            panelManager.mostrarPanel("mainPanel");
        } catch (NumberFormatException e) {
            JOptionPane.showMessageDialog(this, "El valor de consulta y el consultorio deben ser números válidos");
        } catch (ServiceException e) {
            JOptionPane.showMessageDialog(this, "Error al agregar médico: " + e.getMessage());
        }
    }
    
    private void limpiarCampos() {
        nombreField.setText("");
        dniField.setText("");
        telefonoField.setText("");
        emailField.setText("");
        especialidadField.setText("");
        valorConsultaField.setText("");
        consultorioField.setText("");
    }
    
    public void setFormData(int id, String nombre, String dni, String telefono, String email, 
                          String especialidad, double valorConsulta, int consultorio) {
        nombreField.setText(nombre);
        dniField.setText(dni);
        telefonoField.setText(telefono);
        emailField.setText(email);
        especialidadField.setText(especialidad);
        valorConsultaField.setText(String.valueOf(valorConsulta));
        consultorioField.setText(String.valueOf(consultorio));
    }
} 