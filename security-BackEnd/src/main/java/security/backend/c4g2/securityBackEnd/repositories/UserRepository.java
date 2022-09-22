package security.backend.c4g2.securityBackEnd.repositories;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import security.backend.c4g2.securityBackEnd.models.User;

public interface UserRepository extends MongoRepository<User,String> {
    @Query("{'email':?0}")
    public User getUserByMail(String email);
}
