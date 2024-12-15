package UI;

import Model.Turno;
import Service.TurnoService;
import Service.ServiceException;

import javax.swing.*;
import java.awt.*;
import java.text.SimpleDateFormat;
import java.util.List;
import java.util.Calendar;
import java.util.Date;
import java.util.ArrayList;

public class CalendarioTurnosUI extends JPanel {
    private TurnoService turnoService;
    private JPanel calendarioPanel;
    private JComboBox<String> mesCombo;
    private JSpinner anioSpinner;
    private List<Turno> turnos;
    private SimpleDateFormat dateFormat = new SimpleDateFormat("dd/MM/yyyy");
    private SimpleDateFormat timeFormat = new SimpleDateFormat("HH:mm");

    public CalendarioTurnosUI(TurnoService turnoService) {
        this.turnoService = turnoService;
        this.turnos = new ArrayList<>();
        cargarTurnos();
        initComponents();
    }

    private void initComponents() {
        setLayout(new BorderLayout());

        // Panel superior para controles
        JPanel controlPanel = new JPanel();
        String[] meses = {"Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"};
        mesCombo = new JComboBox<>(meses);
        Calendar cal = Calendar.getInstance();
        mesCombo.setSelectedIndex(cal.get(Calendar.MONTH));

        SpinnerNumberModel yearModel = new SpinnerNumberModel(cal.get(Calendar.YEAR), 
                                                            cal.get(Calendar.YEAR) - 1, 
                                                            cal.get(Calendar.YEAR) + 1, 1);
        anioSpinner = new JSpinner(yearModel);

        controlPanel.add(new JLabel("Mes:"));
        controlPanel.add(mesCombo);
        controlPanel.add(new JLabel("Año:"));
        controlPanel.add(anioSpinner);

        JButton actualizarButton = new JButton("Actualizar");
        actualizarButton.addActionListener(e -> actualizarCalendario());
        controlPanel.add(actualizarButton);

        add(controlPanel, BorderLayout.NORTH);

        // Panel del calendario
        calendarioPanel = new JPanel(new GridLayout(0, 7, 2, 2));
        actualizarCalendario();
        JScrollPane scrollPane = new JScrollPane(calendarioPanel);
        add(scrollPane, BorderLayout.CENTER);

        // Botón volver
        JButton volverButton = new JButton("Volver");
        volverButton.addActionListener(e -> volverAlPanel());
        add(volverButton, BorderLayout.SOUTH);
    }

    private void actualizarCalendario() {
        calendarioPanel.removeAll();
        
        // Agregar nombres de días
        String[] diasSemana = {"Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"};
        for (String dia : diasSemana) {
            JLabel label = new JLabel(dia, SwingConstants.CENTER);
            label.setBorder(BorderFactory.createLineBorder(Color.BLACK));
            calendarioPanel.add(label);
        }

        Calendar calendar = Calendar.getInstance();
        calendar.set(Calendar.YEAR, (Integer) anioSpinner.getValue());
        calendar.set(Calendar.MONTH, mesCombo.getSelectedIndex());
        calendar.set(Calendar.DAY_OF_MONTH, 1);

        // Ajustar el primer día de la semana
        int primerDia = calendar.get(Calendar.DAY_OF_WEEK) - 1;
        for (int i = 0; i < primerDia; i++) {
            calendarioPanel.add(new JLabel(""));
        }

        // Agregar días del mes
        int ultimoDia = calendar.getActualMaximum(Calendar.DAY_OF_MONTH);
        for (int dia = 1; dia <= ultimoDia; dia++) {
            JPanel diaPanel = new JPanel(new BorderLayout());
            diaPanel.setBorder(BorderFactory.createLineBorder(Color.BLACK));
            
            JLabel numeroLabel = new JLabel(String.valueOf(dia), SwingConstants.CENTER);
            diaPanel.add(numeroLabel, BorderLayout.NORTH);
            
            // Buscar turnos para este día
            JPanel turnosPanel = new JPanel();
            turnosPanel.setLayout(new BoxLayout(turnosPanel, BoxLayout.Y_AXIS));
            calendar.set(Calendar.DAY_OF_MONTH, dia);
            Date fecha = calendar.getTime();
            
            for (Turno turno : turnos) {
                if (dateFormat.format(turno.getFecha()).equals(dateFormat.format(fecha))) {
                    JLabel turnoLabel = new JLabel(
                        timeFormat.format(turno.getHora()) + " - " + 
                        turno.getPaciente().getNombreYApellido()
                    );
                    turnoLabel.setFont(new Font("Arial", Font.PLAIN, 10));
                    turnosPanel.add(turnoLabel);
                }
            }
            
            JScrollPane scrollPane = new JScrollPane(turnosPanel);
            scrollPane.setPreferredSize(new Dimension(100, 80));
            diaPanel.add(scrollPane, BorderLayout.CENTER);
            
            calendarioPanel.add(diaPanel);
        }

        calendarioPanel.revalidate();
        calendarioPanel.repaint();
    }

    private void cargarTurnos() {
        try {
            turnos = turnoService.obtenerTodos();
        } catch (ServiceException e) {
            JOptionPane.showMessageDialog(this, 
                "Error al cargar turnos: " + e.getMessage(), 
                "Error", 
                JOptionPane.ERROR_MESSAGE);
            turnos = new ArrayList<>();
        }
    }

    private void volverAlPanel() {
        Container parent = this.getParent();
        if (parent instanceof JPanel) {
            CardLayout cl = (CardLayout) parent.getLayout();
            cl.show(parent, "menu");
        }
    }
} 