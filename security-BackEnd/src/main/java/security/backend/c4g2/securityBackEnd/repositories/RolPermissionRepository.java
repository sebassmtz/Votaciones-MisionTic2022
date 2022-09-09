package security.backend.c4g2.securityBackEnd.repositories;

import org.springframework.data.mongodb.repository.MongoRepository;
import security.backend.c4g2.securityBackEnd.models.RolPermission;

public interface RolPermissionRepository extends MongoRepository<RolPermission, String> {

}
