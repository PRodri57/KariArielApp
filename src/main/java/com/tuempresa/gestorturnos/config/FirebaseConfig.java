package com.tuempresa.gestorturnos.config;

import com.google.auth.oauth2.GoogleCredentials;
import com.google.firebase.FirebaseApp;
import com.google.firebase.FirebaseOptions;
import java.io.FileInputStream;
import java.io.IOException;

public class FirebaseConfig {
    private static FirebaseApp firebaseApp;

    public static void inicializar() {
        try {
            if (FirebaseApp.getApps().isEmpty()) {
                FileInputStream serviceAccount = new FileInputStream("kariariel-firebase-adminsdk-4vok9-ada368d1dc.json");

                FirebaseOptions options = FirebaseOptions.builder()
                    .setCredentials(GoogleCredentials.fromStream(serviceAccount))
                    .setDatabaseUrl("https://kariariel-default-rtdb.firebaseio.com")
                    .build();

                firebaseApp = FirebaseApp.initializeApp(options);
            }
        } catch (IOException e) {
            throw new RuntimeException("Error al inicializar Firebase", e);
        }
    }

    public static FirebaseApp getFirebaseApp() {
        if (firebaseApp == null) {
            inicializar();
        }
        return firebaseApp;
    }
} 