package com.cmpe295.backend.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;

import com.cmpe295.backend.model.User;
import com.cmpe295.backend.service.UserService;
import java.util.List;


@RestController
public class UserController {
    @Autowired
    private UserService userService;
    
    @GetMapping("/getUser")
    public User getUser() {
        return userService.getUser(1);
    }
    
    @GetMapping("/getAllUsers")
    public List<User> getAllUsers() {
        return userService.getAllUsers();
    }
}
