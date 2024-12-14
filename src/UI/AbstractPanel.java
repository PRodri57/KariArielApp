package UI;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;

public abstract class AbstractPanel<T> extends JPanel {
    protected JTextField idField;
    protected JTextField nombreYApellidoField;
    protected JTextField dniField;
    protected JTextField telefonoField;
    protected JTextField emailField;
    protected JTextField obraSocialField;
    protected JButton agregarButton;
    protected JButton modificarButton;
    protected JButton eliminarButton;
    protected JButton volverButton;
    protected JTable tablaPacientes;
    protected DefaultTableModel tableModel;
    private PacientePanelManager pacientePanelManager;


    public AbstractPanel() {
        this.tableModel = new DefaultTableModel(new Object[]{"ID", "Nombre y Apellido", "DNI", "Teléfono", "Email", "Obra Social"}, 0);
        this.tablaPacientes = new JTable(tableModel);
        initComponents();
        setUpLayout();
    }

    protected void initComponents() {
        idField = new JTextField(10);
        nombreYApellidoField = new JTextField(10);
        dniField = new JTextField(10);
        telefonoField = new JTextField(10);
        emailField = new JTextField(10);
        obraSocialField = new JTextField(10);

        agregarButton = new JButton("Agregar");
        modificarButton = new JButton("Modificar");
        eliminarButton = new JButton("Eliminar");
        volverButton = new JButton("Volver");

        agregarButton.addActionListener(e -> agregarItem());
        modificarButton.addActionListener(e -> modificarItem());
        eliminarButton.addActionListener(e -> eliminarItem());
        volverButton.addActionListener(e -> volver());
    }

    protected void setUpLayout() {
        setLayout(new BorderLayout());

        JPanel formPanel = new JPanel(new GridLayout(0, 2));
        armarFormulario(formPanel);
        add(formPanel, BorderLayout.NORTH);

        JPanel buttonPanel = new JPanel();
        buttonPanel.add(agregarButton);
        buttonPanel.add(modificarButton);
        buttonPanel.add(eliminarButton);
        buttonPanel.add(volverButton);
        add(buttonPanel, BorderLayout.SOUTH);

        // Configurar la tabla
        tableModel = new DefaultTableModel(new Object[]{"ID", "Nombre y Apellido", "DNI", "Teléfono", "Email", "Obra Social"}, 0);
        tablaPacientes = new JTable(tableModel);
        JScrollPane scrollPane = new JScrollPane(tablaPacientes);
        add(scrollPane, BorderLayout.CENTER);
    }

    protected abstract void armarFormulario(JPanel formPanel);

    protected abstract void agregarItem();

    protected abstract void modificarItem();

    protected abstract void eliminarItem();

    protected abstract void actualizarTabla();

    protected abstract void clearForm();

    public abstract void setFormData(int id, String nombreApellido, String dni, String telefono, String email, String obraSocial);

    protected void volver() {
        pacientePanelManager.mostrarPanel("mainPanel");
    }

}