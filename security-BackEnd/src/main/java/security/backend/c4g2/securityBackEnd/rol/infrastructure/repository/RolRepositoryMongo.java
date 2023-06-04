package security.backend.c4g2.securityBackEnd.rol.infrastructure.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import security.backend.c4g2.securityBackEnd.rol.infrastructure.repository.dto.RolDto;

public interface RolRepositoryMongo extends MongoRepository<RolDto, String> {

}
