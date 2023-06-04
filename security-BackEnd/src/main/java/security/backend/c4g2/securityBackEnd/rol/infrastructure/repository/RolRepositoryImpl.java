package security.backend.c4g2.securityBackEnd.rol.infrastructure.repository;

import org.springframework.stereotype.Component;
import security.backend.c4g2.securityBackEnd.rol.domain.models.Rol;
import security.backend.c4g2.securityBackEnd.rol.domain.repository.RolRepository;
import security.backend.c4g2.securityBackEnd.rol.infrastructure.repository.dto.RolDto;
import security.backend.c4g2.securityBackEnd.rol.infrastructure.repository.mapper.RolMapper;

import java.util.List;

@Component
public class RolRepositoryImpl implements RolRepository {

    private RolRepositoryMongo rolRepositoryMongo;

    public RolRepositoryImpl(RolRepositoryMongo rolRepositoryMongo) {
        this.rolRepositoryMongo = rolRepositoryMongo;
    }

    @Override
    public Rol getRolById(String id) {
        return null;
    }

    @Override
    public Rol saveRol(Rol rol) {
        return RolMapper.toDomain(
                rolRepositoryMongo.save(RolMapper.toDto(rol))
        );
    }

    @Override
    public Rol deleteRol(Rol rol) {
        return null;
    }

    @Override
    public Rol updateRol(Rol rol) {
        return null;
    }

    @Override
    public List<Rol> getAllRoles() {
        return null;
    }
}
