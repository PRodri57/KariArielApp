package UI;

import Service.PacienteService;
import Service.ServiceException;

import javax.swing.*;
import java.awt.*;

public class EliminarPacienteUI extends JPanel {
    private PacientePanelManager panelManager;
    private PacienteService pacienteService;
    private int currentId;
    
    private JLabel nombreLabel;
    private JLabel dniLabel;
    private JLabel telefonoLabel;
    private JLabel emailLabel;
    private JLabel obraSocialLabel;
    
    public EliminarPacienteUI(PacientePanelManager panelManager, PacienteService pacienteService) {
        this.panelManager = panelManager;
        this.pacienteService = pacienteService;
        initComponents();
    }
    
    private void initComponents() {
        setLayout(new BorderLayout());
        
        JPanel infoPanel = new JPanel(new GridLayout(6, 2, 5, 5));
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
        
        infoPanel.add(new JLabel("Obra Social:"));
        obraSocialLabel = new JLabel();
        infoPanel.add(obraSocialLabel);
        
        JPanel buttonPanel = new JPanel();
        JButton eliminarButton = new JButton("Confirmar Eliminación");
        JButton cancelarButton = new JButton("Cancelar");
        
        eliminarButton.addActionListener(e -> eliminarPaciente());
        cancelarButton.addActionListener(e -> panelManager.mostrarPanel("mainPanel"));
        
        buttonPanel.add(eliminarButton);
        buttonPanel.add(cancelarButton);
        
        add(infoPanel, BorderLayout.CENTER);
        add(buttonPanel, BorderLayout.SOUTH);
    }
    
    private void eliminarPaciente() {
        int confirm = JOptionPane.showConfirmDialog(
            this,
            "¿Está seguro que desea eliminar este paciente?",
            "Confirmar eliminación",
            JOptionPane.YES_NO_OPTION
        );
        
        if (confirm == JOptionPane.YES_OPTION) {
            try {
                pacienteService.eliminarPaciente(currentId);
                JOptionPane.showMessageDialog(this, "Paciente eliminado exitosamente");
                panelManager.mostrarPanel("mainPanel");
            } catch (ServiceException e) {
                JOptionPane.showMessageDialog(this, "Error al eliminar paciente: " + e.getMessage());
            }
        }
    }
    
    public void setFormData(int id, String nombre, String dni, String telefono, String email, 
                          String obraSocial) {
        this.currentId = id;
        nombreLabel.setText(nombre);
        dniLabel.setText(dni);
        telefonoLabel.setText(telefono);
        emailLabel.setText(email);
        obraSocialLabel.setText(obraSocial);
    }
}
