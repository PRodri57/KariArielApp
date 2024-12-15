package UI;

import Model.Medico;
import Model.Turno;
import Service.MedicoService;
import Service.TurnoService;
import Service.ServiceException;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.util.Date;
import java.util.List;
import java.util.Calendar;
import java.text.SimpleDateFormat;

public class ReporteMedicoUI extends JPanel {
    private TurnoService turnoService;
    private MedicoService medicoService;
    private JComboBox<Medico> medicoCombo;
    private JTable reporteTable;
    private DefaultTableModel tableModel;
    private JSpinner fechaInicioSpinner;
    private JSpinner fechaFinSpinner;
    private static final double VALOR_CONSULTA = 5000.0; // Valor fijo por consulta

    public ReporteMedicoUI(TurnoService turnoService, MedicoService medicoService) {
        this.turnoService = turnoService;
        this.medicoService = medicoService;
        initComponents();
    }

    private void initComponents() {
        setLayout(new BorderLayout());

        // Panel de filtros
        JPanel filtrosPanel = new JPanel(new FlowLayout());

        // Selector de médico
        filtrosPanel.add(new JLabel("Médico:"));
        medicoCombo = new JComboBox<>();
        cargarMedicos();
        filtrosPanel.add(medicoCombo);

        // Selectores de fecha
        Calendar cal = Calendar.getInstance();
        Date now = cal.getTime();
        cal.add(Calendar.MONTH, -1);
        Date monthAgo = cal.getTime();

        SpinnerDateModel modelInicio = new SpinnerDateModel(monthAgo, null, null, Calendar.DAY_OF_MONTH);
        SpinnerDateModel modelFin = new SpinnerDateModel(now, null, null, Calendar.DAY_OF_MONTH);
        
        filtrosPanel.add(new JLabel("Fecha Inicio:"));
        fechaInicioSpinner = new JSpinner(modelInicio);
        fechaInicioSpinner.setEditor(new JSpinner.DateEditor(fechaInicioSpinner, "dd/MM/yyyy"));
        filtrosPanel.add(fechaInicioSpinner);

        filtrosPanel.add(new JLabel("Fecha Fin:"));
        fechaFinSpinner = new JSpinner(modelFin);
        fechaFinSpinner.setEditor(new JSpinner.DateEditor(fechaFinSpinner, "dd/MM/yyyy"));
        filtrosPanel.add(fechaFinSpinner);

        JButton generarButton = new JButton("Generar Reporte");
        generarButton.addActionListener(e -> generarReporte());
        filtrosPanel.add(generarButton);

        add(filtrosPanel, BorderLayout.NORTH);

        // Tabla de reporte
        tableModel = new DefaultTableModel(
            new Object[]{"Médico", "Cantidad de Turnos", "Total Cobrado"}, 
            0
        ) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };

        reporteTable = new JTable(tableModel);
        JScrollPane scrollPane = new JScrollPane(reporteTable);
        add(scrollPane, BorderLayout.CENTER);

        // Botón volver
        JButton volverButton = new JButton("Volver");
        volverButton.addActionListener(e -> volverAlMenu());
        add(volverButton, BorderLayout.SOUTH);
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

    private void generarReporte() {
        try {
            Medico medico = (Medico) medicoCombo.getSelectedItem();
            Date fechaInicio = (Date) fechaInicioSpinner.getValue();
            Date fechaFin = (Date) fechaFinSpinner.getValue();

            if (medico == null) {
                JOptionPane.showMessageDialog(this, "Por favor seleccione un médico");
                return;
            }

            List<Turno> turnos = turnoService.obtenerTurnosEntreFechas(
                medico.getId(), fechaInicio, fechaFin);

            tableModel.setRowCount(0);
            double totalCobrado = turnos.size() * VALOR_CONSULTA;

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
        Container parent = this.getParent();
        if (parent instanceof JPanel) {
            CardLayout cl = (CardLayout) parent.getLayout();
            cl.show(parent, "menu");
        }
    }
} 