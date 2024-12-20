package com.tuempresa.gestorturnos.ui;

import javafx.scene.layout.BorderPane;
import com.calendarfx.view.CalendarView;
import java.time.LocalDate;
import java.util.List;
import com.calendarfx.model.Entry;
import com.tuempresa.gestorturnos.model.Turno;
import com.tuempresa.gestorturnos.service.TurnoService;
import javafx.scene.control.Alert;
import com.tuempresa.gestorturnos.service.impl.TurnoServiceImpl;
import com.calendarfx.model.Calendar;
import com.tuempresa.gestorturnos.dao.impl.TurnoDAOImpl;
import javafx.scene.control.Button;
import javafx.scene.control.ToolBar;
import java.time.ZoneId;
import com.calendarfx.model.CalendarSource;
import java.util.Map;

public class CalendarioView extends BorderPane {
    private static CalendarioView instance;
    private final TurnoService turnoService;
    private final CalendarView calendario;
    
    public CalendarioView(TurnoService turnoService) {
        this.turnoService = turnoService;
        this.calendario = new CalendarView();
        inicializarCalendario();
        configurarEventos();
    }
    
    public static CalendarioView getInstance() {
        if (instance == null) {
            instance = new CalendarioView(new TurnoServiceImpl(new TurnoDAOImpl()));
        }
        return instance;
    }
    
    private void inicializarCalendario() {
        calendario.setShowAddCalendarButton(false);
        calendario.setShowPrintButton(false);
        calendario.setShowPageToolBarControls(false);
        
        // Crear y agregar un calendario por defecto usando CalendarSource
        CalendarSource source = new CalendarSource("Mis Calendarios");
        Calendar<Turno> calendar = new Calendar<>("Turnos");
        source.getCalendars().add(calendar);
        calendario.getCalendarSources().add(source);
        
        // Crear botones
        Button btnAgregar = new Button("Nuevo Turno");
        Button btnModificar = new Button("Modificar");
        Button btnEliminar = new Button("Eliminar");
        
        // Configurar acciones
        btnAgregar.setOnAction(e -> mostrarDialogoNuevoTurno());
        btnModificar.setOnAction(e -> modificarTurnoSeleccionado());
        btnEliminar.setOnAction(e -> eliminarTurnoSeleccionado());
        
        // Crear toolbar
        ToolBar toolBar = new ToolBar(btnAgregar, btnModificar, btnEliminar);
        
        // Agregar al layout
        setTop(toolBar);
        setCenter(calendario);
        
        // Cargar turnos existentes
        cargarTurnos();
    }

    private void configurarEventos() {
        calendario.setEntryDetailsCallback(param -> {
            Entry<?> entry = param.getEntry();
            Turno turno = (Turno) entry.getUserObject();
            mostrarDetallesTurno(turno);
            return null;
        });
    }

    private void cargarTurnos() {
        try {
            List<Turno> turnos = turnoService.obtenerTodos();
            @SuppressWarnings("unchecked")
            Calendar<Turno> calendar = (Calendar<Turno>) calendario.getCalendarSources()
                .get(0)
                .getCalendars()
                .get(0);
                
            for (Turno turno : turnos) {
                Entry<Turno> entry = new Entry<>("Turno");
                entry.setInterval(turno.getFecha());
                entry.setUserObject(turno);
                calendar.addEntry(entry);
            }
        } catch (Exception e) {
            mostrarError("Error al cargar turnos", e.getMessage());
        }
    }

    private void mostrarDetallesTurno(Turno turno) {
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle("Detalles del Turno");
        alert.setHeaderText("Turno #" + turno.getId());
        alert.setContentText("Fecha y Hora: " + turno.getFecha());
        alert.showAndWait();
    }

    @SuppressWarnings("unchecked")
    public void actualizarTurnos(List<Turno> turnos) {
        Calendar<Turno> calendar = calendario.getCalendars().get(0);
        calendar.clear();
        for (Turno turno : turnos) {
            Entry<Turno> entry = new Entry<>("Turno #" + turno.getId());
            entry.setInterval(turno.getFecha());
            entry.setUserObject(turno);
            calendar.addEntry(entry);
        }
    }

    private void mostrarDialogoNuevoTurno() {
        TurnoDialog dialogo = new TurnoDialog();
        dialogo.showAndWait().ifPresent(turno -> {
            try {
                turnoService.agendarTurno(turno);
                
                // Crear y agregar el evento al calendario
                Entry<Turno> entry = new Entry<>("Turno");
                entry.setInterval(turno.getFecha());
                entry.setUserObject(turno);
                
                // Obtener el calendario "Turnos" y agregar el entry
                @SuppressWarnings("unchecked")
                Calendar<Turno> calendar = (Calendar<Turno>) calendario.getCalendarSources()
                    .get(0)
                    .getCalendars()
                    .get(0);
                calendar.addEntry(entry);
                
            } catch (Exception e) {
                mostrarError("Error al guardar el turno", e.getMessage());
            }
        });
    }

    // Método auxiliar para mostrar errores
    private void mostrarError(String titulo, String mensaje) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle(titulo);
        alert.setHeaderText(null);
        alert.setContentText(mensaje);
        alert.showAndWait();
    }

    @SuppressWarnings("unchecked")
    private void modificarTurnoSeleccionado() {
        Calendar<Turno> calendar = (Calendar<Turno>) calendario.getCalendarSources()
            .get(0)
            .getCalendars()
            .get(0);
        LocalDate date = calendario.getDate();
        Map<LocalDate, List<Entry<?>>> entries = calendar.findEntries(date, date, ZoneId.systemDefault());
        Entry<Turno> selectedEntry = entries.containsKey(date) ? (Entry<Turno>) entries.get(date).get(0) : null;
        
        if (selectedEntry != null) {
            Turno turnoActual = selectedEntry.getUserObject();
            TurnoDialog dialogo = new TurnoDialog(turnoActual);
            dialogo.showAndWait().ifPresent(turnoModificado -> {
                try {
                    turnoService.actualizarTurno(turnoModificado);
                    selectedEntry.setInterval(turnoModificado.getFecha());
                } catch (Exception e) {
                    mostrarError("Error al modificar el turno", e.getMessage());
                }
            });
        }
    }

    @SuppressWarnings("unchecked")
    private void eliminarTurnoSeleccionado() {
        Calendar<Turno> calendar = (Calendar<Turno>) calendario.getCalendarSources()
            .get(0)
            .getCalendars()
            .get(0);
        LocalDate date = calendario.getDate();
        Map<LocalDate, List<Entry<?>>> entries = calendar.findEntries(date, date, ZoneId.systemDefault());
        Entry<Turno> selectedEntry = entries.containsKey(date) ? (Entry<Turno>) entries.get(date).get(0) : null;
        
        if (selectedEntry != null) {
            Turno turno = selectedEntry.getUserObject();
            try {
                turnoService.eliminarTurno(turno.getId());
                
                // Eliminar la entrada del calendario
                calendar.removeEntry(selectedEntry);
                
            } catch (Exception e) {
                mostrarError("Error al eliminar el turno", e.getMessage());
            }
        }
    }
} 