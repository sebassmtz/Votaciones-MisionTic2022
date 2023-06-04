package security.backend.c4g2.securityBackEnd.rol.application.createRolUseCase;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import security.backend.c4g2.securityBackEnd.rol.domain.models.Rol;
import security.backend.c4g2.securityBackEnd.rol.domain.repository.RolRepository;

@Component
public class CreateRolUseCase{



    private RolRepository rolRepository;

    public CreateRolUseCase(RolRepository rolRepository) {
        this.rolRepository = rolRepository;
    }


    public Rol invoke(String name, String description) {
        return rolRepository.saveRol(new Rol(null,name, description));
    }
}
