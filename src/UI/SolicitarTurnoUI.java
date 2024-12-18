package UI;

import Model.Medico;
import Model.Turno;
import Service.MedicoService;
import Service.TurnoService;
import Service.ServiceException;

import javax.swing.*;
import java.awt.*;
import java.util.Date;
import java.util.List;
import java.util.Calendar;
import java.text.SimpleDateFormat;

public class SolicitarTurnoUI extends JPanel {
    private TurnoService turnoService;
    private MedicoService medicoService;
    private int pacienteId;
    private JComboBox<Medico> medicoCombo;
    private SpinnerDateModel dateModel;
    private JSpinner dateSpinner;
    private JComboBox<String> horaCombo;
    private JLabel consultorioLabel;

    public SolicitarTurnoUI(TurnoService turnoService, MedicoService medicoService, int pacienteId) {
        this.turnoService = turnoService;
        this.medicoService = medicoService;
        this.pacienteId = pacienteId;
        initComponents();
        cargarMedicos();
    }

    private void initComponents() {
        setLayout(new BorderLayout(10, 10));
        setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // Panel principal
        JPanel mainPanel = new JPanel(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        // Título
        JLabel titleLabel = new JLabel("Solicitar Turno", SwingConstants.CENTER);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 20));
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.gridwidth = 2;
        mainPanel.add(titleLabel, gbc);

        // Selector de médico
        gbc.gridy = 1;
        gbc.gridwidth = 1;
        mainPanel.add(new JLabel("Médico:"), gbc);

        gbc.gridx = 1;
        medicoCombo = new JComboBox<>();
        medicoCombo.addActionListener(e -> actualizarConsultorio());
        mainPanel.add(medicoCombo, gbc);

        // Mostrar consultorio
        gbc.gridx = 0;
        gbc.gridy = 2;
        mainPanel.add(new JLabel("Consultorio:"), gbc);

        gbc.gridx = 1;
        consultorioLabel = new JLabel();
        mainPanel.add(consultorioLabel, gbc);

        // Selector de fecha
        gbc.gridx = 0;
        gbc.gridy = 3;
        mainPanel.add(new JLabel("Fecha:"), gbc);

        gbc.gridx = 1;
        dateModel = new SpinnerDateModel();
        dateModel.setCalendarField(Calendar.DAY_OF_MONTH);
        dateSpinner = new JSpinner(dateModel);
        JSpinner.DateEditor dateEditor = new JSpinner.DateEditor(dateSpinner, "dd/MM/yyyy");
        dateSpinner.setEditor(dateEditor);
        mainPanel.add(dateSpinner, gbc);

        // Selector de hora
        gbc.gridx = 0;
        gbc.gridy = 4;
        mainPanel.add(new JLabel("Hora:"), gbc);

        gbc.gridx = 1;
        horaCombo = new JComboBox<>();
        cargarHorarios();
        mainPanel.add(horaCombo, gbc);

        add(mainPanel, BorderLayout.CENTER);

        // Panel de botones
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        
        JButton solicitarButton = new JButton("Solicitar Turno");
        solicitarButton.addActionListener(e -> solicitarTurno());
        
        JButton volverButton = new JButton("Volver");
        volverButton.addActionListener(e -> volverAlMenu());
        
        buttonPanel.add(solicitarButton);
        buttonPanel.add(volverButton);
        add(buttonPanel, BorderLayout.SOUTH);
    }

    private void cargarMedicos() {
        try {
            List<Medico> medicos = medicoService.obtenerTodos();
            medicoCombo.removeAllItems();
            for (Medico medico : medicos) {
                medicoCombo.addItem(medico);
            }
        } catch (ServiceException e) {
            JOptionPane.showMessageDialog(this, 
                "Error al cargar médicos: " + e.getMessage(), 
                "Error", 
                JOptionPane.ERROR_MESSAGE);
        }
    }

    private void cargarHorarios() {
        Calendar cal = Calendar.getInstance();
        cal.set(Calendar.HOUR_OF_DAY, 8);
        cal.set(Calendar.MINUTE, 0);
        
        SimpleDateFormat timeFormat = new SimpleDateFormat("HH:mm");
        
        while (cal.get(Calendar.HOUR_OF_DAY) < 20 || 
              (cal.get(Calendar.HOUR_OF_DAY) == 20 && cal.get(Calendar.MINUTE) == 0)) {
            horaCombo.addItem(timeFormat.format(cal.getTime()));
            cal.add(Calendar.MINUTE, 30);
        }
    }

    private void solicitarTurno() {
        try {
            Medico medicoSeleccionado = (Medico) medicoCombo.getSelectedItem();
            Date fechaSeleccionada = dateModel.getDate();
            String horaSeleccionada = (String) horaCombo.getSelectedItem();

            if (medicoSeleccionado == null) {
                JOptionPane.showMessageDialog(this, 
                    "Por favor seleccione un médico", 
                    "Error", 
                    JOptionPane.ERROR_MESSAGE);
                return;
            }

            SimpleDateFormat timeFormat = new SimpleDateFormat("HH:mm");
            Date horaDate = timeFormat.parse(horaSeleccionada);
            
            Calendar fechaCal = Calendar.getInstance();
            fechaCal.setTime(fechaSeleccionada);
            
            Calendar horaCal = Calendar.getInstance();
            horaCal.setTime(horaDate);
            
            fechaCal.set(Calendar.HOUR_OF_DAY, horaCal.get(Calendar.HOUR_OF_DAY));
            fechaCal.set(Calendar.MINUTE, horaCal.get(Calendar.MINUTE));

            Turno nuevoTurno = new Turno(
                0,  // el ID será asignado por la base de datos
                fechaCal.getTime(),  // fecha completa
                fechaCal.getTime(),  // hora
                medicoSeleccionado,
                null,  // el paciente se manejará por ID
                "PENDIENTE"
            );
            
            nuevoTurno.setPacienteId(pacienteId);

            turnoService.agregarTurno(nuevoTurno);
            JOptionPane.showMessageDialog(this, 
                "Turno solicitado exitosamente", 
                "Éxito", 
                JOptionPane.INFORMATION_MESSAGE);
            volverAlMenu();
        } catch (Exception e) {
            JOptionPane.showMessageDialog(this, 
                "Error al solicitar turno: " + e.getMessage(), 
                "Error", 
                JOptionPane.ERROR_MESSAGE);
        }
    }

    private void volverAlMenu() {
        Container parent = getParent();
        if (parent != null) {
            CardLayout cardLayout = (CardLayout) parent.getLayout();
            cardLayout.show(parent, "menu");
        }
    }

    private void actualizarConsultorio() {
        Medico medicoSeleccionado = (Medico) medicoCombo.getSelectedItem();
        if (medicoSeleccionado != null) {
            consultorioLabel.setText("Consultorio " + medicoSeleccionado.getConsultorio());
        } else {
            consultorioLabel.setText("");
        }
    }
} 