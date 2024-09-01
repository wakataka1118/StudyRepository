package com.example.demo.service;

import java.net.URI;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.MediaType;
import org.springframework.http.RequestEntity;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import com.example.demo.result.Result;
import com.example.demo.constants.ResponseCode;
import com.example.demo.request.Request;

@Service
public class ClientService {

    // REST通信用のテンプレート
    @Autowired
    RestTemplateBuilder builder;

    public ResponseCode doApi(Request request) throws Exception {
        // 送信先URL
        String url = "http://localhost:8081/host/response";

        try {
            Result result = post(url, request, Result.class);
            System.out.println(result);
            return ResponseCode.getEnumByResultCode(result.getResultCode());
        } catch (Exception e) {
            System.out.println("例外発生");
            throw e;
        }

    }

    // POST送信実行
    public <T, U> U post(String url, T param, Class<U> resClazz) throws Exception {
        RequestEntity<T> entity = RequestEntity.post(new URI(url)).accept(MediaType.APPLICATION_JSON).body(param);
        ResponseEntity<U> response = builder.build().exchange(entity, resClazz);
        return response != null ? response.getBody() : null;
    }
}
