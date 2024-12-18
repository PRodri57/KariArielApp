package UI;

import Model.Medico;
import Model.Turno;
import Service.MedicoService;
import Service.TurnoService;
import Service.ServiceException;

import javax.swing.*;
import java.awt.*;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

public class SolicitarTurnoUI extends JPanel {
    private TurnoService turnoService;
    private MedicoService medicoService;
    private int pacienteId;
    private JComboBox<Medico> medicoCombo;
    private SpinnerDateModel dateModel;
    private JSpinner dateSpinner;

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
        mainPanel.add(medicoCombo, gbc);

        // Selector de fecha y hora
        gbc.gridx = 0;
        gbc.gridy = 2;
        mainPanel.add(new JLabel("Fecha y Hora:"), gbc);

        gbc.gridx = 1;
        dateModel = new SpinnerDateModel();
        dateSpinner = new JSpinner(dateModel);
        JSpinner.DateEditor dateEditor = new JSpinner.DateEditor(dateSpinner, "dd/MM/yyyy HH:mm");
        dateSpinner.setEditor(dateEditor);
        mainPanel.add(dateSpinner, gbc);

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

    private void solicitarTurno() {
        try {
            Medico medicoSeleccionado = (Medico) medicoCombo.getSelectedItem();
            Date fechaSeleccionada = dateModel.getDate();

            if (medicoSeleccionado == null) {
                JOptionPane.showMessageDialog(this, 
                    "Por favor seleccione un médico", 
                    "Error", 
                    JOptionPane.ERROR_MESSAGE);
                return;
            }

            Turno nuevoTurno = new Turno(
                0,  // el ID será asignado por la base de datos
                fechaSeleccionada,
                fechaSeleccionada,
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
        } catch (ServiceException e) {
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
} 