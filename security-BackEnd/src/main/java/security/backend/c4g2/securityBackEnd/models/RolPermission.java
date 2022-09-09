package security.backend.c4g2.securityBackEnd.models;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.DBRef;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document
public class RolPermission {
    @Id
    private String _id;
    @DBRef
    private Rol rol;
    @DBRef
    private Permission permission;

    public RolPermission(Rol rol, Permission permission) {
        this.rol = rol;
        this.permission = permission;
    }

    public String get_id() {
        return _id;
    }

    public void set_id(String _id) {
        this._id = _id;
    }

    public Rol getRol() {
        return rol;
    }

    public void setRol(Rol rol) {
        this.rol = rol;
    }

    public Permission getPermission() {
        return permission;
    }

    public void setPermission(Permission permission) {
        this.permission = permission;
    }
}
