package UI;

import Model.Turno;
import Service.TurnoService;
import Service.ServiceException;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.*;
import java.text.SimpleDateFormat;
import java.util.List;
import java.util.Date;


public class CalendarioTurnosUI extends JPanel {
    private TurnoService turnoService;
    private int medicoId;  // -1 para admin (todos los médicos), otro valor para médico específico
    private DefaultTableModel tableModel;

    public CalendarioTurnosUI(TurnoService turnoService, int medicoId) {
        this.turnoService = turnoService;
        this.medicoId = medicoId;
        initComponents();
    }

    private void initComponents() {
        setLayout(new BorderLayout());
        setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // Panel superior con selector de fecha
        JPanel topPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JLabel fechaLabel = new JLabel("Seleccione fecha:");
        
        // Crear selectores para día, mes y año
        SpinnerDateModel dateModel = new SpinnerDateModel();
        JSpinner dateSpinner = new JSpinner(dateModel);
        JSpinner.DateEditor dateEditor = new JSpinner.DateEditor(dateSpinner, "dd/MM/yyyy");
        dateSpinner.setEditor(dateEditor);
        dateSpinner.setValue(new Date());  // Fecha actual por defecto
        
        JButton buscarButton = new JButton("Buscar Turnos");
        topPanel.add(fechaLabel);
        topPanel.add(dateSpinner);
        topPanel.add(buscarButton);

        // Tabla de turnos
        String[] columnas = {"Hora", "Médico", "Paciente", "Estado"};
        tableModel = new DefaultTableModel(columnas, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };
        JTable turnosTable = new JTable(tableModel);
        JScrollPane scrollPane = new JScrollPane(turnosTable);

        buscarButton.addActionListener(e -> {
            Date fecha = (Date) dateSpinner.getValue();
            actualizarTurnos(fecha);
        });

        // Panel inferior con botón volver
        JPanel bottomPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        JButton volverButton = new JButton("Volver");
        volverButton.addActionListener(e -> volverAlMenu());
        bottomPanel.add(volverButton);

        add(topPanel, BorderLayout.NORTH);
        add(scrollPane, BorderLayout.CENTER);
        add(bottomPanel, BorderLayout.SOUTH);

        // Inicializar con la fecha actual
        actualizarTurnos(new Date());
    }

    private void actualizarTurnos(Date fecha) {
        try {
            tableModel.setRowCount(0);
            List<Turno> turnos;
            
            if (medicoId == -1) {
                // Vista de admin: todos los turnos
                turnos = turnoService.obtenerTurnosPorFecha(fecha);
            } else {
                // Vista de médico: solo sus turnos
                turnos = turnoService.obtenerTurnosPorFechaYMedico(fecha, medicoId);
            }

            for (Turno turno : turnos) {
                tableModel.addRow(new Object[]{
                    new SimpleDateFormat("HH:mm").format(turno.getHora()),
                    turno.getMedico().getNombreYApellido(),
                    turno.getPaciente().getNombreYApellido(),
                    turno.getEstado()
                });
            }
        } catch (ServiceException e) {
            JOptionPane.showMessageDialog(this, 
                "Error al cargar turnos: " + e.getMessage(), 
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