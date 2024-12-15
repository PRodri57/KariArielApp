package UI;

import Service.ServiceException;
import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.sql.Connection;
import Service.TurnoService;
import Service.TurnoServiceImpl;
import DAO.TurnoDAOImpl;

public abstract class AbstractPanelManager {
    protected MainMenuUI mainMenuUI;
    protected JPanel mainPanel;
    protected JPanel contentPanel;
    protected CardLayout cardLayout;
    protected JTable table;
    protected DefaultTableModel tableModel;
    protected Connection conexion;

    public AbstractPanelManager(MainMenuUI mainMenuUI, Connection conexion) {
        this.mainMenuUI = mainMenuUI;
        this.conexion = conexion;
        cardLayout = new CardLayout();
        contentPanel = new JPanel(cardLayout);
    }

    protected void init() {
        initDAO();
        initComponents();
        initUIComponents();
    }

    private void initComponents() {
        // Crear panel principal
        mainPanel = new JPanel(new BorderLayout());
        
        // Crear y configurar la tabla
        table = new JTable(tableModel);
        table.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        table.getSelectionModel().addListSelectionListener(e -> actualizarFormulariosConSeleccion());
        JScrollPane scrollPane = new JScrollPane(table);
        mainPanel.add(scrollPane, BorderLayout.CENTER);
        
        // Panel de botones
        JPanel buttonPanel = new JPanel();
        JButton agregarButton = new JButton("Agregar");
        JButton modificarButton = new JButton("Modificar");
        JButton eliminarButton = new JButton("Eliminar");
        JButton buscarButton = new JButton("Buscar por Email");
        JButton volverButton = new JButton("Volver al Menú");
        JButton consultarTurnosButton = new JButton("Consultar Turnos");
        
        agregarButton.addActionListener(e -> mostrarPanel("agregar"));
        modificarButton.addActionListener(e -> {
            if (table.getSelectedRow() != -1) {
                mostrarPanel("modificar");
            } else {
                JOptionPane.showMessageDialog(null, "Por favor, seleccione una fila para modificar");
            }
        });
        eliminarButton.addActionListener(e -> {
            if (table.getSelectedRow() != -1) {
                mostrarPanel("eliminar");
            } else {
                JOptionPane.showMessageDialog(null, "Por favor, seleccione una fila para eliminar");
            }
        });
        buscarButton.addActionListener(e -> buscarPorEmail());
        volverButton.addActionListener(e -> volverAlMenuPrincipal());
        consultarTurnosButton.addActionListener(e -> consultarTurnos());
        
        buttonPanel.add(agregarButton);
        buttonPanel.add(modificarButton);
        buttonPanel.add(eliminarButton);
        buttonPanel.add(buscarButton);
        buttonPanel.add(volverButton);
        buttonPanel.add(consultarTurnosButton);
        
        mainPanel.add(buttonPanel, BorderLayout.NORTH);
        
        // Agregar el panel principal al contentPanel
        contentPanel.add(mainPanel, "mainPanel");
        
        try {
            actualizarTabla();
        } catch (ServiceException e) {
            JOptionPane.showMessageDialog(null, "Error al cargar datos: " + e.getMessage());
        }
    }

    public void mostrarPanel(String nombrePanel) {
        cardLayout.show(contentPanel, nombrePanel);
        if (nombrePanel.equals("mainPanel")) {
            try {
                actualizarTabla();
            } catch (ServiceException e) {
                JOptionPane.showMessageDialog(null, "Error al actualizar tabla: " + e.getMessage());
            }
        }
    }

    protected void volverAlMenuPrincipal() {
        mainMenuUI.mostrarMenuPrincipal();
    }

    public JPanel getMainPanel() {
        return contentPanel;
    }

    // Métodos abstractos que deben implementar las clases hijas
    protected abstract void initDAO();
    protected abstract void initUIComponents();
    protected abstract void actualizarTabla() throws ServiceException;
    protected abstract void buscarPorEmail();
    protected abstract void actualizarFormulariosConSeleccion();

    protected void consultarTurnos() {
        if (table.getSelectedRow() != -1) {
            int id = (int) tableModel.getValueAt(table.getSelectedRow(), 0);
            TurnoService turnoService = new TurnoServiceImpl(new TurnoDAOImpl(conexion));
            ConsultarTurnosUI consultarTurnosUI = new ConsultarTurnosUI(turnoService, id);
            contentPanel.add(consultarTurnosUI, "consultarTurnos");
            mostrarPanel("consultarTurnos");
        } else {
            JOptionPane.showMessageDialog(null, "Por favor, seleccione una fila para consultar turnos");
        }
    }
}
