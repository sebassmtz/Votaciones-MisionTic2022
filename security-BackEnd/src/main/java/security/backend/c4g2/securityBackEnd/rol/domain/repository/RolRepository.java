package security.backend.c4g2.securityBackEnd.rol.domain.repository;

import security.backend.c4g2.securityBackEnd.rol.domain.models.Rol;

import java.util.List;

public interface RolRepository {

    Rol getRolById(String id);
    Rol saveRol(Rol rol);
    Rol deleteRol(Rol rol);
    Rol updateRol(Rol rol);
    List<Rol> getAllRoles();

}
