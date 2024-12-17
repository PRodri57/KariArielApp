package UI;

import Model.Usuario;
import Service.UsuarioService;
import Service.ServiceException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import javax.swing.*;
import java.awt.*;
import DAO.UsuarioDAOImpl;
import Service.UsuarioServiceImpl;

public class LoginUI extends JFrame {
    private UsuarioService usuarioService;
    private JTextField usernameField;
    private JPasswordField passwordField;

    public LoginUI(UsuarioService usuarioService) {
        this.usuarioService = usuarioService;
        initComponents();
    }

    private void initComponents() {
        setTitle("Login - Sistema de Gestión Médica");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(300, 200);
        setLocationRelativeTo(null);

        JPanel mainPanel = new JPanel(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5);

        // Username
        gbc.gridx = 0;
        gbc.gridy = 0;
        mainPanel.add(new JLabel("Usuario:"), gbc);

        gbc.gridx = 1;
        usernameField = new JTextField(15);
        mainPanel.add(usernameField, gbc);

        // Password
        gbc.gridx = 0;
        gbc.gridy = 1;
        mainPanel.add(new JLabel("Contraseña:"), gbc);

        gbc.gridx = 1;
        passwordField = new JPasswordField(15);
        mainPanel.add(passwordField, gbc);

        // Login button
        gbc.gridx = 0;
        gbc.gridy = 2;
        gbc.gridwidth = 2;
        JButton loginButton = new JButton("Ingresar");
        loginButton.addActionListener(e -> login());
        mainPanel.add(loginButton, gbc);

        add(mainPanel);
    }

    private void login() {
        String username = usernameField.getText();
        String password = new String(passwordField.getPassword());

        try {
            Usuario usuario = usuarioService.autenticar(username, password);
            if (usuario != null) {
                MainMenuUI mainMenu = new MainMenuUI(usuario);
                mainMenu.mostrarMenuPrincipal();
                this.dispose();
            } else {
                JOptionPane.showMessageDialog(this, 
                    "Usuario o contraseña incorrectos", 
                    "Error de autenticación", 
                    JOptionPane.ERROR_MESSAGE);
            }
        } catch (ServiceException e) {
            JOptionPane.showMessageDialog(this, 
                "Error al intentar iniciar sesión: " + e.getMessage(), 
                "Error", 
                JOptionPane.ERROR_MESSAGE);
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                // Configurar la conexión y servicios
                Connection conexion = DriverManager.getConnection(
                    "jdbc:h2:./database/TurneraMedica", 
                    "sa", 
                    ""
                );
                UsuarioService usuarioService = new UsuarioServiceImpl(new UsuarioDAOImpl(conexion));
                new LoginUI(usuarioService).setVisible(true);
            } catch (SQLException e) {
                JOptionPane.showMessageDialog(null, 
                    "Error de conexión a la base de datos: " + e.getMessage(), 
                    "Error", 
                    JOptionPane.ERROR_MESSAGE);
                System.exit(1);
            }
        });
    }
} 