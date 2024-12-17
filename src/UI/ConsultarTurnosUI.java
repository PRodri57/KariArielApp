package UI;

import Model.Turno;
import Service.TurnoService;
import Service.ServiceException;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
//import java.util.Date;
import java.text.SimpleDateFormat;
import java.util.List;
//import java.util.Calendar;

public class ConsultarTurnosUI extends JPanel {
    private TurnoService turnoService;
    private int id;
    private JTable turnosTable;
    private DefaultTableModel tableModel;

    public ConsultarTurnosUI(TurnoService turnoService, int id) {
        this.turnoService = turnoService;
        this.id = id;
        initComponents();
        cargarTurnos();
    }

    private void initComponents() {
        setLayout(new BorderLayout());

        // Tabla de turnos
        tableModel = new DefaultTableModel(
            new Object[]{"Fecha", "Hora", "Médico", "Paciente", "Estado"}, 
            0
        ) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };

        turnosTable = new JTable(tableModel);
        JScrollPane scrollPane = new JScrollPane(turnosTable);
        add(scrollPane, BorderLayout.CENTER);

        // Panel para el botón volver
        JPanel buttonPanel = new JPanel();
        JButton volverButton = new JButton("Volver");
        volverButton.addActionListener(e -> volverAlPanel());
        buttonPanel.add(volverButton);
        add(buttonPanel, BorderLayout.SOUTH);
    }

    private void cargarTurnos() {
        try {
            List<Turno> turnos;
            // Si es un médico
            if (id > 0) {
                turnos = turnoService.obtenerTodosPorMedico(id);
            } else {
                // Si es un paciente
                turnos = turnoService.obtenerTodosPorPaciente(id);
            }
            actualizarTabla(turnos);
        } catch (ServiceException e) {
            JOptionPane.showMessageDialog(this, 
                "Error al cargar turnos: " + e.getMessage(), 
                "Error", 
                JOptionPane.ERROR_MESSAGE);
        }
    }

    private void actualizarTabla(List<Turno> turnos) {
        tableModel.setRowCount(0);
        SimpleDateFormat dateFormat = new SimpleDateFormat("dd/MM/yyyy");
        SimpleDateFormat timeFormat = new SimpleDateFormat("HH:mm");

        for (Turno turno : turnos) {
            tableModel.addRow(new Object[]{
                dateFormat.format(turno.getFecha()),
                timeFormat.format(turno.getHora()),
                turno.getMedico().getNombreYApellido(),
                turno.getPaciente().getNombreYApellido(),
                turno.getEstado()
            });
        }
    }

    private void volverAlPanel() {
        Container parent = this.getParent();
        if (parent instanceof JPanel) {
            CardLayout cl = (CardLayout) parent.getLayout();
            cl.show(parent, "mainPanel");
        }
    }

    public void actualizarTurnos() {
        cargarTurnos();
    }
}
