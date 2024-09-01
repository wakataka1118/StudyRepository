package com.example.demo.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import com.example.demo.constants.ResponseCode;
import com.example.demo.request.Request;
import com.example.demo.service.ClientService;

@RestController
@RequestMapping("/client")

public class ClientController {

    @Autowired
    ClientService service;

    @ResponseBody
    @PostMapping("/execute")
    public void execute(@RequestParam("str") String str) {
        Request request = new Request();
        request.setStr(str);
        // API実行処理
        try {
            ResponseCode response = service.doApi(request);
            if (response.getResultCode().equals("0")) {
                System.out.println("API連携成功");
                System.out.println("処理結果コード：" + response.getResultCode());
            } else {
                System.out.println("API連携失敗");
                System.out.println("処理結果コード：" + response.getResultCode());
            }
        } catch (Exception e) {
            System.out.println("API連携でエラーが発生しました。");
        }
    }
}
