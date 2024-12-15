package UI;

import Model.Turno;
import Model.Medico;
import Model.Paciente;
import Service.TurnoService;
import Service.ServiceException;

import javax.swing.*;
import java.awt.*;
import java.util.List;
import java.util.Calendar;
import java.util.Date;

public class AgregarTurnoUI extends JPanel {
    private TurnoService turnoService;
    private TurnoPanelManager panelManager;
    private List<Medico> medicos;
    private List<Paciente> pacientes;
    
    private JComboBox<Medico> medicoCombo;
    private JComboBox<Paciente> pacienteCombo;
    private JComboBox<Integer> diaCombo;
    private JComboBox<Integer> mesCombo;
    private JComboBox<Integer> anioCombo;
    private JComboBox<String> horaCombo;
    private JComboBox<String> minutoCombo;
    private JComboBox<String> estadoCombo;
    
    public AgregarTurnoUI(TurnoService turnoService, TurnoPanelManager panelManager, 
                         List<Medico> medicos, List<Paciente> pacientes) {
        this.turnoService = turnoService;
        this.panelManager = panelManager;
        this.medicos = medicos;
        this.pacientes = pacientes;
        initComponents();
    }
    
    private void initComponents() {
        setLayout(new BorderLayout());
        
        // Panel para el formulario
        JPanel formPanel = new JPanel(new GridLayout(8, 2, 5, 5));
        formPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        
        // Médico
        formPanel.add(new JLabel("Médico:"));
        medicoCombo = new JComboBox<>(medicos.toArray(new Medico[0]));
        formPanel.add(medicoCombo);
        
        // Paciente
        formPanel.add(new JLabel("Paciente:"));
        pacienteCombo = new JComboBox<>(pacientes.toArray(new Paciente[0]));
        formPanel.add(pacienteCombo);
        
        // Fecha
        formPanel.add(new JLabel("Día:"));
        diaCombo = new JComboBox<>();
        for (int i = 1; i <= 31; i++) diaCombo.addItem(i);
        formPanel.add(diaCombo);
        
        formPanel.add(new JLabel("Mes:"));
        mesCombo = new JComboBox<>();
        for (int i = 1; i <= 12; i++) mesCombo.addItem(i);
        formPanel.add(mesCombo);
        
        formPanel.add(new JLabel("Año:"));
        anioCombo = new JComboBox<>();
        int currentYear = Calendar.getInstance().get(Calendar.YEAR);
        for (int i = currentYear; i <= currentYear + 1; i++) anioCombo.addItem(i);
        formPanel.add(anioCombo);
        
        // Hora
        formPanel.add(new JLabel("Hora:"));
        horaCombo = new JComboBox<>();
        for (int i = 8; i <= 20; i++) horaCombo.addItem(String.format("%02d", i));
        formPanel.add(horaCombo);
        
        formPanel.add(new JLabel("Minuto:"));
        minutoCombo = new JComboBox<>();
        for (int i = 0; i < 60; i += 15) minutoCombo.addItem(String.format("%02d", i));
        formPanel.add(minutoCombo);
        
        // Estado
        formPanel.add(new JLabel("Estado:"));
        estadoCombo = new JComboBox<>(new String[]{"Pendiente", "Confirmado", "Cancelado"});
        formPanel.add(estadoCombo);
        
        // Panel para botones
        JPanel buttonPanel = new JPanel();
        JButton guardarButton = new JButton("Guardar");
        JButton cancelarButton = new JButton("Cancelar");
        
        guardarButton.addActionListener(e -> guardarTurno());
        cancelarButton.addActionListener(e -> panelManager.mostrarPanel("mainPanel"));
        
        buttonPanel.add(guardarButton);
        buttonPanel.add(cancelarButton);
        
        add(formPanel, BorderLayout.CENTER);
        add(buttonPanel, BorderLayout.SOUTH);
    }
    
    private void guardarTurno() {
        try {
            Calendar calendar = Calendar.getInstance();
            calendar.set(Calendar.YEAR, (Integer) anioCombo.getSelectedItem());
            calendar.set(Calendar.MONTH, (Integer) mesCombo.getSelectedItem() - 1);
            calendar.set(Calendar.DAY_OF_MONTH, (Integer) diaCombo.getSelectedItem());
            Date fecha = calendar.getTime();
            
            calendar.set(Calendar.HOUR_OF_DAY, Integer.parseInt((String) horaCombo.getSelectedItem()));
            calendar.set(Calendar.MINUTE, Integer.parseInt((String) minutoCombo.getSelectedItem()));
            calendar.set(Calendar.SECOND, 0);
            Date hora = calendar.getTime();
            
            Turno turno = new Turno(
                0,
                fecha,
                hora,
                (Medico) medicoCombo.getSelectedItem(),
                (Paciente) pacienteCombo.getSelectedItem(),
                (String) estadoCombo.getSelectedItem()
            );
            
            turnoService.agregarTurno(turno);
            JOptionPane.showMessageDialog(this, "Turno agregado exitosamente");
            limpiarCampos();
            panelManager.mostrarPanel("mainPanel");
        } catch (ServiceException e) {
            JOptionPane.showMessageDialog(this, "Error al agregar turno: " + e.getMessage());
        }
    }
    
    private void limpiarCampos() {
        medicoCombo.setSelectedIndex(0);
        pacienteCombo.setSelectedIndex(0);
        diaCombo.setSelectedIndex(0);
        mesCombo.setSelectedIndex(0);
        anioCombo.setSelectedIndex(0);
        horaCombo.setSelectedIndex(0);
        minutoCombo.setSelectedIndex(0);
        estadoCombo.setSelectedIndex(0);
    }
} 