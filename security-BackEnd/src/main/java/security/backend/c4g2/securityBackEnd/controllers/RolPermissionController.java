package security.backend.c4g2.securityBackEnd.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import security.backend.c4g2.securityBackEnd.models.Permission;
import security.backend.c4g2.securityBackEnd.models.Rol;
import security.backend.c4g2.securityBackEnd.models.RolPermission;
import security.backend.c4g2.securityBackEnd.repositories.PermissionRepository;
import security.backend.c4g2.securityBackEnd.repositories.RolPermissionRepository;
import security.backend.c4g2.securityBackEnd.repositories.RolRepository;

import java.util.List;

@CrossOrigin
@RestController
@RequestMapping("/rol-permission")
public class RolPermissionController {
    @Autowired
    private RolPermissionRepository rolPermissionRepository;
    @Autowired
    private RolRepository rolRepository;
    @Autowired
    private PermissionRepository permissionRepository;

    @GetMapping("")
    public List<RolPermission> index(){
        return this.rolPermissionRepository.findAll();
    }

    /* Asignacion de rol y permiso*/
    @ResponseStatus(HttpStatus.CREATED)
    @PostMapping("rol/{id_rol}/permission/{id_permission}")
    public RolPermission create(@PathVariable String id_rol,@PathVariable String id_permission){
        Rol rol = rolRepository.findById(id_rol).orElse(null);
        Permission permission = permissionRepository.findById(id_permission).orElse(null);
        if (permission != null && rol != null) {
            RolPermission rolPermission = new RolPermission(rol,permission);
            return rolPermissionRepository.save(rolPermission);
        }
        return  null;
    }



}
