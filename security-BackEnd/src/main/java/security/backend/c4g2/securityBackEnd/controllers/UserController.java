package security.backend.c4g2.securityBackEnd.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import security.backend.c4g2.securityBackEnd.models.Rol;
import security.backend.c4g2.securityBackEnd.models.User;
import security.backend.c4g2.securityBackEnd.repositories.RolRepository;
import security.backend.c4g2.securityBackEnd.repositories.UserRepository;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.List;

@CrossOrigin
@RestController
@RequestMapping("/users")
public class UserController {

    @Autowired
    private UserRepository userRepository;
    @Autowired
    private RolRepository rolRepository;

    @GetMapping("")
    public List<User> index() {
        return userRepository.findAll();
    }

    @ResponseStatus(HttpStatus.CREATED)
    @PostMapping
    public User create(@RequestBody User infoUser) {
        infoUser.setPassword(convertSHA256(infoUser.getPassword()));
        return userRepository.save(infoUser);
    }

    @GetMapping("{id}")
    public User show(@PathVariable String id){
        return userRepository.findById(id).orElse(null);
    }

    @PutMapping("{id}")
    public User update(@PathVariable String id,@RequestBody User infoUser){
        User currentUser = userRepository.findById(id).orElse(null);
        if (currentUser != null) {
            currentUser.setPseudonym(infoUser.getPseudonym());
            currentUser.setEmail(infoUser.getEmail());
            currentUser.setPassword(convertSHA256(infoUser.getPassword()));
            return this.userRepository.save(currentUser);
        }else {
            return null;
        }
    }

    @ResponseStatus(HttpStatus.NO_CONTENT)
    @DeleteMapping("{id}")
    public void delete(@PathVariable String id){
        User currentUser = userRepository.findById(id).orElse(null);
        if (currentUser != null) {
            this.userRepository.delete(currentUser);
        }
    }

    /*
    * Relation (1 a n) between rol and user
    * */
    @PutMapping("{id}/rol/{id_rol}")
    public User toAssignRolToUser(@PathVariable String id,@PathVariable String id_rol){
        User currentUser = userRepository.findById(id).orElse(null);
        Rol currentRol = rolRepository.findById(id_rol).orElse(null);
        if (currentRol != null && currentRol != null) {
            currentUser.setRol(currentRol);
            return userRepository.save(currentUser);
        }
        return null;
    }

    public String convertSHA256(String password) {
        MessageDigest md = null;
        try {
            md = MessageDigest.getInstance("SHA-256");
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
            return null;
        }
        byte[] hash = md.digest(password.getBytes());
        StringBuffer sb = new StringBuffer();
        for (byte b : hash) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }

}
