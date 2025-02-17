package com.cmpe295.backend.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Column;
import lombok.*;
import java.sql.Date;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Expense {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "DATE")
    private Date date; 

    @Column(name = "DESCRIPTION")
    private String description;   

    @Column(name = "CATEGORY")
    private String category; 

    @Column(name = "AMOUNT")
    private double amount;     

    @Column(name = "EXPENSE")
    private String expense;  

    @Column(name = "USER_ID")
    private int userId; 
}
