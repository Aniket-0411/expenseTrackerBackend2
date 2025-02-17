package com.cmpe295.backend.controller;

import com.cmpe295.backend.service.expenseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;
import com.cmpe295.backend.model.Expense;
import java.util.List;
import java.util.Map;


@RestController
public class expenseController {
    @Autowired
    private expenseService expenseService;

    //return all expenses from database
    @GetMapping("/getAllExpenses")
    public List<Expense> getAllExpenses() {
        return expenseService.getAllExpenses();
    }
    
    // get distinct categories and number of occurrences using a HashMap
    @GetMapping("/getCategoryCounts")
    public Map<String, Long> getCategoryCounts() {
        return expenseService.getCategoryCounts();
    }

}
