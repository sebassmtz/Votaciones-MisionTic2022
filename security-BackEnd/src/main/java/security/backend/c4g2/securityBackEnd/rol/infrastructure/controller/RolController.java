package security.backend.c4g2.securityBackEnd.rol.infrastructure.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import security.backend.c4g2.securityBackEnd.rol.application.createRolUseCase.CreateRolUseCase;
import security.backend.c4g2.securityBackEnd.rol.infrastructure.controller.requests.RolCreateRequest;


@CrossOrigin
@RestController
@RequestMapping("/rol")
public class RolController {

    @Autowired
    private CreateRolUseCase createRolUseCase;

    @ResponseStatus(HttpStatus.CREATED)
    @PostMapping
    public ResponseEntity<?> create(@RequestBody RolCreateRequest request){

        var rol = createRolUseCase.invoke(request.name(), request.description());
        return new ResponseEntity<>(rol, HttpStatus.CREATED);
    }


}
