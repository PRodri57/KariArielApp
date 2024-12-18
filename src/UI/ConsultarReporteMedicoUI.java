package UI;

import Model.Medico;
import Model.Turno;
import Service.MedicoService;
import Service.TurnoService;
import Service.ServiceException;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.util.List;
import java.util.Date;

public class ConsultarReporteMedicoUI extends JPanel {
    private TurnoService turnoService;
    private MedicoService medicoService;
    private int medicoId;  // -1 para admin (selector de médico), otro valor para médico específico
    private JComboBox<Medico> medicoCombo;
    private DefaultTableModel tableModel;

    public ConsultarReporteMedicoUI(TurnoService turnoService, MedicoService medicoService, int medicoId) {
        this.turnoService = turnoService;
        this.medicoService = medicoService;
        this.medicoId = medicoId;
        initComponents();
    }

    private void initComponents() {
        setLayout(new BorderLayout());
        setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // Panel superior
        JPanel topPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));

        // Selector de médico solo para admin
        if (medicoId == -1) {
            topPanel.add(new JLabel("Médico:"));
            medicoCombo = new JComboBox<>();
            cargarMedicos();
            topPanel.add(medicoCombo);
        }

        // Selectores de fecha
        topPanel.add(new JLabel("Fecha Inicio:"));
        SpinnerDateModel modelInicio = new SpinnerDateModel();
        JSpinner fechaInicioSpinner = new JSpinner(modelInicio);
        JSpinner.DateEditor editorInicio = new JSpinner.DateEditor(fechaInicioSpinner, "dd/MM/yyyy");
        fechaInicioSpinner.setEditor(editorInicio);
        fechaInicioSpinner.setValue(new Date());
        topPanel.add(fechaInicioSpinner);

        topPanel.add(new JLabel("Fecha Fin:"));
        SpinnerDateModel modelFin = new SpinnerDateModel();
        JSpinner fechaFinSpinner = new JSpinner(modelFin);
        JSpinner.DateEditor editorFin = new JSpinner.DateEditor(fechaFinSpinner, "dd/MM/yyyy");
        fechaFinSpinner.setEditor(editorFin);
        fechaFinSpinner.setValue(new Date());
        topPanel.add(fechaFinSpinner);

        JButton generarButton = new JButton("Generar Reporte");
        generarButton.addActionListener(e -> {
            Date fechaInicio = (Date) fechaInicioSpinner.getValue();
            Date fechaFin = (Date) fechaFinSpinner.getValue();
            generarReporte(fechaInicio, fechaFin);
        });
        topPanel.add(generarButton);

        // Tabla de reporte
        String[] columnas = {"Médico", "Cantidad de Turnos", "Total Cobrado"};
        tableModel = new DefaultTableModel(columnas, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };
        JTable reporteTable = new JTable(tableModel);
        JScrollPane scrollPane = new JScrollPane(reporteTable);

        // Panel inferior con botón volver
        JPanel bottomPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        JButton volverButton = new JButton("Volver");
        volverButton.addActionListener(e -> volverAlMenu());
        bottomPanel.add(volverButton);

        add(topPanel, BorderLayout.NORTH);
        add(scrollPane, BorderLayout.CENTER);
        add(bottomPanel, BorderLayout.SOUTH);
    }

    private void cargarMedicos() {
        try {
            List<Medico> medicos = medicoService.obtenerTodos();
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

    private void generarReporte(Date fechaInicio, Date fechaFin) {
        try {
            int medicoIdReporte = medicoId == -1 ? 
                ((Medico) medicoCombo.getSelectedItem()).getId() : 
                medicoId;
            
            Medico medico = medicoService.obtenerPorId(medicoIdReporte);
            List<Turno> turnos = turnoService.obtenerTurnosEntreFechas(medicoIdReporte, fechaInicio, fechaFin);
            
            tableModel.setRowCount(0);
            double totalCobrado = turnos.size() * medico.getValorConsulta();
            
            tableModel.addRow(new Object[]{
                medico.getNombreYApellido(),
                turnos.size(),
                String.format("$%.2f", totalCobrado)
            });
        } catch (ServiceException e) {
            JOptionPane.showMessageDialog(this, 
                "Error al generar reporte: " + e.getMessage(), 
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