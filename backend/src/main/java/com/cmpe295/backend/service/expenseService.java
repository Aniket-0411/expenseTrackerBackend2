package com.cmpe295.backend.service;

import com.cmpe295.backend.model.Expense;
import com.cmpe295.backend.repository.expenseRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class expenseService {
    @Autowired
    private expenseRepository expenseRepository;

    //return all expenses from database
    public List<Expense> getAllExpenses() {
        return expenseRepository.findAll();
    }

    // get distinct categories and number of occurrences using a HashMap
    public Map<String, Long> getCategoryCounts() {
        // Using stream to group by category and count occurrences
        Map<String, Long> categoryCounts = expenseRepository.findAll().stream()
            .collect(
                HashMap::new,
                (map, expense) -> map.merge(expense.getCategory(), 1L, Long::sum),
                HashMap::putAll
            );
        return categoryCounts;
    }

    // get the the 
}
