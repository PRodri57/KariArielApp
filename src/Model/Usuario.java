package Model;

public class Usuario {
    private int id;
    private String username;
    private String password;
    private String rol;
    private Integer medicoId;  // Puede ser null para admin
    private Integer pacienteId;  // Nuevo campo

    public Usuario(int id, String username, String password, String rol, Integer medicoId) {
        this.id = id;
        this.username = username;
        this.password = password;
        this.rol = rol;
        this.medicoId = medicoId;
    }

    // Getters y Setters
    public int getId() { return id; }
    public void setId(int id) { this.id = id; }

    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }

    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }

    public String getRol() { return rol; }
    public void setRol(String rol) { this.rol = rol; }

    public Integer getMedicoId() { return medicoId; }
    public void setMedicoId(Integer medicoId) { this.medicoId = medicoId; }

    public Integer getPacienteId() {
        return pacienteId;
    }

    public void setPacienteId(Integer pacienteId) {
        this.pacienteId = pacienteId;
    }
} 