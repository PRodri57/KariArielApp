package com.tuempresa.gestorturnos.ui;

import javafx.scene.control.*;
import javafx.scene.layout.GridPane;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.LocalDate;
import javafx.scene.control.ButtonType;
import com.tuempresa.gestorturnos.model.Turno;

public class TurnoDialog extends Dialog<Turno> {
    private final DatePicker datePicker = new DatePicker();
    private final ComboBox<LocalTime> timeComboBox = new ComboBox<>();
    
    public TurnoDialog() {
        this(null);
    }
    
    public TurnoDialog(Turno turno) {
        setTitle(turno == null ? "Nuevo Turno" : "Modificar Turno");
        
        // Configurar campos
        datePicker.setValue(turno != null ? turno.getFecha().toLocalDate() : LocalDate.now());
        
        // Poblar combobox con horarios disponibles (cada 30 minutos)
        LocalTime inicio = LocalTime.of(8, 0);
        LocalTime fin = LocalTime.of(18, 0);
        while (inicio.isBefore(fin)) {
            timeComboBox.getItems().add(inicio);
            inicio = inicio.plusMinutes(30);
        }
        
        if (turno != null) {
            timeComboBox.setValue(turno.getFecha().toLocalTime());
        }
        
        // Layout
        GridPane grid = new GridPane();
        grid.setHgap(10);
        grid.setVgap(10);
        grid.add(new Label("Fecha:"), 0, 0);
        grid.add(datePicker, 1, 0);
        grid.add(new Label("Hora:"), 0, 1);
        grid.add(timeComboBox, 1, 1);
        
        getDialogPane().setContent(grid);
        getDialogPane().getButtonTypes().addAll(ButtonType.OK, ButtonType.CANCEL);
        
        // Convertir resultado
        setResultConverter(buttonType -> {
            if (buttonType == ButtonType.OK) {
                Turno nuevoTurno = turno != null ? turno : new Turno();
                LocalDateTime fechaHora = LocalDateTime.of(
                    datePicker.getValue(),
                    timeComboBox.getValue()
                );
                nuevoTurno.setFecha(fechaHora);
                return nuevoTurno;
            }
            return null;
        });
    }
} 