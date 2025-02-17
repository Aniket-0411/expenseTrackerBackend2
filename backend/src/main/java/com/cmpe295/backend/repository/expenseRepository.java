package com.cmpe295.backend.repository;

import com.cmpe295.backend.model.Expense;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface expenseRepository extends JpaRepository<Expense, Integer> {
    // Additional query methods can go here
}
