package UI;

import Model.Medico;
import Service.MedicoService;
import Service.ServiceException;

import javax.swing.*;
import java.awt.*;

public class EliminarMedicoUI extends JPanel {
    private MedicoPanelManager panelManager;
    private MedicoService medicoService;
    private int currentId;
    
    private JLabel nombreLabel;
    private JLabel dniLabel;
    private JLabel telefonoLabel;
    private JLabel emailLabel;
    private JLabel especialidadLabel;
    private JLabel matriculaLabel;
    
    public EliminarMedicoUI(MedicoPanelManager panelManager, MedicoService medicoService) {
        this.panelManager = panelManager;
        this.medicoService = medicoService;
        initComponents();
    }
    
    private void initComponents() {
        setLayout(new BorderLayout());
        
        JPanel infoPanel = new JPanel(new GridLayout(7, 2, 5, 5));
        infoPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        
        infoPanel.add(new JLabel("Nombre y Apellido:"));
        nombreLabel = new JLabel();
        infoPanel.add(nombreLabel);
        
        infoPanel.add(new JLabel("DNI:"));
        dniLabel = new JLabel();
        infoPanel.add(dniLabel);
        
        infoPanel.add(new JLabel("Teléfono:"));
        telefonoLabel = new JLabel();
        infoPanel.add(telefonoLabel);
        
        infoPanel.add(new JLabel("Email:"));
        emailLabel = new JLabel();
        infoPanel.add(emailLabel);
        
        infoPanel.add(new JLabel("Especialidad:"));
        especialidadLabel = new JLabel();
        infoPanel.add(especialidadLabel);
        
        infoPanel.add(new JLabel("Matrícula:"));
        matriculaLabel = new JLabel();
        infoPanel.add(matriculaLabel);
        
        JPanel buttonPanel = new JPanel();
        JButton eliminarButton = new JButton("Confirmar Eliminación");
        JButton cancelarButton = new JButton("Cancelar");
        
        eliminarButton.addActionListener(e -> eliminarMedico());
        cancelarButton.addActionListener(e -> panelManager.mostrarPanel("mainPanel"));
        
        buttonPanel.add(eliminarButton);
        buttonPanel.add(cancelarButton);
        
        add(infoPanel, BorderLayout.CENTER);
        add(buttonPanel, BorderLayout.SOUTH);
    }
    
    private void eliminarMedico() {
        int confirm = JOptionPane.showConfirmDialog(
            this,
            "¿Está seguro que desea eliminar este médico?",
            "Confirmar eliminación",
            JOptionPane.YES_NO_OPTION
        );
        
        if (confirm == JOptionPane.YES_OPTION) {
            try {
                medicoService.eliminar(currentId);
                JOptionPane.showMessageDialog(this, "Médico eliminado exitosamente");
                panelManager.mostrarPanel("mainPanel");
            } catch (ServiceException e) {
                JOptionPane.showMessageDialog(this, "Error al eliminar médico: " + e.getMessage());
            }
        }
    }
    
    public void setFormData(int id, String nombre, String dni, String telefono, String email, 
                          String especialidad, String matricula) {
        this.currentId = id;
        nombreLabel.setText(nombre);
        dniLabel.setText(dni);
        telefonoLabel.setText(telefono);
        emailLabel.setText(email);
        especialidadLabel.setText(especialidad);
        matriculaLabel.setText(matricula);
    }
} 