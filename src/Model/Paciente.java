package Model;

public class Paciente {
    private int id;
    private String nombreYApellido;
    private String dni;
    private String telefono;
    private String email;
    private String obraSocial;

    public Paciente(String nombreYApellido, String dni, String telefono, String email, String obraSocial) {
        this.nombreYApellido = nombreYApellido;
        this.dni = dni;
        this.telefono = telefono;
        this.email = email;
        this.obraSocial = obraSocial;
    }

    public Paciente(int id, String nombreYApellido, String dni, String telefono, String email, String obraSocial) {
        this.id = id;
        this.nombreYApellido = nombreYApellido;
        this.dni = dni;
        this.telefono = telefono;
        this.email = email;
        this.obraSocial = obraSocial;
    }

    public Paciente() {}

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getNombreYApellido() {
        return nombreYApellido;
    }

    public void setNombreYApellido(String nombreYApellido) {
        this.nombreYApellido = nombreYApellido;
    }

    public String getDni() {
        return dni;
    }

    public void setDni(String dni) {
        this.dni = dni;
    }

    public String getTelefono() {
        return telefono;
    }

    public void setTelefono(String telefono) {
        this.telefono = telefono;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getObraSocial() {
        return obraSocial;
    }

    public void setObraSocial(String obraSocial) {
        this.obraSocial = obraSocial;
    }

    @Override
    public String toString() {
        return nombreYApellido; // Para mostrar el nombre y apellido en el JList
    }
}