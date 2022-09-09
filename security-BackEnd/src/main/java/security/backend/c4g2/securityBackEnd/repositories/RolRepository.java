package security.backend.c4g2.securityBackEnd.repositories;

import org.springframework.data.mongodb.repository.MongoRepository;
import security.backend.c4g2.securityBackEnd.models.Rol;

public interface RolRepository extends MongoRepository<Rol, String> {

}
