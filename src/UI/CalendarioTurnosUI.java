package UI;

import Model.Turno;
import Service.TurnoService;
import Service.ServiceException;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.text.SimpleDateFormat;
import java.util.*;
import java.util.List;

public class CalendarioTurnosUI extends JPanel {
    private TurnoService turnoService;
    private int medicoId;
    private DefaultTableModel tableModel;
    private Date fechaActual;
    private JLabel semanaLabel;

    public CalendarioTurnosUI(TurnoService turnoService, int medicoId) {
        this.turnoService = turnoService;
        this.medicoId = medicoId;
        this.fechaActual = new Date();
        initComponents();
    }

    private void initComponents() {
        setLayout(new BorderLayout());
        setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // Panel superior con navegación
        JPanel topPanel = new JPanel(new FlowLayout(FlowLayout.CENTER));
        
        JButton prevButton = new JButton("Semana Anterior");
        semanaLabel = new JLabel();
        JButton nextButton = new JButton("Semana Siguiente");
        
        prevButton.addActionListener(e -> cambiarSemana(-1));
        nextButton.addActionListener(e -> cambiarSemana(1));
        
        topPanel.add(prevButton);
        topPanel.add(semanaLabel);
        topPanel.add(nextButton);

        // Configurar tabla
        tableModel = new DefaultTableModel() {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };
        JTable turnosTable = new JTable(tableModel);
        turnosTable.setRowHeight(50);
        JScrollPane scrollPane = new JScrollPane(turnosTable);

        // Panel inferior con botón volver
        JPanel bottomPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        JButton volverButton = new JButton("Volver");
        volverButton.addActionListener(e -> volverAlMenu());
        bottomPanel.add(volverButton);

        add(topPanel, BorderLayout.NORTH);
        add(scrollPane, BorderLayout.CENTER);
        add(bottomPanel, BorderLayout.SOUTH);

        // Inicializar con la semana actual
        actualizarCalendario();
    }

    private void cambiarSemana(int direccion) {
        Calendar cal = Calendar.getInstance();
        cal.setTime(fechaActual);
        cal.add(Calendar.WEEK_OF_YEAR, direccion);
        fechaActual = cal.getTime();
        actualizarCalendario();
    }

    private void actualizarCalendario() {
        // Configurar columnas
        tableModel.setColumnCount(0);
        tableModel.addColumn("Hora");
        
        // Obtener fechas de la semana
        Calendar cal = Calendar.getInstance();
        cal.setTime(fechaActual);
        cal.set(Calendar.DAY_OF_WEEK, cal.getFirstDayOfWeek());
        
        SimpleDateFormat columnFormat = new SimpleDateFormat("EEE dd/MM");
        SimpleDateFormat labelFormat = new SimpleDateFormat("dd/MM/yyyy");
        
        // Guardar la fecha de inicio y fin para el label
        String inicioSemana = labelFormat.format(cal.getTime());
        
        // Agregar columnas para cada día
        for (int i = 0; i < 7; i++) {
            tableModel.addColumn(columnFormat.format(cal.getTime()));
            cal.add(Calendar.DAY_OF_WEEK, 1);
        }
        
        // Actualizar label de la semana
        cal.add(Calendar.DAY_OF_WEEK, -1);
        String finSemana = labelFormat.format(cal.getTime());
        semanaLabel.setText("Semana: " + inicioSemana + " - " + finSemana);

        // Limpiar filas existentes
        tableModel.setRowCount(0);

        // Crear filas para cada horario (de 8:00 a 20:00 cada 30 minutos)
        Calendar horaCal = Calendar.getInstance();
        horaCal.set(Calendar.HOUR_OF_DAY, 8);
        horaCal.set(Calendar.MINUTE, 0);
        SimpleDateFormat horaFormat = new SimpleDateFormat("HH:mm");

        while (horaCal.get(Calendar.HOUR_OF_DAY) < 20) {
            Vector<String> fila = new Vector<>();
            fila.add(horaFormat.format(horaCal.getTime()));

            // Volver al inicio de la semana
            cal.setTime(fechaActual);
            cal.set(Calendar.DAY_OF_WEEK, cal.getFirstDayOfWeek());

            // Para cada día de la semana
            for (int i = 0; i < 7; i++) {
                StringBuilder celda = new StringBuilder();
                try {
                    List<Turno> turnos;
                    if (medicoId == -1) {
                        turnos = turnoService.obtenerTurnosPorFecha(cal.getTime());
                    } else {
                        turnos = turnoService.obtenerTurnosPorFechaYMedico(cal.getTime(), medicoId);
                    }

                    for (Turno turno : turnos) {
                        Calendar turnoHora = Calendar.getInstance();
                        turnoHora.setTime(turno.getHora());
                        
                        // Calcular la diferencia en minutos entre el turno y el horario actual
                        long diffMinutos = Math.abs(
                            (turnoHora.get(Calendar.HOUR_OF_DAY) * 60 + turnoHora.get(Calendar.MINUTE)) -
                            (horaCal.get(Calendar.HOUR_OF_DAY) * 60 + horaCal.get(Calendar.MINUTE))
                        );
                        
                        // Si el turno está dentro de los 15 minutos antes o después del horario actual
                        if (diffMinutos <= 15) {
                            if (celda.length() > 0) {
                                celda.append("\n");
                            }
                            celda.append(horaFormat.format(turno.getHora()))
                                .append(" - ")
                                .append(turno.getPaciente().getNombreYApellido());
                            if (medicoId == -1) {
                                celda.append(" (").append(turno.getMedico().getNombreYApellido()).append(")");
                            }
                            celda.append(" - ").append(turno.getEstado());
                        }
                    }
                } catch (ServiceException e) {
                    celda.append("Error al cargar turnos");
                }
                fila.add(celda.toString());
                cal.add(Calendar.DAY_OF_WEEK, 1);
            }

            tableModel.addRow(fila);
            horaCal.add(Calendar.MINUTE, 30);
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