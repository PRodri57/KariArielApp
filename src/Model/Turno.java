package Model;

import java.util.Date;

public class Turno {
    private int id;
    private Date fecha;
    private Date hora;
    private Medico medico;
    private Paciente paciente;
    private String estado; // "Pendiente", "Confirmado", "Cancelado", "Completado"

    public Turno(int id, Date fecha, Date hora, Medico medico, Paciente paciente, String estado) {
        this.id = id;
        this.fecha = fecha;
        this.hora = hora;
        this.medico = medico;
        this.paciente = paciente;
        this.estado = estado;
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
}
