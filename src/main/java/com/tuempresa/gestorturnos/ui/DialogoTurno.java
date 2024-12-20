package com.tuempresa.gestorturnos.ui;

import javafx.scene.control.*;
import javafx.scene.layout.*;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.Optional;
import com.tuempresa.gestorturnos.model.Turno;

public class DialogoTurno {
    public Optional<Turno> mostrarDialogo() {
        Dialog<Turno> dialog = new Dialog<>();
        dialog.setTitle("Nuevo Turno");
        
        DatePicker datePicker = new DatePicker();
        ComboBox<String> horaCombo = new ComboBox<>();
        
        // Agregar horas disponibles (formato 24h)
        for (int i = 8; i <= 20; i++) {
            horaCombo.getItems().add(String.format("%02d:00", i));
        }
        
        VBox content = new VBox(10);
        content.getChildren().addAll(
            new Label("Fecha:"), 
            datePicker,
            new Label("Hora:"),
            horaCombo
        );
        
        dialog.getDialogPane().setContent(content);
        dialog.getDialogPane().getButtonTypes().addAll(ButtonType.OK, ButtonType.CANCEL);
        
        dialog.setResultConverter(dialogButton -> {
            if (dialogButton == ButtonType.OK && datePicker.getValue() != null && horaCombo.getValue() != null) {
                Turno turno = new Turno();
                String[] horaParts = horaCombo.getValue().split(":");
                LocalTime time = LocalTime.of(Integer.parseInt(horaParts[0]), Integer.parseInt(horaParts[1]));
                turno.setFecha(LocalDateTime.of(datePicker.getValue(), time));
                return turno;
            }
            return null;
        });
        
        return dialog.showAndWait();
    }
} 