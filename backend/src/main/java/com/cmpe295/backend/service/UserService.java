package com.cmpe295.backend.service;

import org.springframework.beans.factory.annotation.Autowired;
import com.cmpe295.backend.repository.UserRepository;
import com.cmpe295.backend.model.User;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    public User getUser(Integer id) {
        return userRepository.findById(id).orElse(null);
    }
    
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }
}
