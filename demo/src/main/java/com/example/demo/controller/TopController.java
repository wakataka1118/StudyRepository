package com.example.demo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import com.example.demo.request.Request;

@Controller
@RequestMapping("/")
public class TopController {

    @GetMapping
    public String top() {
        return "top";
    }
}
