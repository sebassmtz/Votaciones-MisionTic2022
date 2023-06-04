package security.backend.c4g2.securityBackEnd.rol.infrastructure.repository.mapper;

import security.backend.c4g2.securityBackEnd.rol.domain.models.Rol;
import security.backend.c4g2.securityBackEnd.rol.infrastructure.repository.dto.RolDto;

public class RolMapper {

    public static RolDto toDto(Rol rol){
        return new RolDto(rol.id(), rol.name(), rol.description());
    }

    public static Rol toDomain(RolDto rolDto){
        return new Rol(rolDto.getId(), rolDto.getName(), rolDto.getDescription());
    }
}
