package UI;

import DAO.TurnoDAOImpl;
import Model.Turno;
import Model.Medico;
import Model.Paciente;
import Service.TurnoService;
import Service.TurnoServiceImpl;
import Service.MedicoService;
import Service.PacienteService;
import Service.ServiceException;
import Service.MedicoServiceImpl;
import Service.PacienteServiceImpl;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.sql.Connection;
import java.text.SimpleDateFormat;
import java.util.List;

public class TurnoPanelManager extends AbstractPanelManager {
    private TurnoService turnoService;
    private MedicoService medicoService;
    private PacienteService pacienteService;
    private AgregarTurnoUI agregarTurnoUI;
    private ModificarTurnoUI modificarTurnoUI;
    private EliminarTurnoUI eliminarTurnoUI;
    private ConsultarTurnosUI consultarTurnosUI;

    public TurnoPanelManager(MainMenuUI mainMenuUI, Connection conexion, 
                           MedicoService medicoService, PacienteService pacienteService) {
        super(mainMenuUI, conexion);
        this.medicoService = medicoService;
        this.pacienteService = pacienteService;
        init();
    }

    @Override
    protected void initDAO() {
        TurnoDAOImpl turnoDAO = new TurnoDAOImpl(conexion);
        turnoService = new TurnoServiceImpl(turnoDAO);
        
        tableModel = new DefaultTableModel(
            new Object[]{"ID", "Fecha", "Hora", "Médico", "Paciente", "Estado"}, 
            0
        ) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };
    }

    @Override
    protected void initUIComponents() {
        try {
            List<Medico> medicos = medicoService.obtenerTodos();
            List<Paciente> pacientes = pacienteService.obtenerTodos();
            
            agregarTurnoUI = new AgregarTurnoUI(turnoService, this, medicos, pacientes);
            modificarTurnoUI = new ModificarTurnoUI(turnoService, this, medicos, pacientes);
            eliminarTurnoUI = new EliminarTurnoUI(this, turnoService);
            consultarTurnosUI = new ConsultarTurnosUI(turnoService, -1); // -1 para mostrar todos los turnos
            
            contentPanel.add(agregarTurnoUI, "agregar");
            contentPanel.add(modificarTurnoUI, "modificar");
            contentPanel.add(eliminarTurnoUI, "eliminar");
            contentPanel.add(consultarTurnosUI, "consultarTurnos");
            
        } catch (ServiceException e) {
            JOptionPane.showMessageDialog(null, "Error al inicializar la interfaz: " + e.getMessage());
        }
    }

    @Override
    protected void actualizarTabla() throws ServiceException {
        tableModel.setRowCount(0);
        SimpleDateFormat dateFormat = new SimpleDateFormat("dd/MM/yyyy");
        SimpleDateFormat timeFormat = new SimpleDateFormat("HH:mm");
        
        List<Turno> turnos = turnoService.obtenerTodos();
        for (Turno turno : turnos) {
            tableModel.addRow(new Object[]{
                turno.getId(),
                dateFormat.format(turno.getFecha()),
                timeFormat.format(turno.getHora()),
                turno.getMedico().getNombreYApellido(),
                turno.getPaciente().getNombreYApellido(),
                turno.getEstado()
            });
        }
    }

    @Override
    protected void buscarPorEmail() {
        // No se implementa para turnos
    }

    @Override
    protected void actualizarFormulariosConSeleccion() {
        int selectedRow = table.getSelectedRow();
        if (selectedRow != -1) {
            int id = (int) tableModel.getValueAt(selectedRow, 0);
            try {
                Turno turno = turnoService.obtenerPorId(id);
                modificarTurnoUI.setFormData(turno);
                eliminarTurnoUI.setFormData(turno);
            } catch (ServiceException e) {
                JOptionPane.showMessageDialog(null, "Error al cargar el turno: " + e.getMessage());
            }
        }
    }
} 