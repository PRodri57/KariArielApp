package UI;

import Model.Turno;
import Service.TurnoService;
import Service.ServiceException;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.text.SimpleDateFormat;
import java.util.List;

public class TurnosPacienteUI extends JPanel {
    private TurnoService turnoService;
    private int pacienteId;
    private DefaultTableModel tableModel;
    private JTable turnosTable;

    public TurnosPacienteUI(TurnoService turnoService, int pacienteId) {
        this.turnoService = turnoService;
        this.pacienteId = pacienteId;
        initComponents();
        cargarTurnos();
    }

    private void initComponents() {
        setLayout(new BorderLayout(10, 10));
        setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // Título
        JLabel titleLabel = new JLabel("Mis Turnos", SwingConstants.CENTER);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 20));
        add(titleLabel, BorderLayout.NORTH);

        // Tabla de turnos
        String[] columnas = {"Fecha", "Hora", "Médico", "Especialidad", "Estado"};
        tableModel = new DefaultTableModel(columnas, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };
        turnosTable = new JTable(tableModel);
        JScrollPane scrollPane = new JScrollPane(turnosTable);
        add(scrollPane, BorderLayout.CENTER);

        // Panel de botones
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        
        JButton actualizarButton = new JButton("Actualizar");
        actualizarButton.addActionListener(e -> cargarTurnos());
        
        JButton volverButton = new JButton("Volver");
        volverButton.addActionListener(e -> volverAlMenu());
        
        buttonPanel.add(actualizarButton);
        buttonPanel.add(volverButton);
        add(buttonPanel, BorderLayout.SOUTH);
    }

    private void cargarTurnos() {
        try {
            List<Turno> turnos = turnoService.obtenerTodosPorPaciente(pacienteId);
            tableModel.setRowCount(0);
            SimpleDateFormat dateFormat = new SimpleDateFormat("dd/MM/yyyy");
            SimpleDateFormat timeFormat = new SimpleDateFormat("HH:mm");

            for (Turno turno : turnos) {
                tableModel.addRow(new Object[]{
                    dateFormat.format(turno.getFecha()),
                    timeFormat.format(turno.getHora()),
                    turno.getMedico().getNombreYApellido(),
                    turno.getMedico().getEspecialidad(),
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