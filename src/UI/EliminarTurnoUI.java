package UI;

import Model.Turno;
import Service.TurnoService;
import Service.ServiceException;

import javax.swing.*;
import java.awt.*;
import java.text.SimpleDateFormat;

public class EliminarTurnoUI extends JPanel {
    private TurnoPanelManager panelManager;
    private TurnoService turnoService;
    private int currentId;
    
    private JLabel fechaLabel;
    private JLabel horaLabel;
    private JLabel medicoLabel;
    private JLabel pacienteLabel;
    private JLabel estadoLabel;
    
    public EliminarTurnoUI(TurnoPanelManager panelManager, TurnoService turnoService) {
        this.panelManager = panelManager;
        this.turnoService = turnoService;
        initComponents();
    }
    
    private void initComponents() {
        setLayout(new BorderLayout());
        
        // Panel de información
        JPanel infoPanel = new JPanel(new GridLayout(6, 2, 5, 5));
        infoPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        
        // Añadir campos de información
        infoPanel.add(new JLabel("Fecha:"));
        fechaLabel = new JLabel();
        infoPanel.add(fechaLabel);
        
        infoPanel.add(new JLabel("Hora:"));
        horaLabel = new JLabel();
        infoPanel.add(horaLabel);
        
        infoPanel.add(new JLabel("Médico:"));
        medicoLabel = new JLabel();
        infoPanel.add(medicoLabel);
        
        infoPanel.add(new JLabel("Paciente:"));
        pacienteLabel = new JLabel();
        infoPanel.add(pacienteLabel);
        
        infoPanel.add(new JLabel("Estado:"));
        estadoLabel = new JLabel();
        infoPanel.add(estadoLabel);
        
        // Mensaje de advertencia
        JLabel warningLabel = new JLabel("¿Está seguro que desea eliminar este turno?");
        warningLabel.setForeground(Color.RED);
        warningLabel.setHorizontalAlignment(SwingConstants.CENTER);
        infoPanel.add(warningLabel);
        
        // Panel de botones
        JPanel buttonPanel = new JPanel();
        JButton eliminarButton = new JButton("Confirmar Eliminación");
        JButton cancelarButton = new JButton("Cancelar");
        
        eliminarButton.addActionListener(e -> eliminarTurno());
        cancelarButton.addActionListener(e -> panelManager.mostrarPanel("mainPanel"));
        
        buttonPanel.add(eliminarButton);
        buttonPanel.add(cancelarButton);
        
        add(infoPanel, BorderLayout.CENTER);
        add(buttonPanel, BorderLayout.SOUTH);
    }
    
    public void setFormData(Turno turno) {
        this.currentId = turno.getId();
        
        SimpleDateFormat dateFormat = new SimpleDateFormat("dd/MM/yyyy");
        SimpleDateFormat timeFormat = new SimpleDateFormat("HH:mm");
        
        fechaLabel.setText(dateFormat.format(turno.getFecha()));
        horaLabel.setText(timeFormat.format(turno.getHora()));
        medicoLabel.setText(turno.getMedico().getNombreYApellido());
        pacienteLabel.setText(turno.getPaciente().getNombreYApellido());
        estadoLabel.setText(turno.getEstado());
    }
    
    private void eliminarTurno() {
        int confirm = JOptionPane.showConfirmDialog(
            this,
            "¿Está seguro que desea eliminar este turno?",
            "Confirmar eliminación",
            JOptionPane.YES_NO_OPTION
        );
        
        if (confirm == JOptionPane.YES_OPTION) {
            try {
                turnoService.eliminarTurno(currentId);
                JOptionPane.showMessageDialog(this, "Turno eliminado exitosamente");
                panelManager.mostrarPanel("mainPanel");
            } catch (ServiceException e) {
                JOptionPane.showMessageDialog(this, "Error al eliminar turno: " + e.getMessage());
            }
        }
    }
} 