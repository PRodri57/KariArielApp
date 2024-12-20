package com.tuempresa.gestorturnos;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.stage.Stage;
import com.tuempresa.gestorturnos.service.TurnoService;
import com.tuempresa.gestorturnos.service.impl.TurnoServiceImpl;
import com.tuempresa.gestorturnos.dao.TurnoDAO;
import com.tuempresa.gestorturnos.dao.impl.TurnoDAOImpl;
import com.tuempresa.gestorturnos.config.FirebaseConfig;
import com.tuempresa.gestorturnos.ui.CalendarioView;
import com.google.cloud.firestore.*;
import com.google.firebase.cloud.FirestoreClient;
import com.google.api.core.ApiFuture;


public class GestorTurnosApp extends Application {
    private TurnoService turnoService;

    @Override
    public void init() {
        FirebaseConfig.inicializar();
        testConexion();
        
        // Inicializar servicios
        TurnoDAO turnoDAO = new TurnoDAOImpl();
        turnoService = new TurnoServiceImpl(turnoDAO);
    }

    private void testConexion() {
        try {
            Firestore db = FirestoreClient.getFirestore();
            ApiFuture<QuerySnapshot> future = db.collection("turnos").limit(1).get();
            future.get();
            System.out.println("Conexión exitosa a Firestore");
        } catch (Exception e) {
            System.err.println("Error de conexión: " + e.getMessage());
            e.printStackTrace();
        }
    }

    @Override
    public void start(Stage primaryStage) {
        CalendarioView calendarioView = new CalendarioView(turnoService);
        
        Scene scene = new Scene(calendarioView, 1024, 768);
        primaryStage.setTitle("Gestor de Turnos");
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
} 