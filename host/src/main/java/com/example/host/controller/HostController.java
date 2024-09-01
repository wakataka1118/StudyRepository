package com.example.host.controller;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import com.example.host.request.Request;
import com.example.host.response.Response;

@RestController
@RequestMapping("/host")
public class HostController {
    @PostMapping("/response")
    @ResponseBody
    public Response createResponse(@RequestBody Request request) {
        Response response = new Response();
        try {
            System.out.println("受領したリクエストの文字列=" + request.getStr());
            response.setResultCode("0");
            System.out.println("レスポンスで返す処理結果コードは→" + response.getResultCode());
            return response;
        } catch (Exception e) {
            response.setResultCode("1");
            System.out.println("エラーが発生しました。処理結果コード1を返却");
            return response;

        }
    }
}
