package Model;

public class Medico {
    private int id;
    private String nombreYApellido;
    private String dni;
    private String telefono;
    private String email;
    private String especialidad;
    private String matricula;

    // Constructor
    public Medico(int id, String nombreYApellido, String dni, String telefono, String email, String especialidad, String matricula) {
        this.id = id;
        this.nombreYApellido = nombreYApellido;
        this.dni = dni;
        this.telefono = telefono;
        this.email = email;
        this.especialidad = especialidad;
        this.matricula = matricula;
    }

    // Getters and Setters
    public int getId() { return id; }
    public void setId(int id) { this.id = id; }

    public String getNombreYApellido() { return nombreYApellido; }
    public void setNombreYApellido(String nombreYApellido) { this.nombreYApellido = nombreYApellido; }

    public String getDni() { return dni; }
    public void setDni(String dni) { this.dni = dni; }

    public String getTelefono() { return telefono; }
    public void setTelefono(String telefono) { this.telefono = telefono; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getEspecialidad() { return especialidad; }
    public void setEspecialidad(String especialidad) { this.especialidad = especialidad; }

    public String getMatricula() { return matricula; }
    public void setMatricula(String matricula) { this.matricula = matricula; }

    @Override
    public String toString() {
        return this.getNombreYApellido();
    }
} 