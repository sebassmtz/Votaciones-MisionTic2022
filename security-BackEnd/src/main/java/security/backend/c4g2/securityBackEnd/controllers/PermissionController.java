package security.backend.c4g2.securityBackEnd.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import security.backend.c4g2.securityBackEnd.models.Permission;
import security.backend.c4g2.securityBackEnd.repositories.PermissionRepository;

import java.util.List;

@CrossOrigin
@RestController
@RequestMapping("/permissions")
public class PermissionController {

    @Autowired
    private PermissionRepository permissionRepository;

    @GetMapping("")
    public List<Permission> index(){
        return permissionRepository.findAll();
    }

    @ResponseStatus(HttpStatus.CREATED)
    @PostMapping
    public Permission create(@RequestBody Permission infoPermission){
        return permissionRepository.save(infoPermission);
    }

    @GetMapping("{id}")
    public Permission show(@PathVariable String id){
        return permissionRepository.findById(id).orElse(null);
    }

    @PutMapping("{id}")
    public Permission update(@PathVariable String id, @RequestBody Permission infoPermission){
        Permission permission = permissionRepository.findById(id).orElse(null);
        if (permission != null){
            permission.setMethod(infoPermission.getMethod());
            permission.setUrl(infoPermission.getUrl());
            return permissionRepository.save(permission);
        }else {
            return null;
        }
    }

    @ResponseStatus(HttpStatus.NO_CONTENT)
    @DeleteMapping("{id}")
    public void delete(@PathVariable String id){
        Permission permission = permissionRepository.findById(id).orElse(null);
        if (permission != null) {
            permissionRepository.delete(permission);
        }
    }

}
