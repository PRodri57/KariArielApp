package Model;

import java.util.Date;

public class Turno {
    private int id;
    private int medicoId;
    private int pacienteId;
    private Date fecha;
    private Date hora;
    private Medico medico;
    private Paciente paciente;
    private String estado; // "Pendiente", "Confirmado", "Cancelado", "Completado"

    public Turno() {
        // Constructor vacío
    }

    public Turno(int id, Date fecha, Date hora, Medico medico, Paciente paciente, String estado) {
        this.id = id;
        this.fecha = fecha;
        this.hora = hora;
        this.medico = medico;
        this.paciente = paciente;
        this.estado = estado;
        this.medicoId = medico.getId();
        this.pacienteId = paciente.getId();
    }

    // Getters y Setters
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public Date getFecha() {
        return fecha;
    }

    public void setFecha(Date fecha) {
        this.fecha = fecha;
    }

    public Date getHora() {
        return hora;
    }

    public void setHora(Date hora) {
        this.hora = hora;
    }

    public Medico getMedico() {
        return medico;
    }

    public void setMedico(Medico medico) {
        this.medico = medico;
    }

    public Paciente getPaciente() {
        return paciente;
    }

    public void setPaciente(Paciente paciente) {
        this.paciente = paciente;
    }

    public String getEstado() {
        return estado;
    }

    public void setEstado(String estado) {
        this.estado = estado;
    }

    public int getMedicoId() {
        return medicoId;
    }

    public void setMedicoId(int medicoId) {
        this.medicoId = medicoId;
    }

    public int getPacienteId() {
        return pacienteId;
    }

    public void setPacienteId(int pacienteId) {
        this.pacienteId = pacienteId;
    }
}
